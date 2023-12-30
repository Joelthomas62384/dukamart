from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver


# Create your models here.


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

