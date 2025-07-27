from rest_framework.response import Response
from rest_framework.decorators import api_view
from product.models import Product, Category
from django.shortcuts import get_object_or_404
from product.serializers import ProductSerializer, CategorySerializer
from django.db.models import Count
from rest_framework import status

# Create your views here.

@api_view(['GET', 'POST'])
def view_products(request):
    if request.method == 'GET':
        products = Product.objects.select_related('category').all()
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response({"products": serializer.data})

    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view()
def view_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    serializer = ProductSerializer(product, context={'request': request})
    return Response({"product": serializer.data})


@api_view(['GET', 'POST'])
def view_categories(request):
    if request.method == 'GET':
        categories = Category.objects.annotate(
                product_count=Count('products')
        ).all()
        serializer = CategorySerializer(categories, many=True)
        return Response({"categories": serializer.data})

    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

        

@api_view()
def view_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    serializer = CategorySerializer(category)
    return Response({"category": serializer.data})