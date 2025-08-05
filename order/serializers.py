from rest_framework import serializers
from order.models import Cart, CartItem
from product.models import Product
from order.models import Order, OrderItem
from order.services import OrderService


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']  

class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = CartItem
        fields = ['product_id', 'quantity']
    
    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']

        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            cart_item = CartItem(cart_id=cart_id, **self.validated_data)
            cart_item.save()  
            self.instance = cart_item

        return self.instance

    def validate_product_id(self, attrs):
        if not Product.objects.filter(id=attrs).exists():
            raise serializers.ValidationError("Product does not exist.")
        return attrs
    
    
class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']


class CartItemSerializer(serializers.ModelSerializer):
    product=SimpleProductSerializer(read_only=True)
    total_price = serializers.SerializerMethodField(method_name='get_total_price')
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']

    def get_total_price(self, cart_item: CartItem):
        return cart_item.product.price * cart_item.quantity

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField(method_name='get_total_price')
    class Meta:
        model = Cart
        fields = ['id', 'user','items', 'total_price','created_at']
        read_only_fields = ['user']

    def get_total_price(self, cart: Cart):
        return sum(item.product.price * item.quantity for item in cart.items.all())

class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price', 'total_price']
        
class CreateOrderItemSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField(write_only=True)

    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError("Cart does not exist.")
        if not CartItem.objects.filter(cart_id=cart_id).exists():
            raise serializers.ValidationError("Cart is empty.")
        return cart_id

    def create(self, validated_data):
        cart_id = validated_data['cart_id']
        user_id = self.context['user_id']
        
        try:
            order = OrderService.create_order(user_id=user_id, cart_id=cart_id)
            return order
        except Exception as e:
            raise serializers.ValidationError(f"Failed to create order: {str(e)}")
        
    
    def to_representation(self, instance):
        return OrderSerializer(instance).data


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'total_price', 'created_at', 'updated_at', 'items']