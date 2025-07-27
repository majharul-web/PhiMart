from django.urls import path
from product import views

urlpatterns = [
    path('', views.view_products, name='product-list'),
    path('<int:pk>/', views.view_product, name='product-detail'),
]
