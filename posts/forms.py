from django import forms
from .models import SellItem, Donation, GeneralAnnouncement



class SellItemForm(forms.ModelForm):
    class Meta:
        model = SellItem
        fields = ['title', 'description', 'price', 'post_type', 'image','location','phone']
        widgets = {
            'post_type': forms.Select(choices=SellItem.POST_TYPE_CHOICES),
        }
       

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['role', 'title', 'description', 'location', 'phone', 'image']
       

class GeneralAnnouncementForm(forms.ModelForm):
    class Meta:
        model = GeneralAnnouncement
        fields = ['title', 'content', 'location', 'image',]
        


from django import forms
from .models import SellItemComment

class SellItemCommentForm(forms.ModelForm):
    class Meta:
        model = SellItemComment
        fields = ['content']

from django import forms
from .models import DonationComment

class DonationCommentForm(forms.ModelForm):
    class Meta:
        model = DonationComment
        fields = ['content']

from django import forms
from .models import GeneralAnnouncementComment

class GeneralAnnouncementCommentForm(forms.ModelForm):
    class Meta:
        model = GeneralAnnouncementComment
        fields = ['content']
