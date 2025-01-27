from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.utils.timezone import now, make_aware
from datetime import datetime
from django.db.models import Max

# นำเข้าโมเดล
from .models import ChatRoom, Message
from posts.models import GeneralAnnouncement, SellItem, Donation  # โมเดลที่เกี่ยวข้องกับโพสต์

# นำเข้าโมเดล User
from django.contrib.auth import get_user_model
User = get_user_model()



@login_required
def start_chat(request, user_id=None, post_id=None, post_type=None):
    user1 = request.user

    # ตรวจสอบว่า `user_id` มีค่าหรือไม่
    if user_id:
        user2 = get_object_or_404(User, id=user_id)
    elif post_id and post_type:
        if post_type == 'sell_item':
            post = get_object_or_404(SellItem, id=post_id)
        elif post_type == 'donation':
            post = get_object_or_404(Donation, id=post_id)
        elif post_type == 'general_announcement':
            post = get_object_or_404(GeneralAnnouncement, id=post_id)
        else:
            return HttpResponseBadRequest("Invalid post type")
        user2 = post.user
    else:
        return HttpResponseBadRequest("Invalid request")

    # ตรวจสอบว่าห้องแชทมีอยู่แล้วหรือไม่
    chatroom, created = ChatRoom.objects.get_or_create(
        user1=min(user1, user2, key=lambda u: u.id),  # จัดเรียง user1 เป็น id ต่ำกว่าเสมอ
        user2=max(user1, user2, key=lambda u: u.id)
    )

    # Redirect ไปยังหน้าห้องแชท
    return redirect('chat_room', chatroom_id=chatroom.id)



@login_required
def chat_room(request, chatroom_id):
    """
    ห้องแชทหลัก:
    - โหลดข้อความจากฐานข้อมูล (GET ปกติ)
    - ดึงข้อความใหม่เมื่อมีการร้องขอด้วย AJAX
    - เพิ่มข้อความใหม่ลงในฐานข้อมูลเมื่อ POST
    """
    # ดึงข้อมูลห้องแชท
    chatroom = get_object_or_404(ChatRoom, id=chatroom_id)

    # ตรวจสอบสิทธิ์การเข้าถึงห้องแชท
    if request.user != chatroom.user1 and request.user != chatroom.user2:
        return HttpResponseForbidden("คุณไม่มีสิทธิ์เข้าห้องแชทนี้")

    # เมื่อมีการส่งข้อความใหม่ผ่าน POST
    if request.method == "POST":
        content = request.POST.get("content")
        if content and content.strip():  # ตรวจสอบข้อความว่าไม่ว่างเปล่า
            message = Message.objects.create(
                chatroom=chatroom,
                sender=request.user,
                content=content.strip(),
                timestamp=now(),
            )
            return JsonResponse({
                "status": "success",
                "sender_id": message.sender.id,
                "username": message.sender.username,
                "content": message.content,
                "timestamp": message.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            })
        return JsonResponse({"status": "error", "message": "Empty content"}, status=400)

    # เมื่อมีการร้องขอดึงข้อความใหม่ผ่าน AJAX/GET (โหลดข้อความหลัง last_timestamp)
    if request.GET.get("last_timestamp"):
        last_timestamp = request.GET.get("last_timestamp")
        try:
            last_timestamp = make_aware(datetime.strptime(last_timestamp, "%Y-%m-%d %H:%M:%S"))
        except (ValueError, TypeError):
            return JsonResponse({"error": "Invalid timestamp format"}, status=400)

        new_messages = chatroom.messages.filter(timestamp__gt=last_timestamp).order_by('timestamp')
        return JsonResponse({
            "messages": [
                {
                    "sender_id": message.sender.id,
                    "username": message.sender.username,
                    "content": message.content,
                    "timestamp": message.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                }
                for message in new_messages
            ]
        })

    # เมื่อเป็น GET request ปกติ (โหลดหน้าเว็บ)
    messages = chatroom.messages.order_by('timestamp')

    # ดึงข้อมูลคู่สนทนา
    other_user = chatroom.user1 if chatroom.user2 == request.user else chatroom.user2

    return render(request, 'chat/chat_room.html', {
        'chatroom': chatroom,
        'messages': messages,
        'other_user': other_user,  # คู่สนทนา
    })


@login_required
def chat_list(request):
    chatrooms = ChatRoom.objects.filter(user1=request.user) | ChatRoom.objects.filter(user2=request.user)
    chatrooms = chatrooms.distinct().annotate(last_message_time=Max('messages__timestamp')).order_by('-last_message_time')

    return render(request, 'chat/chat_list.html', {
        'chatrooms': chatrooms,
    })


