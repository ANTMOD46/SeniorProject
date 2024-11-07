from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'SeniorProject/home.html', {'title': 'หน้าหลัก'})


def recycle_view(request):
    return render(request, 'recycle.html', {'title': 'ขยะรีไซเคิล'})

def organic_view(request):
    return render(request, 'organic.html', {'title': 'ขยะเปียก'})

def general_view(request):
    return render(request, 'general.html', {'title': 'ขยะทั่วไป'})

def hazardous_view(request):
    return render(request, 'hazardous.html', {'title': 'ขยะอันตราย'})




