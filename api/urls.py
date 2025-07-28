from django.urls import path,include
from rest_framework.routers import DefaultRouter
from product.views import ProductViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'categories', CategoryViewSet, basename='category')

# urlpatterns = router.urls
urlpatterns = [
    path('', include(router.urls)),
    # If you want to include other URLs, you can add them here
    # path('some-other-url/', include('some_app.urls')),
]
