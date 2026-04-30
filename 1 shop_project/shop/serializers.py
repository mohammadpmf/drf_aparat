from decimal import Decimal

from rest_framework import serializers

from .models import Product


class CategorySerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    onvan = serializers.CharField(max_length=255, source="title")
    description = serializers.CharField(max_length=255)
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class ProductSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField()
    slug = serializers.SlugField()
    price = serializers.DecimalField(max_digits=15, decimal_places=2)
    price_with_tax = serializers.SerializerMethodField()
    inventory = serializers.IntegerField()
    inventory_5 = serializers.SerializerMethodField()
    category_id = serializers.PrimaryKeyRelatedField(read_only=True, source="category")
    category_str = serializers.StringRelatedField(read_only=True, source="category")
    category = CategorySerializer()

    def get_price_with_tax(self, product: Product):
        return round(product.price * Decimal(1.1), 2)

    def get_inventory_5(self, product: Product):
        return product.inventory + 5


class CustomerSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    phone_number = serializers.CharField(max_length=255)
    birth_date = serializers.DateField()


class CountrySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)


class ProvinceSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    country = CountrySerializer()


class CitySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    province = ProvinceSerializer()


class AddressSerializer(serializers.Serializer):
    customer_id = serializers.PrimaryKeyRelatedField(read_only=True)
    customer_name = serializers.StringRelatedField(read_only=True, source="customer")
    customer_info = CustomerSerializer(source="customer")
    city = CitySerializer()
    street = serializers.CharField(max_length=255)
    alley = serializers.CharField(max_length=255)
    building_number = serializers.IntegerField()
    building_name = serializers.CharField(max_length=255)
    floor = serializers.IntegerField()
    unit = serializers.IntegerField()
    zip_code = serializers.CharField(max_length=10)
