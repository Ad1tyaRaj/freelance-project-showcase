from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Buy_items(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    item_name = models.CharField(max_length=100)
    item_price = models.DecimalField(max_digits=10, decimal_places=2)
    item_reviews = models.IntegerField(default=0)
    item_description = models.TextField()
    item_image = models.ImageField(upload_to='item_buy_image')
    item_quantity = models.IntegerField(default=1, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.item_name
    
    @property
    def total_price(self):
        return float(self.item_price) * float(self.item_quantity or 1)
    
class Order_items(models.Model):
    STATUS_CHOICES = (
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Buy_items)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    promocode = models.CharField(max_length=10, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Processing')
    
    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"