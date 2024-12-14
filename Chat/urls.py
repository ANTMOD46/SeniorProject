from django.urls import path
from . import views


urlpatterns = [
    path('start/<int:user_id>/', views.start_chat, name='start_chat'),
    path('room/<int:chatroom_id>/', views.chat_room, name='chat_room'),
    path('room/<int:chatroom_id>/', views.chat_room, name='chat_room'),
    path('list/', views.chat_list, name='rooms'),  # กำหนดชื่อ URL name เป็น 'rooms'
     path('start/<int:post_id>/<str:post_type>/', views.start_chat, name='start_chat'),
     
     
    
]
