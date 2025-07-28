from django.urls import path
from product import views

urlpatterns = [
    path('', views.ViewProducts.as_view(), name='product-list'),
    path('<int:pk>/', views.ViewProduct.as_view(), name='product-detail'),
]
