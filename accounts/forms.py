from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User  # ใช้ User Model
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser  # ถ้าใช้ User Model ที่ปรับแต่งเอง
        fields = ('first_name', 'last_name', 'address', 'phone_number', 'email', 'username', 'password1', 'password2', 'profile_picture')


from django import forms
from .models import CustomUser

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email',  'phone_number', 'address', 'profile_picture']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'w-full p-3 border border-gray-300 rounded-lg'}),
            'email': forms.EmailInput(attrs={'class': 'w-full p-3 border border-gray-300 rounded-lg'}),
            'first_name': forms.TextInput(attrs={'class': 'w-full p-3 border border-gray-300 rounded-lg'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full p-3 border border-gray-300 rounded-lg'}),
            'phone_number': forms.TextInput(attrs={'class': 'w-full p-3 border border-gray-300 rounded-lg'}),
            'address': forms.Textarea(attrs={'class': 'w-full p-3 border border-gray-300 rounded-lg', 'rows': 3}),
            'profile_picture': forms.FileInput(attrs={'class': 'w-full p-3 border border-gray-300 rounded-lg'}),
        }



# from django import forms
# from .models import CustomUser

# class MemberForm(forms.ModelForm):
#     class Meta:
#         model = CustomUser
#         fields = ['username', 'first_name', 'last_name', 'email', ]  # เพิ่มฟิลด์ตามต้องการ
