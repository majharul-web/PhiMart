from rest_framework.response import Response
from rest_framework.decorators import api_view
from product.models import Product, Category
from django.shortcuts import get_object_or_404
from product.serializers import ProductSerializer, CategorySerializer

# Create your views here.

@api_view()
def view_products(request):
    products = Product.objects.select_related('category').all()
    product_data = ProductSerializer(products, many=True, context={'request': request}).data
    return Response({"products": product_data})

@api_view()
def view_product(request,id):
    product =get_object_or_404(Product, id=id)
    product_data = ProductSerializer(product).data
    return Response({"product": product_data})


@api_view()
def view_categories(request):
    categories = Category.objects.all()
    category_data = CategorySerializer(categories, many=True).data
    return Response({"categories": category_data})

@api_view()
def view_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category_data = CategorySerializer(category).data
    return Response({"category": category_data})