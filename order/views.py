from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet,ModelViewSet
from order.models import Cart, CartItem
from order.serializers import CartSerializer, CartItemSerializer, AddCartItemSerializer, UpdateCartItemSerializer
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin,RetrieveModelMixin

# Create your views here.

class CartViewSet(CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


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
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk'])
        
    