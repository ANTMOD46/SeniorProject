from django.shortcuts import render

def home(request):
    return render(request, 'SeniorProject/home.html')  # ชี้ไปยังตำแหน่งเทมเพลต home.html
