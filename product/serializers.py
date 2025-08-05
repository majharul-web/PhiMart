from rest_framework import serializers
from product.models import Product,Category,Review,ProductImage
from decimal import Decimal
from django.contrib.auth import get_user_model



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'product_count']
    product_count = serializers.IntegerField(read_only=True)
        
    # product_count = serializers.SerializerMethodField(method_name='calculate_product_count')
    # def calculate_product_count(self, category):
    #     return Product.objects.filter(category=category).count()

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id','image']
        read_only_fields = ['created_at','id']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'category','price_with_tax', 'images']
    images= ProductImageSerializer(many=True, read_only=True)
    category=serializers.HyperlinkedRelatedField(
            view_name='category-detail',
            queryset=Category.objects.all()
        )
    price_with_tax = serializers.SerializerMethodField(method_name='get_price_with_tax')
    def get_price_with_tax(self, product):
        tax_rate = 1.15
        return round(product.price * Decimal(tax_rate))

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value

    def validate(self, attrs):
        if attrs.get('stock', 0) < 0:
            raise serializers.ValidationError("Stock cannot be negative.")
        if attrs.get('price', 0) < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        return attrs
    

    

class SimpleUserSerializer(serializers.ModelSerializer):
    name= serializers.SerializerMethodField(method_name='get_name')
    class Meta:
        model = get_user_model()
        fields = ['id', 'name']

    def get_name(self, obj):
        return obj.get_full_name()

class ReviewSerializer(serializers.ModelSerializer):
    # user = SimpleUserSerializer(read_only=True)
    user= serializers.SerializerMethodField(method_name='get_user')
    class Meta:
        model = Review
        fields = ['id', 'user', 'product', 'rating', 'comment', 'created_at', 'updated_at']
        read_only_fields = ['user', 'product']
        
    def get_user(self, obj):
        return SimpleUserSerializer(obj.user).data
    
    def create(self, validated_data):
        product_id = self.context.get('product_id')
        review= Review.objects.create(
            product_id=product_id,
            **validated_data
        )
        return review