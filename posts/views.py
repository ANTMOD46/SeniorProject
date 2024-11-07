from django.shortcuts import render, redirect
from .models import SellItem  # สมมติว่าคุณมีโมเดลชื่อ SellItem
from .forms import SellItemForm
from .forms import DonationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from .forms import GeneralAnnouncementForm

def home(request):
    return render(request, 'SeniorProject/home.html')  # ชี้ไปยังตำแหน่งเทมเพลต home.html



def post_ad_view(request):
    # คุณสามารถเพิ่มการจัดการสำหรับการโพสต์โฆษณาที่นี่
    return render(request, 'posts/post_ad.html')  # เปลี่ยนเป็นชื่อ template ที่ต้องการ


def sell_item_all(request):
    items = SellItem.objects.filter(is_closed=False)  # ดึงข้อมูลสินค้าที่ยังเปิดอยู่
    return render(request, 'posts/sell_item_all.html', {'items': items})

def donation_all(request):
    # สามารถดึงข้อมูลการบริจาคที่จำเป็นและส่งไปยังเทมเพลตได้ที่นี่
    return render(request, 'donation/donation_all.html')  # ใช้เทมเพลตที่เหมาะสม

def announcement_all(request):
    # นี่เป็นตัวอย่างของข้อมูลการประกาศ
    announcements = []  # เปลี่ยนเป็นการดึงข้อมูลจริงจากฐานข้อมูล
    return render(request, 'accounts/announcement_all.html', {'announcements': announcements})


