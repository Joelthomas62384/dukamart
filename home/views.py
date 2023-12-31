from django.shortcuts import render,redirect
from django.http import JsonResponse
from . models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
import json
from django.template.loader import render_to_string
from functools import reduce
from math import ceil





# Create your views here.
slider = Slider.objects.all().order_by('-id')[:3]
banner = Feature.objects.all().order_by('-id')[:3]
category = Main_Category.objects.all()
product = Product.objects.all()
context = {
    "slider":slider,
    'banner':banner,
    'category':category,
    'product':product,
}




def home(request):
   

    return render(request,'home.html', context)

def product_detail(request,slug):
    product = Product.objects.get(slug=slug)
    context = {
        'product':product,
    }
    return render(request,'product-details.html', context)

def register_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if len(password)<4:
            messages.warning(request,"Password must be at least 4 characters")
            return redirect("register_page")
        if User.objects.filter(username=username , email=email).exists:
            messages.warning(request,"User already exists")
            return redirect("register_page")
        user = User(username=username, email=email, password=password)
        user.save()
        messages.success(request,f"User {username} Created Successfully")
        return redirect("register_page")

    return render(request,'registerPage.html',context)


def login_page(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:

            login(request,user)
            messages.success(request,"Login successful")
            return redirect("home")
        else:
            messages.warning(request,"Invalid Credentials")

    return render(request,"registerPage.html",context)

    
def logout_user(request):
    logout(request)
    messages.success(request,"logout successful")
    return redirect("home")
    
    
    
def category_wise(request):
    product = Product.objects.all()
    category = Category.objects.all()
    context = { "products": product, "category": category    }
    return render(request, "product-view.html", context)

    
    
    
    
    
    
    
    
    
    

def user_validate(request,username,field):
    if field == "email":

        if User.objects.filter(email=username).exists():
            return JsonResponse({"status":False, "message":"Email already Exists"})
        else:
            return JsonResponse({"status":True})
    else:
        if User.objects.filter(username=username).exists():
            return JsonResponse({"status":False, "message":"User name already Exists"})
        else:
            return JsonResponse({"status":True})
    


def filter_category(request):
    product = Product.objects.all()
    not_found = False

    if request.method == 'POST':
        try:
            # Assuming the JSON payload contains an array named 'categories'
            json_data = json.loads(request.body.decode('utf-8'))
            selected_categories = json_data.get('categories', [])
            product = Product.objects.filter(category__id__in=selected_categories).distinct()
            not_found = False
            if len(product)<1:
                not_found = True
            if len(selected_categories)<1:
                product = Product.objects.all()
                not_found = False
        except json.JSONDecodeError as e:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

    context = {"products": product,"not_found": not_found}

    data = render_to_string("includes/ajax/productAjax.html", context)


    return JsonResponse({"data": data})


def cart_page(request):
    cart = Cart.objects.filter(user=request.user)

    calculate_item_price = lambda x: (x.product.price * (x.product.discount / 100) ) * x.amount
    
    total_price = reduce(lambda acc, item: acc + calculate_item_price(item), cart,0)

    print(total_price)



   
    context["carts"]=cart
    context['total_price']=ceil(total_price)
    
    return render(request,"cart.html",context)



def cart_minus(request,id):
    cart = Cart.objects.filter(id=id)
    if cart.amount == 0:
        cart.amount = 0
    else:
        cart.amount -= 1
    cart.save()

    return JsonResponse({'status':'success'})

def cart_add(request,id):
    cart = Cart.objects.filter(id=id)
    cart.amount += 1
    cart.save()
    
    return JsonResponse({'status':'success'})