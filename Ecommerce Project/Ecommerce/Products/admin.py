from django.contrib import admin
from .models import Products
# Register your models here.

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'product_name',
        'product_badge',
        'product_category',
        'product_price',
        'product_old_price',
        'product_reviews',
        'product_description',
        'product_image',
    )