from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User  # ใช้ User Model
from .models import CustomUser, UserProfile  # โมเดล CustomUser และ UserProfile

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser  # ถ้าใช้ User Model ที่ปรับแต่งเอง
        fields = ('first_name', 'last_name', 'address', 'phone_number', 'email', 'username', 'password1', 'password2', 'profile_picture')


class ProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=False)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'profile_picture']

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields['username'].disabled = True  # Username ไม่สามารถแก้ไขได้

    def save(self, commit=True):
        user = super(ProfileUpdateForm, self).save(commit=False)
        user_profile = user.profile  # ใช้ related_name ที่กำหนดไว้ใน UserProfile
        user_profile.phone_number = self.cleaned_data['phone_number']
        user_profile.address = self.cleaned_data['address']
        if commit:
            user.save()
            user_profile.save()
        return user
