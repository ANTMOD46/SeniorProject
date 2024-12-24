import io
from django.http import HttpResponse
from barcode import Code39
from barcode.writer import ImageWriter
from .models import GeneratedBarcode

def generate_barcode(request, code):
    code_obj = Code39(code, writer=ImageWriter())
    buffer = io.BytesIO()
    code_obj.write(buffer)
    buffer.seek(0)

    barcode_obj, created = GeneratedBarcode.objects.get_or_create(code=code)
    if created:
        barcode_obj.image.save(f'{code}.png', buffer, save=True)
        action = "created"
    else:
        action = "fetched"

    return HttpResponse(f'Barcode "{code}" {action} successfully! <a href="{barcode_obj.image.url}">IMAGE LINK</a>')
