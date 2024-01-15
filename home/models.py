from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User


# Create your models here.

class UserAddress(models.Model):
    user= models.OneToOneField(User, related_name='user_address',on_delete=models.CASCADE)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20,null=True)

    def __str__(self) -> str:
        return self.user.username


class Slider(models.Model):
    choices = (
        ('New Deal','New Deal'),
        ('New Arrivals','New Arrivals'),
        ('Hot Deals','Hot Deals'),
    )
    title = models.CharField(max_length=200)
    Slider_image = models.ImageField(upload_to="media/Slider",default="")
    deal = models.CharField(choices=choices,max_length=200)
    discount = models.PositiveIntegerField(default=0,null=True)
    link = models.CharField(default="#",max_length=500,null=True,blank=True)


    def __str__(self):
        return self.title

class Feature(models.Model):

    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="media/Feature")
    link = models.CharField(default="#",max_length=500,null=True,blank=True)
    discount = models.PositiveIntegerField(default=0,null=True)

    def __str__(self):
        return self.title


class Section(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    

class Main_Category(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Main Category"
        verbose_name_plural = "Main Categories"

    def __str__(self) -> str:
        return self.name



class Category(models.Model):
    name = models.CharField(max_length=200)
    main_category = models.ForeignKey(Main_Category,on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
    
class Sub_Category(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)

    def __str__(self):
        return self.name





class Product(models.Model):
    name = models.CharField(max_length=200)
    section = models.ForeignKey(Section, null=True, on_delete=models.DO_NOTHING, blank=True)
    featured_image = models.CharField(max_length=500)
    price = models.PositiveIntegerField(default=0)
    total = models.PositiveIntegerField(default=0)
    available = models.PositiveIntegerField(default=0)
    discount = models.PositiveIntegerField(default=0)
    Description = RichTextField(blank=True,null=True)
    brand = models.CharField(max_length=100,default="")
    category = models.ForeignKey(Category, null=True,on_delete=models.DO_NOTHING)
    tags = models.CharField(max_length=200)
    product_information = RichTextField(blank=True,null=True)
    slug = models.SlugField(max_length=200,unique=True,null=True,blank=True)

   
    


 


    def __str__(self) -> str:
        return self.name[:20] + "..."


@receiver(pre_save, sender=Product)
def generate_slug(sender, instance,*args, **kwargs):
    if not instance.slug:
        base_slug = slugify(instance.name)
        unique_slug = base_slug

        while Product.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{base_slug}-{instance.id}"
        instance.slug = unique_slug


pre_save.connect(generate_slug, sender=Product)




class Additional_Information(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    specification = models.CharField(max_length=100)
    detail = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.product.name
    

class Product_images(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    image = models.CharField(max_length=500)

    def __str__(self) -> str:
        return self.product.name



class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        return self.user.username + ' - ' + self.product.name
    
    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Cart"



class Orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    products = models.ManyToManyField("Product", through="OrderProducts", related_name="orders")
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    total_price = models.PositiveIntegerField(default=0)
    is_paid = models.BooleanField(default=False)
    razorpay_order_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_payment_signature = models.CharField(max_length=255, blank=True, null=True)
    delivered = models.BooleanField(default=False)
    

    def __str__(self) -> str:
        return self.user.username
    
    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

class OrderProducts(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    total = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.order.user.username}-{self.product.name}"

class OrderTracking(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    reached = models.CharField(max_length=220,null=True,blank=True)

    def __str__(self) -> str:
        return self.order.user.username
    



class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    comment = models.TextField(null=True,blank=True)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)


    def __str__(self) -> str:
        return self.user.username + ", " + self.product.name[:30]