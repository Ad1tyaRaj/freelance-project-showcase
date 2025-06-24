from django.shortcuts import render
from .models import Products
from django.conf import settings
import os
from rest_framework import serializers
from rest_framework import viewsets
from .serializers import ProductsSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions

# Create your views here.







# Products page
def products(request):
    products_list = Products.objects.all()
    
    # Check if product images exist and set default image if not
    for product in products_list:
        if product.product_image and not os.path.exists(os.path.join(settings.MEDIA_ROOT, str(product.product_image))):
            # Set a default image path or placeholder
            product.image_url = settings.STATIC_URL + 'images/placeholder.jpg'
        else:
            product.image_url = product.product_image.url if product.product_image else settings.STATIC_URL + 'images/placeholder.jpg'
    
    context = {
        'products': products_list
    }
    
    return render(request, 'Products/product.html', context)