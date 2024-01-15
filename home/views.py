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
import razorpay
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.decorators import login_required





# We create some of the model objects globally to avoid the rewriting of them
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
    context['cart_count'] = Cart.objects.filter(user=request.user)
    return render(request,'home.html', context)

def product_detail(request,slug):
    product = Product.objects.get(slug=slug)
    print(request.path)
    comments = Comments.objects.filter(product=product).order_by('-verified','-id')
    context = {
        'product':product,
     
        'comments':comments
    }
    context['cart_count'] = Cart.objects.filter(user=request.user)
    try:
        context['cart'] = Cart.objects.get(user=request.user,product=product)
    except:
        context['cart'] = 0 


    return render(request,'product-details.html', context)

def register_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        if len(password)<4:
            messages.warning(request,"Password must be at least 4 characters")
            return redirect("register_page")
        if User.objects.filter(username=username , email=email).exists():
            messages.warning(request,"User already exists")
            return redirect("register_page")
        user = User(username=username, email=email,)
        user.set_password(password)
        user.save()
        useraddress = UserAddress(user=user, address=address,phone=phone)
        useraddress.save()
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

@login_required(login_url='login_page')   
def logout_user(request):
    logout(request)
    messages.success(request,"logout successful")
    return redirect("home")
    
    
    
def category_wise(request):
    product = Product.objects.all()
    category = Category.objects.all()
    context = { "products": product, "category": category  ,
    }
    context['cart_count'] = Cart.objects.filter(user=request.user)

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
            return JsonResponse({"error": "Invalid JSON data"}, status=404)

    context = {"products": product,"not_found": not_found}

    data = render_to_string("includes/ajax/productAjax.html", context)


    return JsonResponse({"data": data})

@login_required(login_url='login_page')   

def cart_page(request):
    try:
        cart = Cart.objects.filter(user=request.user)
    except:
        cart = []

    calculate_item_price = lambda x: round((x.product.price * (x.product.discount / 100) ) * x.amount,2 )
    
    total_price = reduce(lambda acc, item: acc + calculate_item_price(item), cart,0)
    context["carts"]=cart
    context['total_price']=total_price
    context['cart_count'] = Cart.objects.filter(user=request.user)
    
    return render(request,"cart.html",context)


@login_required(login_url='login_page')   

def cart_minus(request,id):
    cart = Cart.objects.get(product__id=id,user=request.user)
    if cart.amount == 0:
        cart.amount = 0
    else:
        cart.amount -= 1
    cart.save()

    return JsonResponse({'status':'success','count':Cart.objects.filter(user=request.user).count()})
@login_required(login_url='login_page')   

def cart_add(request,id):
    cart = Cart.objects.filter(product__id=id,user=request.user).first()
    if cart is None:
        cart = Cart(user=request.user,product=Product.objects.get(id=id),amount=1)
        
    else:
        cart.amount += 1
    # print(cart.amount)
    cart.save()
    
    
    return JsonResponse({'status':'success','count':Cart.objects.filter(user=request.user).count()})

@login_required(login_url='login_page')   

def cart_remove(request,id):
    cart_id = Cart.objects.get(id=id,user=request.user)

    cart_id.delete()
    cart = Cart.objects.filter(user=request.user)
    calculate_item_price = lambda x: round((x.product.price * (x.product.discount / 100) ) * x.amount,2 )
    
    total_price = reduce(lambda acc, item: acc + calculate_item_price(item), cart,0)
    return JsonResponse({'status':'success',"data":total_price,'count':Cart.objects.filter(user=request.user).count()})



@login_required(login_url='login_page')   

def checkout(request):
    cart = Cart.objects.filter(user=request.user, amount__gt=0)
    
    if not cart.exists():
        return redirect('cart_page')
    
    calculate_item_price = lambda x: round((x.product.price * (x.product.discount / 100)) * x.amount, 2)
    
    total_price = reduce(lambda acc, item: acc + calculate_item_price(item), cart, 0)
    client = razorpay.Client(auth=(settings.KEY, settings.SECRET))
    
    # Check if an order already exists with the same criteria
    existing_order = Orders.objects.filter(
        user=request.user,
        address=request.user.user_address.address,
        phone=request.user.user_address.phone,
        total_price=total_price,
        is_paid=False
    ).first()

    if existing_order:
        order = existing_order
    else:
        # Create a new order instance
        order = Orders(user=request.user, address=request.user.user_address.address, phone=request.user.user_address.phone, total_price=total_price)
        order.save()

        # Create a list of OrderProducts instances
        order_products_list = [
            OrderProducts(order=order, product=cart_item.product, total=cart_item.amount)
            for cart_item in cart
        ]

        # Bulk create the OrderProducts instances
        OrderProducts.objects.bulk_create(order_products_list)

    # Mark the order as paid
    order.save()

    # Clear the user's cart
    

    # Redirect or do whatever you need after a successful checkout

    # Now, order object is created, and you can associate the Razorpay order ID
    payment = client.order.create({'amount': total_price * 100, 'currency': "INR", 'payment_capture': 1})
    order.razorpay_order_id = payment['id']
    order.save()

    print(payment)
    context = {
        'cart_count': cart,
        'total_price': round(total_price, 2),
        'payment': payment
    }
    return render(request, "checkout.html", context)
@login_required(login_url='login_page')   
def payment_success(request):
    order = Orders.objects.get(razorpay_order_id=request.GET.get('razorpay_order_id'))
    order.is_paid = True
    order.save()
    cart = Cart.objects.filter(user=request.user)
    cart.delete()
    return redirect('order_page')

def Orders_page(request):
    orders = Orders.objects.filter(user=request.user, is_paid=True).order_by('delivered','-id')
    context = {
        'orders': orders
    }
    return render(request, "order-details.html", context)



@login_required(login_url='login_page')   

def add_comment(request):
    if request.method=='POST':
        comment = request.POST.get('comment')
        product = Product.objects.get(id=request.POST.get('id'))
        orderproduct = OrderProducts.objects.filter(product = product,order__user=request.user,order__delivered=True)
        comment = Comments(comment=comment,product=product,user=request.user,verified=orderproduct.exists())
       
       
        comment.save()
        redirect_url = reverse('product_detail', kwargs={'slug': product.slug}) + '#review'
        return redirect(redirect_url)
    return redirect("product_detail",slug=product.slug)