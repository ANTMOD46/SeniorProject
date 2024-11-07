from django import forms
from .models import SellItem, Donation, GeneralAnnouncement

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
        fields = ['title', 'content', 'location', 'image']
        
