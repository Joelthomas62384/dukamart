from django.shortcuts import render
from . models import *

# Create your views here.


def home(request):
    slider = Slider.objects.all().order_by('-id')[:3]
    banner = Feature.objects.all().order_by('-id')[:3]
    category = Main_Category.objects.all()
    context = {
        "slider":slider,
        'banner':banner,
        'category':category
    }
    return render(request,'home.html', context)