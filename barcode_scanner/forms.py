# barcode_scanner/forms.py
from django import forms
from django.forms import inlineformset_factory
from .models import WasteItem, WasteImage

from django import forms
from .models import WasteItem

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




WasteImageFormSet = inlineformset_factory(
    WasteItem,
    WasteItem.images.through,  # ใช้ through model สำหรับ ManyToManyField
    fields=('wasteimage',),
    extra=1,
    can_delete=True
)
