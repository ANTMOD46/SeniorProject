from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/today/', views.dashboard_today, name='dashboard_today'),
    path('dashboard/all/', views.dashboard_all, name='dashboard_all'),
]
