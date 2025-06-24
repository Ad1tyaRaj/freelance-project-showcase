from django.contrib import admin
from .models import  Buy_items, Order_items
# Register your models here.

    
@admin.register(Buy_items)
class Buy_itemsAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'item_name',
                    'item_quantity',
                    'item_price',
                    'item_reviews',
                    'item_description',
                    'item_image',
                    )

@admin.register(Order_items)
class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'created_at', 'promocode')
    list_filter = ('created_at', 'promocode')
    search_fields = ('user__username', 'promocode')
    readonly_fields = ('created_at',)
    
    def get_items(self, obj):
        return ", ".join([item.item_name for item in obj.items.all()])
    
    get_items.short_description = 'Items'
