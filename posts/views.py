from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, DetailView, ListView, UpdateView, DeleteView, CreateView
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
from django.db import models
from .models import SellItemComment


CustomUser = get_user_model()  # ดึงโมเดล CustomUser ที่กำหนดเอง

from .models import (
    SellItem,
    Donation,
    GeneralAnnouncement,
    GeneralAnnouncementComment,
    DonationComment,
)
from .forms import (
    SellItemForm,
    DonationForm,
    GeneralAnnouncementForm,
)

User = get_user_model()  # ใช้โมเดล User ที่กำหนดเอง (ถ้ามี)



def home(request):
    return render(request, 'SeniorProject/home.html')  # ชี้ไปยังตำแหน่งเทมเพลต home.html


def post_ad_view(request):
    # คุณสามารถเพิ่มการจัดการสำหรับการโพสต์โฆษณาที่นี่
    return render(request, 'posts/post_ad.html')  # เปลี่ยนเป็นชื่อ template ที่ต้องการ


def sell_item_all(request):
    # ดึงข้อมูลทั้งหมดจาก SellItem
    items = SellItem.objects.all()
    
    # รับค่าจาก query parameters
    role = request.GET.get('role')  # ?role=buyer หรือ seller
    status = request.GET.get('status')  # ?status=open หรือ closed
    title = request.GET.get('title')  # ?title=ข้อความค้นหา
    
    # กรองข้อมูลตามบทบาท
    if role:
        items = items.filter(user_role=role)
    
    # กรองข้อมูลตามสถานะ
    if status:
        if status == 'open':
            items = items.filter(is_closed=False)
        elif status == 'closed':
            items = items.filter(is_closed=True)
    
    # กรองข้อมูลตามหัวข้อ (title)
    if title:
        items = items.filter(title__icontains=title)  # ค้นหาแบบไม่สนใจตัวพิมพ์ใหญ่-เล็ก
    
    # ส่งข้อมูลไปยัง template
    context = {
        'items': items,
        'selected_role': role,
        'selected_status': status,
        'selected_title': title,
    }
    
    return render(request, 'posts/sell_item_all.html', context)


class SellItemView(View):
    def get(self, request):
        form = SellItemForm()
        return render(request, 'posts/sell_item.html', {'form': form})

    def post(self, request):
        form = SellItemForm(request.POST, request.FILES)
        print(request.POST)  # ตรวจสอบว่าฟิลด์ `location` ถูกส่งมาหรือไม่
        if form.is_valid():
            sell_item = form.save(commit=False)
            sell_item.user = request.user
            print(f"Location from form: {sell_item.location}")  # ดูค่าที่ได้จากฟอร์ม
            sell_item.save()
            messages.success(request, 'ลงประกาศขายสำเร็จ')
            return redirect('sell_item_details', item_id=sell_item.id)
        else:
            print(form.errors)  # แสดงข้อผิดพลาดในฟอร์ม (ถ้ามี)
            messages.error(request, 'เกิดข้อผิดพลาดในการลงประกาศ')
        return render(request, 'posts/sell_item.html', {'form': form})


class SellItemDetailView(View):
    def get(self, request, item_id):
        post_ad = get_object_or_404(SellItem, id=item_id)
        context = {
            'post_ad': post_ad,
            'can_edit': request.user == post_ad.user or request.user.is_staff,
            'is_owner': request.user == post_ad.user,
        }
        return render(request, 'posts/sell_item_details.html', context)

    def post(self, request, item_id):
        """จัดการคำขอ POST สำหรับลบความคิดเห็น"""
        comment_id = request.POST.get('comment_id')
        if comment_id:
            comment = get_object_or_404(SellItemComment, id=comment_id)
            # อนุญาตให้ลบถ้าเป็นเจ้าของโพสต์, เจ้าของความคิดเห็น หรือแอดมิน
            if request.user == comment.user or request.user.is_staff or request.user == comment.sell_item.user:
                comment.delete()
        return redirect('sell_item_details', item_id=item_id)



class SellItemDeleteView(DeleteView):
    model = SellItem
    template_name = 'posts/sell_item_confirm_delete.html'  # ชื่อไฟล์ที่ใช้ในการยืนยันการลบ
    success_url = reverse_lazy('sell_item_all')  # URL ที่จะนำไปหลังจากลบเสร็จ

    
    
# class EditItemView(UserPassesTestMixin, UpdateView):
#     model = SellItem
#     template_name = 'posts/edit_item.html'
    
#     def test_func(self):
#         post_ad = self.get_object()
#         return self.request.user == post_ad.user or self.request.user.is_staff


    
@login_required
def delete_item(request, item_id):
    # ดึงโพสต์ตาม ID
    post_ad = get_object_or_404(SellItem, id=item_id)
    # ตรวจสอบสิทธิ์การลบ
    if request.user == post_ad.user or request.user.is_staff:
        if request.method == 'POST':
            post_ad.delete()
            return JsonResponse({'success': True, 'message': 'ลบโพสต์สำเร็จ'})
        return JsonResponse({'success': False, 'message': 'คำขอไม่ถูกต้อง'})
    return JsonResponse({'success': False, 'message': 'คุณไม่มีสิทธิ์ลบโพสต์นี้'})


class EditItemView(UpdateView):
    model = SellItem
    fields = ['title', 'description', 'price', 'location', 'image']
    template_name = 'posts/edit_item.html'

    def get_object(self, queryset=None):
        return get_object_or_404(SellItem, id=self.kwargs['item_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_ad'] = self.get_object()  # Ensure 'post_ad' is available
        return context
    
    def get_success_url(self):
        # ระบุ URL ที่จะ redirect หลังจากบันทึกสำเร็จ
        return reverse('sell_item_details', kwargs={'item_id': self.object.id})



class CloseSaleView(View):
    def post(self, request, item_id):
        # ตรวจสอบว่าไอเท็มมีอยู่หรือไม่
        post_ad = get_object_or_404(SellItem, id=item_id)

        # ตรวจสอบสิทธิ์ของผู้ใช้
        if request.user == post_ad.user or request.user.is_staff:
            if not post_ad.is_closed:
                post_ad.is_closed = True
                post_ad.save()
                return JsonResponse({"success": True, "message": "ปิดการขายสำเร็จ"})
            else:
                return JsonResponse({"success": False, "message": "ประกาศนี้ถูกปิดการขายไปแล้ว"})

        # หากผู้ใช้ไม่มีสิทธิ์
        return JsonResponse({"success": False, "message": "คุณไม่มีสิทธิ์ปิดการขายนี้"}, status=403)

    


def donation_all(request):
    role = request.GET.get('role')
    status = request.GET.get('status')
    title = request.GET.get('title')

    donations = Donation.objects.all()

    if role:
        donations = donations.filter(role=role)
    if status:
        donations = donations.filter(is_closed=(status == 'closed'))
    if title:
        donations = donations.filter(title__icontains=title)

    context = {
        'donations': donations,
        'selected_role': role,
        'selected_status': status,
        'selected_title': title,
    }
    return render(request, 'posts/donation_all.html', context)



class DonationFormView(LoginRequiredMixin, CreateView):
    model = Donation
    form_class = DonationForm
    template_name = 'posts/donation_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('donation_details', kwargs={'pk': self.object.pk})
        

class DonationDetailView(LoginRequiredMixin, DetailView):
    model = Donation
    template_name = 'posts/donation_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['donation'] = self.object  # ส่ง object เป็น 'donation'
        context['post_id'] = self.object.id  # ส่ง ID ของโพสต์
        context['post_type'] = 'donation'  # ระบุประเภทโพสต์
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        content = request.POST.get('content')
        if content:
            DonationComment.objects.create(
                donation=self.object,
                user=request.user,
                content=content
            )
        return HttpResponseRedirect(reverse('donation_details', args=[self.object.id]))


class DonationUpdateView(UpdateView):
    model = Donation
    fields = ['title', 'description', 'location', 'phone', 'image']
    template_name = 'posts/edit_donation.html'

    def get_object(self, queryset=None):
        # ดึงวัตถุ Donation ตาม id ที่ระบุใน URL
        return get_object_or_404(Donation, id=self.kwargs['donation_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['donation'] = self.get_object()  # เพื่อให้มี 'donation' ใช้ใน template
        return context

    def get_success_url(self):
        return reverse('donation_details', kwargs={'pk': self.object.id})
    

    
class DonationDeleteView(DeleteView):
    model = Donation
    template_name = 'posts/donation_confirm_delete.html'  # ไฟล์เทมเพลตที่ใช้ยืนยันการลบ
    success_url = reverse_lazy('donation_all')  # เปลี่ยนตาม URL หลังลบเสร็จ



class CloseDonationView(View):
    def post(self, request, donation_id):
        donation = get_object_or_404(Donation, id=donation_id)
        if request.user == donation.user or request.user.is_staff:
            donation.is_closed = True
            donation.save()
            return JsonResponse({"success": True, "is_closed": donation.is_closed})
        return JsonResponse({"success": False, "message": "คุณไม่มีสิทธิ์ปิดการบริจาคนี้"})


    
def announcement_all(request):
    # ดึงข้อมูลการประกาศทั้งหมดจากฐานข้อมูล
    announcements = GeneralAnnouncement.objects.all()
    
    # รับค่าจาก query parameter
    title = request.GET.get('title')  # ค่าที่ผู้ใช้กรอกในช่องค้นหา
    
    # กรองข้อมูลตามหัวข้อการประกาศ
    if title:
        announcements = announcements.filter(title__icontains=title)  # กรองข้อมูลแบบไม่สนใจตัวพิมพ์ใหญ่-เล็ก

    # ส่งค่าที่กรองไปยัง template
    context = {
        'announcements': announcements,  # รายการการประกาศ
        'selected_title': title,  # ค่าที่กรอกในช่องค้นหา
    }
    return render(request, 'posts/general_announcement_all.html', context)



def general_announcement(request):
    # Logic สำหรับกระทู้สอบถามทั่วไป
    return render(request, 'posts/general_announcement.html')


class GeneralAnnouncementView(View):
    def get(self, request):
        form = GeneralAnnouncementForm()
        return render(request, 'posts/general_announcement.html', {'form': form})

    def post(self, request):
        form = GeneralAnnouncementForm(request.POST, request.FILES)
        if form.is_valid():
            general_announcement = form.save(commit=False)
            general_announcement.user = request.user
            general_announcement.save()
            messages.success(request, 'ลงประกาศทั่วไปสำเร็จ')
            
            # เปลี่ยนเส้นทางไปยังหน้ารายละเอียดประกาศที่เพิ่งสร้าง
            return redirect('general_announcement_detail', announcement_id=general_announcement.id)
        else:
            print(form.errors)  # พิมพ์ข้อผิดพลาดในกรณีที่ฟอร์มไม่ผ่าน
            messages.error(request, 'เกิดข้อผิดพลาดในการลงประกาศ')
        return render(request, 'posts/general_announcement.html', {'form': form})


@login_required
def general_announcement_details(request, announcement_id):
    announcement = get_object_or_404(GeneralAnnouncement, id=announcement_id)

    if request.method == 'POST':
        content = request.POST.get('content')
        GeneralAnnouncementComment.objects.create(
            general_announcement=announcement,
            user=request.user,
            content=content
        )
        return redirect('general_announcement_details', announcement_id=announcement_id)

    context = {
        'announcement': announcement,
    }
    return render(request, 'posts/general_announcement_detail.html', context)


class GeneralAnnouncementUpdateView(UpdateView):
    model = GeneralAnnouncement
    fields = ['title', 'content', 'location', 'image']
    template_name = 'posts/edit_general_announcement.html'
    success_url = reverse_lazy('general_announcement_all')  # เปลี่ยน URL นี้เป็น URL ที่คุณต้องการเปลี่ยนเส้นทาง

    # หรือใช้ dynamic success URL
    def get_success_url(self):
        return reverse_lazy('general_announcement_detail', kwargs={'announcement_id': self.object.pk})
    
    


class GeneralAnnouncementDeleteView(DeleteView):
    model = GeneralAnnouncement
    template_name = 'posts/gen_confirm_delete.html'  # เทมเพลตยืนยันการลบ
    success_url = reverse_lazy('general_announcement_all')  # ไปหน้ารายการโพสต์ทั่วไปหลังลบ

    def post(self, request, *args, **kwargs):
        obj = get_object_or_404(GeneralAnnouncement, pk=self.kwargs['pk'])
        obj.delete()
        return redirect(self.success_url)



class GeneralAnnouncementListView(ListView):
    model = GeneralAnnouncement
    template_name = 'posts/general_announcement_all.html'
    context_object_name = 'announcements'
    


class UserStoreView(ListView):
    template_name = 'posts/user_store.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs['username'])
        
        general_announcements = GeneralAnnouncement.objects.filter(user=user).annotate(
            model_name=models.Value('GeneralAnnouncement', output_field=models.CharField())
        )
        sell_items = SellItem.objects.filter(user=user).annotate(
            model_name=models.Value('SellItem', output_field=models.CharField())
        )
        donations = Donation.objects.filter(user=user).annotate(
            model_name=models.Value('Donation', output_field=models.CharField())
        )

        # รวมโพสต์ทั้งหมดและเรียงตามวันที่
        all_posts = list(general_announcements) + list(sell_items) + list(donations)
        all_posts.sort(key=lambda x: x.created_at, reverse=True)

        return all_posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_profile'] = get_object_or_404(User, username=self.kwargs['username'])
        return context


@login_required
def add_comment(request, post_id):
    if request.method == 'POST':
        content = request.POST.get('content')
        sell_item = get_object_or_404(SellItem, id=post_id)

        print("User ID:", request.user.id)  # ตรวจสอบ User ID
        print("Sell Item:", sell_item)

        # ตรวจสอบว่าผู้ใช้งานที่ล็อกอินอยู่เป็น CustomUser
        user = get_object_or_404(CustomUser, id=request.user.id)

        SellItemComment.objects.create(
            sell_item=sell_item,
            user=user,  # ใช้ CustomUser ที่กำหนด
            content=content
        )
        return redirect('sell_item_details', item_id=post_id)

    return redirect('sell_item_details', item_id=post_id)



@login_required
def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(SellItemComment, id=comment_id, sell_item_id=post_id)
    
    # ตรวจสอบสิทธิ์การลบ: เจ้าของโพสต์, เจ้าของความคิดเห็น, หรือแอดมิน
    if request.user == comment.user or request.user == comment.sell_item.user or request.user.is_staff:
        comment.delete()
        return redirect('sell_item_details', item_id=post_id)
    
    return HttpResponseForbidden("คุณไม่มีสิทธิ์ในการลบความคิดเห็นนี้")



@login_required
def delete_donation_comment(request, donation_id, comment_id):
    # ค้นหาความคิดเห็นที่ต้องการลบ
    comment = get_object_or_404(DonationComment, id=comment_id, donation_id=donation_id)

    # ตรวจสอบสิทธิ์การลบ: เจ้าของโพสต์, เจ้าของความคิดเห็น, หรือแอดมิน
    if request.user == comment.user or request.user == comment.donation.user or request.user.is_staff:
        comment.delete()
        messages.success(request, "ความคิดเห็นถูกลบเรียบร้อยแล้ว")
        return redirect('donation_details', donation_id=donation_id)
    
    return HttpResponseForbidden("คุณไม่มีสิทธิ์ในการลบความคิดเห็นนี้")




@login_required
def delete_announcement_comment(request, announcement_id, comment_id):
    # ดึงความคิดเห็นที่ต้องการลบ
    comment = get_object_or_404(GeneralAnnouncementComment, id=comment_id, general_announcement_id=announcement_id)
    
    # ตรวจสอบสิทธิ์การลบ
    if request.user == comment.user or request.user == comment.general_announcement.user or request.user.is_staff:
        comment.delete()
        return redirect('general_announcement_details', announcement_id=announcement_id)
    
    # หากไม่มีสิทธิ์
    return HttpResponseForbidden("คุณไม่มีสิทธิ์ในการลบความคิดเห็นนี้")



