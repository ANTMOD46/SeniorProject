"""
URL configuration for SeniorProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


from . import views  # นำเข้า views จากโปรเจกต์หลัก
urlpatterns = [
    path("admin/", admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path('', views.home, name='home'),  # เส้นทางสำหรับหน้าหลัก
    path('posts/', include('posts.urls')),  # เส้นทางสำหรับ posts
    path('comments/', include('comments.urls')),  # ตัวอย่าง comments
    path('accounts/', include('accounts.urls')),
    path('waste/', include('waste_separation.urls')),
    path('Chat/', include('Chat.urls')),
    path('generator/', include('barcode_generator.urls')),
    path('scanner/', include('barcode_scanner.urls')),
   
    
    
    
    path('recycle/', views.recycle_view, name='recycle'),  # เส้นทางสำหรับขยะรีไซเคิล
    path('organic/', views.organic_view, name='organic'),  # เส้นทางสำหรับขยะเปียก
    path('general/', views.general_view, name='general'),  # เส้นทางสำหรับขยะทั่วไป
    path('hazardous/', views.hazardous_view, name='hazardous'),  # เส้นทางสำหรับขยะอันตราย
    

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


