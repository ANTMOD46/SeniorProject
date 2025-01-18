from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm  # นำเข้าฟอร์มที่สร้างขึ้น
from django.contrib.auth import login,authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProfileUpdateForm  # ฟอร์มสำหรับอัปเดตโปรไฟล์
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ProfileUpdateForm

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
    # การจัดการข้อมูลที่ใช้สำหรับแก้ไขโปรไฟล์
    return render(request, 'accounts/profile_edit.html')  # เปลี่ยนเป็นชื่อ template ที่ต้องการ




class CustomLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')  # เปลี่ยน 'home' เป็น URL ที่คุณต้องการ

    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')
    
    
@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # ตรวจสอบว่า 'profile' มีใน urls.py
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'accounts/profile_edit.html', {'form': form})


@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {'user': request.user})



from django.shortcuts import render
from .models import CustomUser

def admin_member_list(request):
    # ดึงข้อมูลสมาชิกทั้งหมด
    members = CustomUser.objects.all()
    return render(request, 'accounts/admin_member_list.html', {'members': members})




from django.shortcuts import get_object_or_404, render
from .models import CustomUser

def view_member_detail(request, member_id):
    member = get_object_or_404(CustomUser, id=member_id)
    return render(request, 'accounts/view_member_detail.html', {'member': member})


from django.shortcuts import get_object_or_404, redirect
from .models import CustomUser

def delete_member(request, member_id):
    member = get_object_or_404(CustomUser, id=member_id)
    member.delete()
    return redirect('accounts/admin_member_list')  # กลับไปยังหน้ารายชื่อสมาชิก



from django.shortcuts import render
from barcode_scanner.models import WasteImage

from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from barcode_scanner.models import WasteImage
from django.contrib.auth.decorators import login_required

@login_required
def my_waste_details(request):
    # ดึงเฉพาะ WasteImage ที่เชื่อมโยงกับ waste_item และผู้ใช้งานคนปัจจุบันเพิ่ม
    user_waste_images = WasteImage.objects.filter(added_by=request.user, waste_item__isnull=False)
    return render(request, 'barcode_scanner/my_waste_details.html', {'waste_images': user_waste_images})

