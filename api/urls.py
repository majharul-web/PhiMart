from django.urls import path,include

urlpatterns = [
    path('categories/', include('product.category_urls')),
    path('products/', include('product.product_urls')),

]