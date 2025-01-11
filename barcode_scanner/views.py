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


from django.shortcuts import render

def form_view(request):
    barcode = request.GET.get('barcode')  # ดึงบาร์โค้ดจาก query string
    return render(request, 'barcode_scanner/form.html', {'barcode': barcode})



def scan_camera(request):
    return render(request, 'barcode_scanner/scan_camera.html')

from django.shortcuts import render, redirect
from .models import WasteItem



def scan_result(request):
    barcode_data = request.GET.get("barcode", None)

    if barcode_data:
        # ค้นหาข้อมูลในฐานข้อมูลที่ตรงกับ barcode
        try:
            waste_item = WasteItem.objects.get(barcode=barcode_data)
            # ถ้ามีข้อมูลแล้ว จะส่งข้อมูลไปยังฟอร์มเพื่อแสดงให้ผู้ใช้
            return render(request, 'barcode_scanner/form.html', {'waste_item': waste_item})
        except WasteItem.DoesNotExist:
            # ถ้าไม่พบข้อมูล ให้แสดงฟอร์มให้กรอกข้อมูลใหม่
            return render(request, 'barcode_scanner/form.html', {'barcode': barcode_data})
    else:
        # ถ้าไม่มี barcode ที่กำหนด
        return redirect('scanner:scan_barcode')



from django.shortcuts import render, redirect
from .forms import WasteItemForm
from .models import WasteItem, WasteImage

def submit_form(request):
    if request.method == 'POST':
        form = WasteItemForm(request.POST, request.FILES)
        if form.is_valid():
            waste_item = form.save(commit=False)
            waste_item.save()  # บันทึกข้อมูล WasteItem
            # บันทึกภาพผลิตภัณฑ์
            if 'product_image' in request.FILES:
                product_image = WasteImage.objects.create(image=request.FILES['product_image'])
                waste_item.product_image.add(product_image)
            # บันทึกภาพขยะ
            if 'waste_image' in request.FILES:
                waste_image = WasteImage.objects.create(image=request.FILES['waste_image'])
                waste_item.waste_image.add(waste_image)
            return redirect('success_url')  # แสดงหน้าสำเร็จ
    else:
        form = WasteItemForm()
    return render(request, 'scanner/form.html', {'form': form})


def submit_product_info(request):
    if request.method == 'POST':
        barcode = request.POST.get('barcode')
        product_name = request.POST.get('product_name')
        product_category = request.POST.get('product_category')
        product_description = request.POST.get('product_description')

        # สร้างหรืออัปเดตข้อมูลสินค้า
        product = WasteItemForm.objects.create(
            barcode=barcode,
            product_name=product_name,
            product_category=product_category,
            product_description=product_description
        )
        return redirect('success')  # ปรับ URL ที่ต้องการไปต่อหลังจากบันทึกสำเร็จ

    return HttpResponse("Bad Request", status=400)

from django.shortcuts import render, redirect, get_object_or_404
from .models import WasteItem
from .forms import WasteItemForm

from .models import WasteImage

from .models import WasteItem, WasteImage

from .models import WasteItem, WasteImage
from .forms import WasteItemForm

from django.shortcuts import render, redirect
from .models import WasteItem, WasteImage
from .forms import WasteItemForm

from django.shortcuts import render, redirect, get_object_or_404
from .forms import WasteItemForm
from .models import WasteItem, WasteImage

from django.shortcuts import render, redirect
from .forms import WasteItemForm
from .models import WasteItem, WasteImage

def add_waste_item(request):
    barcode = request.GET.get('barcode', None)  # Fetch barcode from query parameter

    if request.method == 'POST':
        form = WasteItemForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the main WasteItem
            waste_item = form.save()

            # Save additional waste details
            for key in request.POST:
                if key.startswith('waste_type-'):
                    index = key.split('-')[1]
                    waste_type = request.POST.get(f'waste_type-{index}')
                    subtype = request.POST.get(f'subtype-{index}')
                    category = request.POST.get(f'category-{index}')
                    separation_method = request.POST.get(f'separation_method-{index}')

                    if waste_type or subtype or category or separation_method:
                        # Create WasteImage instance
                        waste_image = WasteImage.objects.create(
                            waste_type=waste_type,
                            subtype=subtype,
                            category=category,
                            separation_method=separation_method
                        )

                        # Add uploaded images
                        if f'images-{index}' in request.FILES:
                            for image_file in request.FILES.getlist(f'images-{index}'):
                                waste_image.image.save(image_file.name, image_file)

                        # Associate WasteImage with WasteItem
                        waste_item.images.add(waste_image)

            waste_item.save()
            return redirect('barcode_scanner:waste_item_detail', pk=waste_item.pk)
    else:
        # Pre-fill form with barcode if available
        form = WasteItemForm(initial={'barcode': barcode})

    return render(request, 'barcode_scanner/form.html', {'form': form, 'barcode': barcode})





def waste_item_detail(request, pk):
    waste_item = get_object_or_404(WasteItem, pk=pk)
    return render(request, 'barcode_scanner/waste_item_detail.html', {'waste_item': waste_item})






from django.shortcuts import render

def success(request):
    return render(request, 'barcode_scanner/success.html', {'message': 'บันทึกข้อมูลสำเร็จ!'})





def search_waste_item(request):
    barcode = request.GET.get('barcode', None)
    if barcode:
        if not re.match(r'^\d{13}$', barcode):
            # ถ้ารหัสบาร์โค้ดไม่ถูกต้อง ให้แสดงหน้าผลลัพธ์ไม่พบข้อมูล
            return render(request, 'barcode_scanner/search_result.html', {'barcode': barcode, 'error': True})
        try:
            waste_item = WasteItem.objects.get(barcode=barcode)
            # ถ้ามีข้อมูลแสดงรายละเอียด
            return render(request, 'barcode_scanner/waste_item_detail.html', {'waste_item': waste_item})
        except WasteItem.DoesNotExist:
            # ถ้าไม่พบข้อมูล แสดงหน้าผลลัพธ์ที่แจ้งว่าพบปัญหาในการค้นหา
            return render(request, 'barcode_scanner/search_result.html', {'barcode': barcode, 'error': True})
    return redirect('add_waste_item')



from django.shortcuts import redirect, get_object_or_404
from .models import WasteItem

def scan_barcode_redirect(request):
    barcode = request.GET.get('barcode', None)

    if barcode:
        try:
            # ตรวจสอบว่ามีบาร์โค้ดในฐานข้อมูลหรือไม่
            waste_item = WasteItem.objects.get(barcode=barcode)
            # หากเจอ ให้ redirect ไปยัง waste_item_detail
            return redirect('barcode_scanner:waste_item_detail', pk=waste_item.pk)
        except WasteItem.DoesNotExist:
            # หากไม่เจอ ให้ redirect ไปยัง add_waste_item พร้อม query string
            return redirect(f'/scanner/add/?barcode={barcode}')
    else:
        # หากไม่มีบาร์โค้ดใน query string ให้ redirect กลับไปยังหน้า scan
        return redirect('barcode_scanner:scan_barcode_redirect')

