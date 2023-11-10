from django.shortcuts import render


def index(request):
    return render(request , 'index.html')

def ads(request):
    return render(request , 'ads.html')