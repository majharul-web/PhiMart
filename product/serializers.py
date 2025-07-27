from rest_framework import serializers
from product.models import Product,Category

from decimal import Decimal

class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=500, allow_blank=True, required=False) 


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=500)
    unit_price = serializers.DecimalField(max_digits=10, decimal_places=2,source='price')
    stock = serializers.IntegerField()
    price_with_tax=serializers.SerializerMethodField(method_name='get_price_with_tax')
    
    # category=serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    # category=serializers.StringRelatedField()
    # category=CategorySerializer()
    category=serializers.HyperlinkedRelatedField(
        view_name='category-detail',
        queryset=Category.objects.all()
    )

    def get_price_with_tax(self, product):
        tax_rate = 1.15
        return round(product.price * Decimal(tax_rate))





