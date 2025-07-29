from django.urls import path,include
from product.views import ProductViewSet, CategoryViewSet,ReviewViewSet
from rest_framework_nested import routers

router = routers.SimpleRouter()
router.register('products', ProductViewSet, basename='product')
router.register('categories', CategoryViewSet, basename='category')

product_router = routers.NestedSimpleRouter(router, 'products', lookup='product')
product_router.register('reviews', ReviewViewSet, basename='product-reviews')



# urlpatterns = router.urls
urlpatterns = [
    path('', include(router.urls)),
    path('', include(product_router.urls)),
    
    # If you want to include other URLs, you can add them here
    # path('some-other-url/', include('some_app.urls')),
]
