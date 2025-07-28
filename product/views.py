from rest_framework.response import Response
from rest_framework.decorators import api_view
from product.models import Product, Category
from django.shortcuts import get_object_or_404
from product.serializers import ProductSerializer, CategorySerializer
from django.db.models import Count
from rest_framework import status
from rest_framework.views import APIView 


class ViewProducts(APIView):
    def get(self, request):
        products = Product.objects.select_related('category').all()
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response({"products": serializer.data})

    def post(self, request):
        serializer = ProductSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ViewProduct(APIView):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, context={'request': request})
        return Response({"product": serializer.data})

    def put(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"product": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        deleted_product = ProductSerializer(product, context={'request': request})
        return Response({"deleted_product": deleted_product.data}, status=status.HTTP_204_NO_CONTENT)

class ViewCategory(APIView):
    def get(self, request, pk):
        category = get_object_or_404(Category.objects.annotate(product_count=Count('products')).all(), pk=pk)
        serializer = CategorySerializer(category)
        return Response({"category": serializer.data})

    def put(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"category": serializer.data})

    def delete(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        deleted_category = CategorySerializer(category, context={'request': request})
        return Response({"deleted_category": deleted_category.data}, status=status.HTTP_204_NO_CONTENT)
        



class ViewCategories(APIView):
    def get(self, request):
        categories = Category.objects.annotate(product_count=Count('products')).all()
        serializer = CategorySerializer(categories, many=True)
        return Response({"categories": serializer.data})

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)