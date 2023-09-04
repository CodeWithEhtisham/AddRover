from django.shortcuts import render


def dashboard(request):
    return render(request , 'index-3.html')