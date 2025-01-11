from django import forms
from .models import WasteImage, WasteItem

class WasteImageForm(forms.ModelForm):
    class Meta:
        model = WasteImage
        fields = ['image', 'waste_type', 'subtype', 'category', 'separation_method']
        widgets = {
            'waste_type': forms.Select(choices=WasteImage.WASTE_TYPE_CHOICES),
            'category': forms.Select(choices=WasteImage.CATEGORY_CHOICES),
        }


class WasteItemForm(forms.ModelForm):
    class Meta:
        model = WasteItem
        fields = ['barcode', 'brand_name', 'product_name', 'product_image']
