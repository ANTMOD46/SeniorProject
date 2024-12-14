from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from .models import ChatRoom, Message
from django.contrib.auth import get_user_model
from posts.models import GeneralAnnouncement, SellItem, Donation  # เพิ่ม GeneralAnnouncement


User = get_user_model()

from django.http import HttpResponseBadRequest
from posts.models import SellItem, Donation  # นำเข้าโมเดลที่เกี่ยวข้องกับโพสต์

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


from django.utils.timezone import make_aware
from datetime import datetime

from django.utils.timezone import now

from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse, HttpResponseForbidden
from django.utils.timezone import now, make_aware
from datetime import datetime
from .models import ChatRoom, Message
from django.contrib.auth.decorators import login_required

@login_required
def chat_room(request, chatroom_id):
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
                "content": message.content,
                "timestamp": message.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            })
        return JsonResponse({"status": "error", "message": "Empty content"}, status=400)

    # เมื่อมีการร้องขอดึงข้อความใหม่ผ่าน GET
    if request.method == "GET" and request.GET.get("last_timestamp"):
        last_timestamp = request.GET.get("last_timestamp")
        try:
            # แปลง `last_timestamp` เป็น datetime-aware
            last_timestamp = make_aware(datetime.strptime(last_timestamp, "%Y-%m-%d %H:%M:%S.%f"))
        except (ValueError, TypeError):
            return JsonResponse({"error": "Invalid timestamp format"}, status=400)

        new_messages = chatroom.messages.filter(timestamp__gt=last_timestamp).order_by('timestamp')
        return JsonResponse({
            "messages": [
                {
                    "sender_id": message.sender.id,
                    "content": message.content,
                    "timestamp": message.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                }
                for message in new_messages
            ]
        })

    # เมื่อเป็น GET request ปกติ (โหลดหน้าแชท)
    messages = chatroom.messages.order_by('timestamp')

    # ดึงข้อมูลผู้ใช้อีกคนในห้องแชท (นอกเหนือจากผู้ใช้ที่ล็อกอิน)
    other_user = chatroom.user1 if chatroom.user2 == request.user else chatroom.user2

    # Render ข้อมูลไปยัง Template
    return render(request, 'chat/chat_room.html', {
        'chatroom': chatroom,
        'messages': messages,
        'other_user': other_user,  # ส่งข้อมูลผู้ใช้อีกคนไปยัง Template
    })

    





from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ChatRoom

from django.db.models import Max

@login_required
def chat_list(request):
    chatrooms = ChatRoom.objects.filter(user1=request.user) | ChatRoom.objects.filter(user2=request.user)
    chatrooms = chatrooms.distinct().annotate(last_message_time=Max('messages__timestamp')).order_by('-last_message_time')

    return render(request, 'chat/chat_list.html', {
        'chatrooms': chatrooms,
    })


