from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Products(models.Model):
    CATEGORY_CHOICES = [
        ('electronics', 'Electronics'),
        ('clothing', 'Clothing'),
        ('home_appliance', 'Home Appliance'),
        ('books', 'Books'),
        ('toys', 'Toys'),
        ('sports', 'Sports'),
        ('beauty', 'Beauty'),
        ('others', 'Others'),
    ]

    product_badge = models.CharField(max_length=100)
    product_name = models.CharField(max_length=100)
    product_price = models.IntegerField()
    product_old_price = models.IntegerField()
    product_category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    product_reviews = models.IntegerField(default=0)
    product_description = models.TextField()
    product_image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return f"{self.product_name} ({self.get_product_category_display()})"