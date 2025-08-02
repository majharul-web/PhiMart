from product.models import Product, Category,Review
from product.serializers import ProductSerializer, CategorySerializer, ReviewSerializer
from django.db.models import Count
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from product.filters import ProductFilter
from rest_framework.filters import SearchFilter,OrderingFilter
from product.paginations import DefaultPagination
from rest_framework.permissions import IsAdminUser, AllowAny, DjangoModelPermissions,DjangoModelPermissionsOrAnonReadOnly
from api.permissions import IsAdminOrReadOnly,FullDjangoModelPermissions
from product.permissions import IsReviewAuthorReadOnly



class ProductViewSet(ModelViewSet):
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at']
    
    permission_classes = [IsAdminOrReadOnly] 
     
     
    # permission_classes = [DjangoModelPermissionsOrAnonReadOnly]  
    # permission_classes = [DjangoModelPermissions]  
    # permission_classes = [FullDjangoModelPermissions]
    # permission_classes = [IsAdminUser]

    # def get_permissions(self):
    #     if self.request.method == 'GET':
    #         return [AllowAny()]
    #     return [IsAdminUser()]

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
    permission_classes = [IsAdminOrReadOnly] 

    def get_serializer_context(self):
        return {'request': self.request}

class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewAuthorReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    


    def get_queryset(self):
        product_id = self.kwargs['product_pk']
        return Review.objects.filter(product_id=product_id).all()
    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}

