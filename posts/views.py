from django.shortcuts import render, redirect
from .models import SellItem  # สมมติว่าคุณมีโมเดลชื่อ SellItem
from .forms import SellItemForm
from .forms import DonationForm
from .models import GeneralAnnouncement
from .forms import GeneralAnnouncementForm  # เพิ่มบรรทัดนี้
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import SellItemForm
from .models import SellItem
from django.views.generic import DeleteView
from .models import SellItem
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import UpdateView, DeleteView
from django.urls import reverse
from django.views.generic import CreateView
from .models import Donation
from .forms import DonationForm  # สมมติว่าคุณมีฟอร์ม DonationForm
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import DonationForm
from .models import Donation
from django.views.generic import DetailView
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from .models import Donation
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import DeleteView
from .models import GeneralAnnouncement

from .models import GeneralAnnouncement
from django.views.generic.edit import DeleteView
from .models import GeneralAnnouncement
from django.views.generic import ListView



def home(request):
    return render(request, 'SeniorProject/home.html')  # ชี้ไปยังตำแหน่งเทมเพลต home.html


def post_ad_view(request):
    # คุณสามารถเพิ่มการจัดการสำหรับการโพสต์โฆษณาที่นี่
    return render(request, 'posts/post_ad.html')  # เปลี่ยนเป็นชื่อ template ที่ต้องการ


def sell_item_all(request):
    # ดึงข้อมูลทั้งหมดจาก SellItem
    items = SellItem.objects.all()
    
    # กรองข้อมูลตามเงื่อนไขจาก URL query parameters
    role = request.GET.get('role')  # รับค่าจากพารามิเตอร์ ?role=buyer หรือ seller
    status = request.GET.get('status')  # รับค่าจากพารามิเตอร์ ?status=open หรือ closed

    if role:
        items = items.filter(user_role=role)

    if status:
        if status == 'open':
            items = items.filter(is_closed=False)
        elif status == 'closed':
            items = items.filter(is_closed=True)
    
    context = {
        'items': items,
        'selected_role': role,
        'selected_status': status,
    }
    
    return render(request, 'posts/sell_item_all.html', context)





class SellItemView(View):
    def get(self, request):
        form = SellItemForm()
        return render(request, 'posts/sell_item.html', {'form': form})

    def post(self, request):
        form = SellItemForm(request.POST, request.FILES)
        if form.is_valid():
            sell_item = form.save(commit=False)
            sell_item.user = request.user
            sell_item.save()
            messages.success(request, 'ลงประกาศขายสำเร็จ')
            return redirect('sell_item_details', item_id=sell_item.id)
        else:
            print(form.errors)  # เพิ่มการพิมพ์ข้อผิดพลาดถ้ามี
            messages.error(request, 'เกิดข้อผิดพลาดในการลงประกาศ')
        return render(request, 'posts/sell_item.html', {'form': form})

class SellItemDetailView(View):
    def get(self, request, item_id):
        post_ad = get_object_or_404(SellItem, id=item_id)
        
        # กำหนดว่า can_edit เป็น True ถ้าผู้ใช้ปัจจุบันเป็นเจ้าของโพสต์หรือแอดมิน
        can_edit = request.user == post_ad.user or request.user.is_staff
        
        context = {
            'post_ad': post_ad,
            'can_edit': can_edit,
        }
        return render(request, 'posts/sell_item_details.html', context)


class SellItemDeleteView(DeleteView):
    model = SellItem
    template_name = 'posts/sell_item_confirm_delete.html'  # หรือชื่อไฟล์ที่เหมาะสม
    success_url = reverse_lazy('sell_item_all')  # หรือ URL ที่คุณต้องการหลังการลบ
    
    
class EditItemView(UserPassesTestMixin, UpdateView):
    model = SellItem
    template_name = 'posts/edit_item.html'
    
    def test_func(self):
        post_ad = self.get_object()
        return self.request.user == post_ad.user or self.request.user.is_staff

class DeleteItemView(UserPassesTestMixin, DeleteView):
    model = SellItem
    template_name = 'posts/sell_item_confirm_delete.html'  # หรือเทมเพลตยืนยันการลบ
    success_url = reverse_lazy('sell_item_all')

    def test_func(self):
        return self.request.user == self.get_object().user or self.request.user.is_staff

    

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
        post_ad = get_object_or_404(SellItem, id=item_id)
        if request.user == post_ad.user or request.user.is_staff:
            post_ad.is_sold = True
            post_ad.save()
        return redirect('sell_item_details', item_id=item_id)
    
    


def donation_all(request):
    role = request.GET.get('role')
    status = request.GET.get('status')

    donations = Donation.objects.all()

    if role:
        donations = donations.filter(role=role)
    if status:
        donations = donations.filter(is_closed=(status == 'closed'))

    context = {
        'donations': donations,
        'selected_role': role,
        'selected_status': status,
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
        
from django.views.generic.edit import UpdateView
from .models import Donation

class DonationDetailView(LoginRequiredMixin, DetailView):
    model = Donation
    template_name = 'posts/donation_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user  # เพิ่ม context ให้ HTML
        return context
    
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
    
    
def announcement_all(request):
    # ดึงข้อมูลการประกาศทั้งหมดจากฐานข้อมูล
    announcements = GeneralAnnouncement.objects.all()  # หรือใช้ .filter() ถ้าต้องการกรองข้อมูล
    return render(request, 'posts/general_announcement_all.html', {'announcements': announcements})



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
            return redirect('general_announcement_detail', pk=general_announcement.id)
        else:
            print(form.errors)  # พิมพ์ข้อผิดพลาดในกรณีที่ฟอร์มไม่ผ่าน
            messages.error(request, 'เกิดข้อผิดพลาดในการลงประกาศ')
        return render(request, 'posts/general_announcement.html', {'form': form})

class GeneralAnnouncementDetailView(DetailView):
    model = GeneralAnnouncement
    template_name = 'posts/general_announcement_detail.html'
    context_object_name = 'announcement'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['request'] = self.request  # ส่ง request ไปยังเทมเพลต
        return context
    
class GeneralAnnouncementUpdateView(UpdateView):
    model = GeneralAnnouncement
    fields = ['title', 'content', 'location', 'image']
    template_name = 'posts/edit_general_announcement.html'
    success_url = reverse_lazy('general_announcement_all')  # เปลี่ยน URL นี้เป็น URL ที่คุณต้องการเปลี่ยนเส้นทาง

    # หรือใช้ dynamic success URL
    def get_success_url(self):
        return reverse_lazy('general_announcement_detail', kwargs={'pk': self.object.pk})
    
    

    
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from .models import GeneralAnnouncement

from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from .models import GeneralAnnouncement
from django.shortcuts import get_object_or_404, redirect

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
    
    
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db import models  # เพิ่มการนำเข้า models สำหรับ Value และ CharField
from .models import GeneralAnnouncement, SellItem, Donation

User = get_user_model()  # ดึงโมเดล User ที่กำหนดเอง (ถ้ามี)

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
