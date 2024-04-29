from django.contrib import admin
from .models import Product, ProductCategory, ProductTag, ProductBrand, ProductVisit, ProductGallery
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
   
   list_display = ['title', 'is_active']
   list_editable = ['is_active']
   list_filter = ['category']
    

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductCategory)
admin.site.register(ProductTag)
admin.site.register(ProductBrand)
admin.site.register(ProductVisit)
admin.site.register(ProductGallery)

