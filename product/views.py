from product.models import Product, Category
from product.serializers import ProductSerializer, CategorySerializer
from django.db.models import Count
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        return {'request': self.request}
    
    def destroy(self, request, *args, **kwargs):
        product= self.get_object()
        if product.stock > 10:
            return Response({"error": "Cannot delete product with stock greater than 10."}, status=400)
        return super().destroy(request, *args, **kwargs)


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.annotate(product_count=Count('products')).all()
    serializer_class = CategorySerializer

    def get_serializer_context(self):
        return {'request': self.request}