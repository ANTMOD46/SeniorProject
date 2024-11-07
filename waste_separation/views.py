from django.shortcuts import render

def separate_waste(request):
    return render(request, 'waste_separation/separate_waste.html')  # สร้างไฟล์เทมเพลตนี้ในโฟลเดอร์ templates
