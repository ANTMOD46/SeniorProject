from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Room
from django.contrib import messages
from .models import Room, Message 

@login_required
def rooms(request):
    rooms = Room.objects.all()
    return render(request, 'rooms/rooms.html', {'mods': rooms})

@login_required
def room(request, slug):
    room = Room.objects.get(slug=slug)
    messages = room.messages.all()  # ดึงข้อความจากห้องนี้
    
    return render(request, 'rooms/room.html', {'room': room, 'messages': messages})

@login_required
def send_message(request, slug):
    room = Room.objects.get(slug=slug)
    
    if request.method == 'POST':
        content = request.POST['message']
        message = Message.objects.create(room=room, sender=request.user, content=content)
    
    return redirect('room', slug=slug)

@login_required
def create_room(request):
    if request.method == 'POST':
        room_name = request.POST['name']
        room_slug = room_name.lower().replace(' ', '-')
        room = Room.objects.create(name=room_name, slug=room_slug)
        messages.success(request, f'ห้องแชท "{room_name}" ถูกสร้างแล้ว!')
        return redirect('rooms')
    
    return render(request, 'rooms/create_room.html')




