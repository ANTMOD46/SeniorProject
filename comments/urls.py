from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='comments-home'),  # หรือชื่อ view ที่มีอยู่
]
