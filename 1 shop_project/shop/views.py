from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializers import *


@api_view()
def get_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view()
def get_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    serializer = CategorySerializer(category)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view()
def get_products(request):
    products = Product.objects.select_related("category").all()[:100]
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view()
def get_product(request, pk):
    product = get_object_or_404(Product.objects.select_related("category"), pk=pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view()
def get_addresses(request):
    addresses = Address.objects.select_related(
        "customer", "city__province__country"
    ).all()
    serializer = AddressSerializer(addresses, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view()
def get_address(request, pk):
    address = get_object_or_404(
        Address.objects.select_related("customer", "city__province__country"), pk=pk
    )
    serializer = AddressSerializer(address)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view()
def get_customers(request):
    customers = Customer.objects.all()[:10]
    serializer = CustomerSerializer(customers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(http_method_names=["GET", "POST", "PUT", "PATCH", "DELETE"])
def get_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "GET":
        serializer = CustomerSerializer(customer)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == "POST":
        serializer = CustomerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    if request.method == "DELETE":
        customer.delete()
        return Response("Customer deleted successfully!", status=status.HTTP_204_NO_CONTENT)
    if request.method == "PUT":
        serializer = CustomerSerializer(instance=customer, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    if request.method == "PATCH":
        serializer = CustomerSerializer(instance=customer, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    return Response("OK", status=status.HTTP_200_OK)
