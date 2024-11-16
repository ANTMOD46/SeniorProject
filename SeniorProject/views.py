from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'SeniorProject/home.html', {'title': 'หน้าหลัก'})


from django.shortcuts import render

def recycle_view(request):
    return render(request, 'SeniorProject/recycle.html')

def organic_view(request):
    return render(request, 'SeniorProject/organic.html', {'title': 'ขยะเปียก'})

def general_view(request):
    return render(request, 'SeniorProject/general.html', {'title': 'ขยะทั่วไป'})

def hazardous_view(request):
    return render(request, 'SeniorProject/hazardous.html', {'title': 'ขยะอันตราย'})




