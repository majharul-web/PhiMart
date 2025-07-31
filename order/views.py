from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet,ModelViewSet
from order.models import Cart, CartItem
from order.serializers import CartSerializer
from order.serializers import CartSerializer, CartItemSerializer
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin,RetrieveModelMixin

# Create your views here.

class CartViewSet(CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    
    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk'])
        
    