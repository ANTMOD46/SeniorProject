from django.urls import path
from .views import separate_waste  # นำเข้าฟังก์ชันวิว

urlpatterns = [
    path('', separate_waste, name='separate_waste'),  # เปลี่ยนเป็นเส้นทางที่คุณต้องการ
]
