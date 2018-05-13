from django.contrib import admin

from .models import Product, ProductColorVariation, ProductSizeVariation

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'product_type', 'gender', 'season', 'price', 'sale_price', 'active']
    list_filter = ['product_type', 'gender', 'season', 'active']
    search_field = ['name']

    class Meta:
        model = Product

class ProductColorVariationAdmin(admin.ModelAdmin):
    list_display = ['product', 'image', 'color']
    list_filter = ['color']
    search_field = ['product']

    class Meta:
        model = ProductColorVariation

class ProductSizeVariationAdmin(admin.ModelAdmin):
    list_display = ['product', 'size', 'inventory'] # 'product.color'
    list_filter = ['size']
    search_field = ['product']

    class Meta:
        model = ProductSizeVariation

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductColorVariation, ProductColorVariationAdmin)
admin.site.register(ProductSizeVariation, ProductSizeVariationAdmin)
