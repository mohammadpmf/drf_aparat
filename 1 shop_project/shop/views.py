from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import *
from .serializers import *


@api_view()
def get_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view()
def get_category(request, pk):
    category = Category.objects.get(pk=pk)
    serializer = CategorySerializer(category)
    return Response(serializer.data)


@api_view()
def get_products(request):
    products = Product.objects.select_related("category").all()[:100]
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)



@api_view()
def get_product(request, pk):
    product = Product.objects.select_related("category").get(pk=pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)