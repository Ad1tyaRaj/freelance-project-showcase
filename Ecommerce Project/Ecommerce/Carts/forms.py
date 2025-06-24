from django import forms
from django.contrib.auth.forms import UserCreationForm
from Products.models import Products


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['product_badge', 'product_name', 'product_price', 'product_old_price', 'product_reviews', 'product_image', 'product_description']
        labels = {
            'product_badge': 'Badge',
            'product_name': 'Product Name',
            'product_price': 'Product Price',
            'product_old_price': 'Product Old Price',
            'product_reviews': 'Product Reviews',
            'product_image': 'Product Image',
            'product_description': 'Product Description',
        }