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
    list_display = ('sliced_name', 'price', 'total', 'available', 'discount')
    list_editable = ('price', 'total', 'available', 'discount')

    def sliced_name(self, obj):
        
        return obj.name[:20] 
    sliced_name.short_description = 'Sliced Name'



admin.site.register(Slider)
admin.site.register(Feature)
admin.site.register(Main_Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Section)




