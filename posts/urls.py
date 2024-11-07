from django.urls import path
from . import views
from .views import post_ad_view, sell_item_all , donation_all,announcement_all
from .views import post_ad_view

urlpatterns = [
    path('', views.home, name='posts-home'),  # หรือชื่อ view ที่มีอยู่
    path('post-ad/', post_ad_view, name='post_ad'),
    path('sell_items/', sell_item_all, name='sell_item_all'),
    path('donation/', donation_all, name='donation_all'),  # เส้นทางสำหรับหน้าบริจาค
    path('announcement_all/', announcement_all, name='announcement_all'),
    path('post-ad/', post_ad_view, name='post_ad'),
   
]


