from rest_framework import serializers
from .models import Buy_items, Order_items




class Buy_itemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buy_items
        fields = '__all__'


class Order_itemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order_items
        fields = '__all__'