# barcode_scanner/forms.py
from django import forms
from django.forms import inlineformset_factory
from .models import WasteItem, WasteImage

class WasteItemForm(forms.ModelForm):
    class Meta:
        model = WasteItem
        fields = [
            'barcode',
            'brand_name',
            'product_name',
            'waste_type',
            'subtype',
            'category',
            'separation_method',
            'product_image',
            
        ]
        widgets = {
            'waste_type': forms.Select(),
            'subtype': forms.TextInput(attrs={'placeholder': 'เช่น พลาสติกแข็ง PET'}),
            'category': forms.Select(),
            'separation_method': forms.Textarea(attrs={'rows': 4}),
        }



WasteImageFormSet = inlineformset_factory(
    WasteItem,
    WasteItem.images.through,  # ใช้ through model สำหรับ ManyToManyField
    fields=('wasteimage',),
    extra=1,
    can_delete=True
)
