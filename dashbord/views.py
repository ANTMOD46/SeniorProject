from django.shortcuts import render
from django.utils import timezone
from posts.models import SellItem, Donation, GeneralAnnouncement
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_today(request):
    today = timezone.now().date()

    # ข้อมูลประกาศซื้อขาย (วันนี้)
    buy_sales_today = SellItem.objects.filter(post_type='buy', created_at__date=today)
    sell_sales_today = SellItem.objects.filter(post_type='sell', created_at__date=today)

    # ข้อมูลปิดการซื้อขาย (วันนี้)
    buy_sales_closed_today = buy_sales_today.filter(is_closed=True)
    sell_sales_closed_today = sell_sales_today.filter(is_closed=True)

    # ข้อมูลการบริจาค (วันนี้)
    donations_today = Donation.objects.filter(created_at__date=today)
    donations_donors_today = donations_today.filter(role='donor')
    donations_receivers_today = donations_today.filter(role='recipient')

    # ข้อมูลปิดการบริจาค (วันนี้)
    donations_closed_today = donations_today.filter(is_closed=True)

    # ข้อมูลประกาศทั่วไป (วันนี้)
    general_announcements_today = GeneralAnnouncement.objects.filter(created_at__date=today)

    # ส่งข้อมูลไปยังเทมเพลต
    return render(request, 'dashbord/dashboard_today.html', {
        'buy_sales_today': buy_sales_today,
        'sell_sales_today': sell_sales_today,
        'buy_sales_closed_today': buy_sales_closed_today,
        'sell_sales_closed_today': sell_sales_closed_today,
        'donations_today': donations_today,
        'donations_donors_today': donations_donors_today,
        'donations_receivers_today': donations_receivers_today,
        'donations_closed_today': donations_closed_today,
        'general_announcements_today': general_announcements_today,
    })


@login_required
def dashboard_all(request):
    # ข้อมูลประกาศซื้อขายทั้งหมด
    buy_sales_all = SellItem.objects.filter(post_type='buy')
    sell_sales_all = SellItem.objects.filter(post_type='sell')

    # ข้อมูลปิดการซื้อขาย
    buy_sales_closed = buy_sales_all.filter(is_closed=True)
    sell_sales_closed = sell_sales_all.filter(is_closed=True)

    # ข้อมูลประกาศบริจาคทั้งหมด (ไม่กรอง `is_closed`)
    donations_all = Donation.objects.all()  # แก้ไขตรงนี้หากไม่ต้องการกรองเฉพาะการบริจาคที่เปิด
    donations_donors = donations_all.filter(role='donor')
    donations_receivers = donations_all.filter(role='recipient')

    # ข้อมูลปิดการบริจาค
    donations_closed = donations_all.filter(is_closed=True)

    # ข้อมูลประกาศทั่วไป
    general_announcements_all = GeneralAnnouncement.objects.all()

    return render(request, 'dashbord/dashboard_all.html', {
        'buy_sales_all': buy_sales_all,
        'sell_sales_all': sell_sales_all,
        'buy_sales_closed': buy_sales_closed,
        'sell_sales_closed': sell_sales_closed,
        'donations_all': donations_all,
        'donations_donors': donations_donors,
        'donations_receivers': donations_receivers,
        'donations_closed': donations_closed,
        'general_announcements_all': general_announcements_all,
    })


