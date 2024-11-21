from django.urls import path
from . import views
from .views import post_ad_view, sell_item_all , donation_all,announcement_all
from .views import post_ad_view
from .views import  SellItemView,SellItemDetailView
from .views import SellItemDeleteView
from .views import SellItemDetailView, EditItemView, DeleteItemView ,CloseSaleView
from .views import DonationDetailView
from .views import DonationDeleteView,DonationUpdateView
from . import views 
from .views import GeneralAnnouncementDetailView
from .views import GeneralAnnouncementView, GeneralAnnouncementDetailView
from .views import GeneralAnnouncementUpdateView
from .views import GeneralAnnouncementDeleteView
from .views import GeneralAnnouncementListView
from .views import UserStoreView
from .views import add_comment, delete_comment

urlpatterns = [
    path('', views.home, name='posts-home'),  # หรือชื่อ view ที่มีอยู่
    path('post-ad/', post_ad_view, name='post_ad'),
    path('sell_items/', sell_item_all, name='sell_item_all'),
    path('donation/', donation_all, name='donation_all'),  # เส้นทางสำหรับหน้าบริจาค
    path('announcement_all/', announcement_all, name='announcement_all'),
    path('post-ad/', post_ad_view, name='post_ad'),
    path('sell-item/', SellItemView.as_view(), name='sell_item'),
    path('sell-item/<int:item_id>/', SellItemDetailView.as_view(), name='sell_item_details'),
    path('sell-item/<int:pk>/delete/', SellItemDeleteView.as_view(), name='delete_item'),
    path('sell-item/<int:item_id>/', SellItemDetailView.as_view(), name='sell_item_details'),
    path('sell-item/<int:item_id>/edit/', EditItemView.as_view(), name='edit_item'),
    path('sell-item/<int:item_id>/edit/', EditItemView.as_view(), name='update_item'),
    path('sell-item/<int:pk>/delete/', DeleteItemView.as_view(), name='delete_item'),
    path('sell-item/<int:pk>/delete/', SellItemDeleteView.as_view(), name='delete_item'),
    path('sell-item/<int:item_id>/close-sale/', CloseSaleView.as_view(), name='close_sale'),
    
    
    path('donation-form/', views.DonationFormView.as_view(), name='donation_form'),
    path('donation/<int:pk>/', DonationDetailView.as_view(), name='donation_details'),
    path('donation/<int:pk>/delete/', DonationDeleteView.as_view(), name='delete_donation'),
    path('donation/<int:donation_id>/edit/', DonationUpdateView.as_view(), name='edit_donation'),
    path('donation/<int:donation_id>/edit/', DonationUpdateView.as_view(), name='update_donation'),
    path('donation/<int:pk>/', DonationDetailView.as_view(), name='donation_details'),
    
    
    
    path('general-announcement/', GeneralAnnouncementView.as_view(), name='general_announcement'),
    path('general-announcement/<int:pk>/', GeneralAnnouncementDetailView.as_view(), name='general_announcement_detail'),
   path('general-announcement/<int:pk>/edit/', GeneralAnnouncementUpdateView.as_view(), name='edit_announcement'),
    path('general-announcement/<int:pk>/delete/', GeneralAnnouncementDeleteView.as_view(), name='delete_announcement'),
    path('general-announcements/', GeneralAnnouncementListView.as_view(), name='general_announcement_all'),
    path('user/<str:username>/', views.UserStoreView.as_view(), name='user_store'),  # เพิ่มเส้นทางสำหรับหน้าร้านของ user
     path('user/<str:username>/', UserStoreView.as_view(), name='user_store'),
   
    path('comment/add/<int:pk>/', add_comment, name='add_comment'),
    path('comment/delete/<int:pk>/', delete_comment, name='delete_comment'),
    
]


