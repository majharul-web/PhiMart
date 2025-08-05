from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet,ModelViewSet
from order.models import Cart, CartItem, Order, OrderItem
from order.serializers import CartSerializer, CartItemSerializer, AddCartItemSerializer, UpdateCartItemSerializer,OrderSerializer,CreateOrderItemSerializer
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin,RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers

# Create your views here.

class CartViewSet(CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,GenericViewSet):
    serializer_class = CartSerializer
    permission_classes=[IsAuthenticated]
    
    def perform_create(self, serializer):
        user = self.request.user
        if Cart.objects.filter(user=user).exists():
            raise serializers.ValidationError("User already has a cart.")
        serializer.save(user=user)

    def get_queryset(self):
        return Cart.objects.prefetch_related('items__product').filter(user=self.request.user)


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = CartItem.objects.all()
    def get_serializer_class(self):
        if self.request.method in ['POST']:
            return AddCartItemSerializer
        elif self.request.method in 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}
    
    def get_queryset(self):
        return CartItem.objects.select_related('product').filter(cart_id=self.kwargs['cart_pk'])



class OrderViewSet(ModelViewSet):

    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method in ['POST']:
            return CreateOrderItemSerializer
        return OrderSerializer
    
    def get_serializer_context(self):
        return {'user_id': self.request.user.id}

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.prefetch_related('items__product').all()
        return Order.objects.prefetch_related('items__product').filter(user=self.request.user)

