from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from functools import reduce
from operator import or_
from collections import defaultdict

from .models import WasteItem, WasteImage
from .forms import WasteItemForm
from posts.models import SellItem
from barcode_generator.models import GeneratedBarcode
from pyzbar.pyzbar import decode
from PIL import Image


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



def add_waste_item(request):
    barcode = request.GET.get('barcode', None)  # ดึงข้อมูลบาร์โค้ดจาก URL
    
    if request.method == 'POST':
        item_form = WasteItemForm(request.POST, request.FILES)
        if item_form.is_valid():
            # สร้าง WasteItem ใหม่
            waste_item = item_form.save(commit=False)
            waste_item.created_by = request.user
            waste_item.save()

            # บันทึกข้อมูล WasteImage
            for key in request.POST:
                if key.startswith('waste_type-'):
                    index = key.split('-')[1]
                    waste_type = request.POST.get(f'waste_type-{index}')
                    subtype = request.POST.get(f'subtype-{index}')
                    category = request.POST.get(f'category-{index}')
                    separation_method = request.POST.get(f'separation_method-{index}')
                    image_file = request.FILES.get(f'images-{index}')

                    if waste_type or category or image_file:
                        # สร้าง WasteImage
                        waste_image = WasteImage.objects.create(
                            waste_type=waste_type,
                            subtype=subtype,
                            category=category,
                            separation_method=separation_method,
                            image=image_file,
                            added_by=request.user,
                            waste_item=waste_item  # เชื่อมโยง WasteItem
                        )
                        waste_item.images.add(waste_image)

            # Redirect ไปยังหน้า Waste Item Detail หลังจากบันทึกเสร็จ
            return redirect('barcode_scanner:waste_item_detail', pk=waste_item.pk)

    else:
          item_form = WasteItemForm(initial={'barcode': barcode})

    return render(request, 'barcode_scanner/form.html', {'form': item_form, 'barcode': barcode})



def handle_barcode_member(request):
    # รับค่าบาร์โค้ดจาก GET parameter
    barcode = request.GET.get('barcode', '').strip()

    if barcode:
        try:
            # ตรวจสอบว่ามี WasteItem ในฐานข้อมูลหรือไม่
            waste_item = WasteItem.objects.get(barcode=barcode)
            # หากเจอข้อมูล ให้ไปที่ waste_item_detail
            return redirect('barcode_scanner:waste_item_detail', pk=waste_item.pk)
        except WasteItem.DoesNotExist:
            # ถ้าไม่มีข้อมูล ให้ไปยัง add_waste_item เพื่อเพิ่มข้อมูล
            return redirect(f"{reverse('barcode_scanner:add_waste_item')}?barcode={barcode}")
    else:
        # ถ้าไม่มีบาร์โค้ด ให้ redirect กลับไปยังหน้าสแกน
        return redirect('barcode_scanner:scan_camera')



@login_required
def add_waste_detail(request, barcode):
    # Query WasteItem จาก barcode
    waste_item = get_object_or_404(WasteItem, barcode=barcode)

    if request.method == 'POST':
        waste_type = request.POST.get('waste_type')
        subtype = request.POST.get('subtype')
        category = request.POST.get('category')
        separation_method = request.POST.get('separation_method')
        image_file = request.FILES.get('image')

        if waste_type and category:  # ตรวจสอบข้อมูลที่จำเป็น
            waste_image = WasteImage.objects.create(
                waste_type=waste_type,
                subtype=subtype,
                category=category,
                separation_method=separation_method,
                image=image_file,
                added_by=request.user,
                waste_item=waste_item  # เชื่อมโยงกับ WasteItem
            )
            waste_item.images.add(waste_image)  # เชื่อมโยง ManyToMany
            return redirect('barcode_scanner:my_waste_details')
        else:
            error_message = "กรุณากรอกข้อมูลให้ครบถ้วน"
            return render(request, 'barcode_scanner/add_waste_detail.html', {
                'barcode': barcode,
                'waste_item': waste_item,
                'error_message': error_message
            })

    return render(request, 'barcode_scanner/add_waste_detail.html', {
        'barcode': barcode,
        'waste_item': waste_item
    })



def waste_item_detail(request, pk):
    waste_item = get_object_or_404(WasteItem, pk=pk)

    # เตรียมข้อมูลสำหรับ Template
    images_with_related_buyers = []
    for image in waste_item.images.all():
        waste_types = [image.waste_type] if image.waste_type else []
        subtypes = [image.subtype] if image.subtype else []

        query = Q()
        for value in waste_types + subtypes:
            query |= Q(title__icontains=value) | Q(description__icontains=value)

        related_buyers = SellItem.objects.filter(
            post_type='buy'
        ).filter(query).distinct()

        images_with_related_buyers.append({
            'image': image,
            
            'related_buyers': related_buyers,
        })

    return render(request, 'barcode_scanner/waste_item_detail.html', {
        'waste_item': waste_item,
        'images_with_related_buyers': images_with_related_buyers,
    })



@csrf_exempt
@login_required
def vote_correct(request, image_id):
    if request.method == 'POST':
        image = get_object_or_404(WasteImage, id=image_id)
        if request.user in image.correct_votes.all():
            image.correct_votes.remove(request.user)
        else:
            image.correct_votes.add(request.user)
            image.incorrect_votes.remove(request.user)
        return JsonResponse({
            'status': 'success',
            'total_correct': image.total_correct_votes(),
            'total_incorrect': image.total_incorrect_votes(),
        })


@csrf_exempt
@login_required
def vote_incorrect(request, image_id):
    if request.method == 'POST':
        image = get_object_or_404(WasteImage, id=image_id)
        if request.user in image.incorrect_votes.all():
            image.incorrect_votes.remove(request.user)
        else:
            image.incorrect_votes.add(request.user)
            image.correct_votes.remove(request.user)
        return JsonResponse({
            'status': 'success',
            'total_correct': image.total_correct_votes(),
            'total_incorrect': image.total_incorrect_votes(),
        })


@login_required
def update_votes(request, image_id):
    image = get_object_or_404(WasteImage, id=image_id)

    # ส่งข้อมูลจำนวนโหวตกลับในรูปแบบ JSON
    data = {
        'total_correct': image.total_correct_votes(),
        'total_incorrect': image.total_incorrect_votes(),
    }
    return JsonResponse(data)



@login_required
def all_barcodes(request):
    waste_items = WasteItem.objects.all()
    return render(request, 'barcode_scanner/all_barcode.html', {'waste_items': waste_items})



@login_required
def my_waste_details(request):
    waste_images = WasteImage.objects.all().order_by('waste_item__barcode')
    return render(request, 'barcode_scanner/my_waste_details.html', {'waste_images': waste_images})




@login_required
def delete_waste_item(request, pk):
    waste_item = get_object_or_404(WasteItem, pk=pk)  # ตรวจสอบว่ามี WasteItem นี้อยู่ในฐานข้อมูล
    if request.method == 'POST':
        waste_item.delete()  # ลบรายการ
    return redirect('barcode_scanner:all_barcodes')  # เปลี่ยนเส้นทางกลับไปยังหน้ารายการบาร์โค้ดทั้งหมด



@login_required
def delete_waste_image(request, pk):
    waste_image = get_object_or_404(WasteImage, pk=pk)

    # ตรวจสอบว่าผู้ใช้ที่ลบเป็นเจ้าของหรือไม่
    if waste_image.added_by == request.user:
        waste_image.delete()
        # เพิ่มข้อความแจ้งเตือนถ้าต้องการ
    return redirect('barcode_scanner:my_waste_details')  # กลับไปที่หน้าการแยกขยะของฉัน



# สำหรับคนยังไม่สมาชิก

def scan_camera_guest(request):
    return render(request, 'barcode_scanner/scan_camera_guest.html')

   

def handle_barcode_guest(request):
    """
    จัดการทั้งการค้นหาและการสแกนบาร์โค้ด
    """
    # รับค่าบาร์โค้ดจาก GET parameter
    barcode = request.GET.get('barcode', '').strip()

    if barcode:
        try:
            # ดึง WasteItem โดยใช้บาร์โค้ด
            waste_item = WasteItem.objects.get(barcode=barcode)

            # เตรียมข้อมูลสำหรับ Template พร้อมข้อมูลคนรับซื้อ
            images_with_related_buyers = []
            for image in waste_item.images.all():
                waste_types = [image.waste_type] if image.waste_type else []
                subtypes = [image.subtype] if image.subtype else []

                query = Q()
                for value in waste_types + subtypes:
                    query |= Q(title__icontains=value) | Q(description__icontains=value)

                # ค้นหา SellItem (คนรับซื้อ) ที่เกี่ยวข้อง
                related_buyers = SellItem.objects.filter(
                    post_type='buy'
                ).filter(query).distinct()

                images_with_related_buyers.append({
                    'image': image,
                    'related_buyers': related_buyers,
                })

            # หากเจอข้อมูล ให้แสดงรายละเอียดในหน้า waste_item_detail_guest.html
            return render(request, 'barcode_scanner/waste_item_detail_guest.html', {
                'waste_item': waste_item,
                'images_with_related_buyers': images_with_related_buyers,
            })

        except WasteItem.DoesNotExist:
            # ถ้าไม่เจอข้อมูล ให้แสดงข้อความใน guest_popup.html
            return render(request, 'barcode_scanner/guest_popup.html', {
                'barcode': barcode,
                'message': 'ไม่มีข้อมูลสำหรับบาร์โค้ดนี้ในฐานข้อมูล',
            })

    # หากไม่มีการส่งบาร์โค้ดหรือข้อมูลไม่ครบ ให้ Redirect กลับไปยังหน้ากล้อง
    return redirect('scanner:scan_camera_guest')
