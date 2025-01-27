from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View
from .forms import CustomUserCreationForm, ProfileEditForm  # รวมฟอร์มที่ใช้
from .models import CustomUser


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)  # อย่าลืมเพิ่ม request.FILES สำหรับไฟล์รูป
        if form.is_valid():
            user = form.save()
            login(request, user)  # ล็อกอินอัตโนมัติหลังจากสมัครสมาชิก
            return redirect('login')  # เปลี่ยนเส้นทางไปยังหน้า Home
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home_user')  # เปลี่ยนเส้นทางไปที่ home_user
        else:
            error_message = 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง'
            return render(request, 'accounts/login.html', {'error_message': error_message})
    else:
        return render(request, 'accounts/login.html')
    
    
@login_required
def home_user(request):
    return render(request, 'accounts/home_user.html')  # ตรวจสอบให้แน่ใจว่าใช้ template ที่ถูกต้อง


@login_required
def profile_edit(request):
    user = request.user  # ผู้ใช้ปัจจุบัน

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'บันทึกข้อมูลโปรไฟล์เรียบร้อยแล้ว')
            return redirect('home_user')  # เปลี่ยนเส้นทางกลับไปยังหน้าหลัก
        else:
            messages.error(request, 'เกิดข้อผิดพลาด กรุณาตรวจสอบข้อมูล')
    else:
        form = ProfileEditForm(instance=user)  # โหลดข้อมูลเดิมมาแสดงในฟอร์ม

    return render(request, 'accounts/profile_edit.html', {'form': form})


class CustomLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')  # เปลี่ยน 'home' เป็น URL ที่คุณต้องการ

    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')
    

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {'user': request.user})


def admin_member_list(request):
    # ดึงข้อมูลสมาชิกทั้งหมด
    members = CustomUser.objects.all()
    return render(request, 'accounts/admin_member_list.html', {'members': members})



def view_member_detail(request, member_id):
    member = get_object_or_404(CustomUser, id=member_id)
    return render(request, 'accounts/view_member_detail.html', {'member': member})



def delete_member(request, member_id):
    member = get_object_or_404(CustomUser, id=member_id)
    member.delete()
    return redirect('accounts/admin_member_list')  # กลับไปยังหน้ารายชื่อสมาชิก



