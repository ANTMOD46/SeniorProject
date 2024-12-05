from django.urls import path
from . import views

urlpatterns = [
    path('', views.rooms, name='rooms'),
    path('create/', views.create_room, name='create_room'),  # เพิ่มเส้นทางนี้
    path('<slug:slug>/', views.room, name='room'),
    path('<slug:slug>/send/', views.send_message, name='send_message'),
]
