from django import forms
from .models import SellItem, Donation, GeneralAnnouncement
from .models import Comment
class SellItemForm(forms.ModelForm):
    class Meta:
        model = SellItem
        fields = ['user_role', 'title', 'description', 'price', 'location', 'phone', 'image']
       

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['role', 'title', 'description', 'location', 'phone', 'image']
       

class GeneralAnnouncementForm(forms.ModelForm):
    class Meta:
        model = GeneralAnnouncement
        fields = ['title', 'content', 'location', 'image', "phone"]
        

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-pink-500',
                'placeholder': 'เพิ่มความคิดเห็นของคุณ...',
                'rows': 3,
            }),
        }