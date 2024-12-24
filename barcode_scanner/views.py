from pyzbar.pyzbar import decode
from PIL import Image
from barcode_generator.models import GeneratedBarcode
from django.shortcuts import render
from django.http import JsonResponse
from barcode_generator.models import GeneratedBarcode
from django.http import HttpResponse

def scan_barcode(request):
    if request.method == 'POST':
        try:
            barcode_image = request.FILES['barcode_image']
            image = Image.open(barcode_image)
            decoded_objects = decode(image)

            if decoded_objects:
                barcode_data = decoded_objects[0].data.decode('utf-8')
                barcode_data = barcode_data[:-1]
                barcode_obj = GeneratedBarcode.objects.get(code=barcode_data)
                return HttpResponse(f'Scanned Barcode: {barcode_obj.code}, Image: <a href="{barcode_obj.image.url}">IMAGE LINK</a>.')
            else:
                return HttpResponse('No barcode found.')
        except Exception as e:
            return HttpResponse(f'Error: {str(e)}', status=500)
    else:
        return render(request, 'barcode_scanner/scan.html')





def scan_camera(request):
    return render(request, 'barcode_scanner/scan_camera.html')

def scan_result(request):
    if request.method == "POST":
        import json
        data = json.loads(request.body)
        barcode_data = data.get("barcode")

        try:
            barcode_obj = GeneratedBarcode.objects.get(code=barcode_data)
            return JsonResponse({"success": True, "message": "Barcode found!", "code": barcode_obj.code})
        except GeneratedBarcode.DoesNotExist:
            return JsonResponse({"success": False, "message": "Barcode not found!"})


def submit_form(request):
    if request.method == "POST":
        barcode = request.POST.get("barcode")
        category = request.POST.get("category")
        description = request.POST.get("description")
        # Logic บันทึกข้อมูลในฐานข้อมูล
        return JsonResponse({"success": True, "message": "บันทึกข้อมูลสำเร็จ"})