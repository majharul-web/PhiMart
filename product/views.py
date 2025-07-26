from rest_framework.response import Response
from rest_framework.decorators import api_view
from product.models import Product, Category
from django.shortcuts import get_object_or_404

# Create your views here.

@api_view()
def view_products(request):
    products = Product.objects.all()
    product_data = [{"id": product.id, "name": product.name} for product in products]
    return Response({"products": product_data})

@api_view()
def view_product(request,id):
    product =get_object_or_404(Product, id=id)
    product_data = {"id": product.id, "name": product.name, "price": product.price}
    return Response({"product": product_data})


@api_view()
def view_categories(request):
    categories = Category.objects.all()
    category_data = [{"id": category.id, "name": category.name} for category in categories]
    return Response({"categories": category_data})