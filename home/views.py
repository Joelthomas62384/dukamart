from django.shortcuts import render
from . models import *

# Create your views here.


def home(request):
    slider = Slider.objects.all().order_by('-id')[:3]
    banner = Feature.objects.all().order_by('-id')[:3]
    context = {
        "slider":slider,
        'banner':banner
    }
    return render(request,'home.html', context)