from rest_framework import serializers
from product.models import Product,Category
from decimal import Decimal

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'product_count']
    product_count = serializers.IntegerField()
        
    # product_count = serializers.SerializerMethodField(method_name='calculate_product_count')
    # def calculate_product_count(self, category):
    #     return Product.objects.filter(category=category).count()


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'category','price_with_tax']

    category=serializers.HyperlinkedRelatedField(
            view_name='category-detail',
            queryset=Category.objects.all()
        )
    price_with_tax = serializers.SerializerMethodField(method_name='get_price_with_tax')
    def get_price_with_tax(self, product):
        tax_rate = 1.15
        return round(product.price * Decimal(tax_rate))


