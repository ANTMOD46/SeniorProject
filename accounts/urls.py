from django.urls import path
from django.contrib.auth import views as auth_views
from . import views  # ใช้ views จากแอป accounts
from .views import signup, login_view, home_user
from .views import profile_edit
from .views import CustomLogoutView

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),  # Login
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Logout
    path('signup/', views.signup, name='signup'),  # Signup (ฟังก์ชันที่เราจะสร้างใน views.py)
    # path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('signup/', signup, name='signup'),  # URL สำหรับการสมัครสมาชิก
    path('login/', login_view, name='login'),  # URL สำหรับล็อกอิน
    path('home_user/', home_user, name='home_user'),  # URL สำหรับหน้า home_user
    path('profile/edit/', profile_edit, name='profile_edit'),  
    path('accounts/logout/', CustomLogoutView.as_view(), name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('admin/members/', views.admin_member_list, name='admin_member_list'),
     path('admin/members/<int:member_id>/', views.view_member_detail, name='view_member_detail'),
    path('admin/members/<int:member_id>/delete/', views.delete_member, name='delete_member'),
    
     path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(template_name='accounts/password_reset_form.html'),
        name='password_reset'
    ),
    path(
        'password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
        name='password_reset_complete'
    ),
    
   
   
   

]
