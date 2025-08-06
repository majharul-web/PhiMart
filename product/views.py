from product.models import Product, Category,Review
from product.serializers import ProductSerializer, CategorySerializer, ReviewSerializer, ProductImageSerializer
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
from drf_yasg.utils import swagger_auto_schema



class ProductViewSet(ModelViewSet):
    
    """
    API endpoint for managing products.
     - Allows listing, retrieving, creating, updating, and deleting products.
     - Supports filtering, searching, and ordering.
     - Pagination is applied using DefaultPagination.
     - Only admin users can create, update, or delete products.
     - Regular users can view the product list and details.
    
    """
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at']
    
    permission_classes = [IsAdminOrReadOnly] 
     

    def list(self, request, *args, **kwargs):
        """
        Provides a list of products with optional filtering, searching, and ordering.
        """

        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Create a new product",
        operation_description="Creates a new product with the provided details.",
        request_body=ProductSerializer,
        responses={201: ProductSerializer,400: 'Bad Request', 403: 'Forbidden'}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
     
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
    
class ProductImageViewSet(ModelViewSet):
    """
    API endpoint for managing product images.
     - Allows listing, retrieving, creating, updating, and deleting images for a specific product.
     - Only admin users can create, update, or delete images.
     - Regular users can view the images.

    """
    
    serializer_class = ProductImageSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Product.objects.none()
        product_id = self.kwargs.get('product_pk')
        return Product.objects.get(id=product_id).images.all()
    
    def perform_create(self, serializer):
        product_id = self.kwargs.get('product_pk')
        serializer.save(product_id=product_id)
    
    def get_serializer_context(self):
        return {'product_id': self.kwargs.get('product_pk')}


class CategoryViewSet(ModelViewSet):
    """
    API endpoint for managing product categories.
     - Allows listing, retrieving, creating, updating, and deleting categories.
     - Only admin users can create, update, or delete categories.
     - Regular users can view the category list and details.
    """
    queryset = Category.objects.annotate(product_count=Count('products')).all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly] 

    def get_serializer_context(self):
        return {'request': self.request}

class ReviewViewSet(ModelViewSet):
    """
    API endpoint for managing product reviews.
     - Allows listing, retrieving, creating, updating, and deleting reviews for a specific product.
     - Only admin users can create, update, or delete reviews.
     - Regular users can view the reviews.
    """
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewAuthorReadOnly]
    
    def perform_create(self, serializer):
        if getattr(self, 'swagger_fake', False):
            return super().perform_create(serializer)
        serializer.save(user=self.request.user)
    
    def get_queryset(self):
        product_id = self.kwargs.get('product_pk')
        return Review.objects.filter(product_id=product_id).all()
    def get_serializer_context(self):
        return {'product_id': self.kwargs.get('product_pk')}

