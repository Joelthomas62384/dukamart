from django.contrib import admin
from . models import *



class subCategoryTabular(admin.TabularInline):
    model = Sub_Category
    

class CategoryAdmin(admin.ModelAdmin):
    inlines = [subCategoryTabular]
    extra =1

class ProductImageTabular(admin.TabularInline):
    model = Product_images

class AddtionalInformationTabular(admin.TabularInline):
    model = Additional_Information


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageTabular, AddtionalInformationTabular]
    extra = 1




admin.site.register(Slider)
admin.site.register(Feature)
admin.site.register(Main_Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category,CategoryAdmin)






# admin.site.register()
# admin.site.register()
# admin.site.register()