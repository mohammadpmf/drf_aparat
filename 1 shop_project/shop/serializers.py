from decimal import Decimal

from rest_framework import serializers

from .models import Address, Order, OrderItem, Product, Customer


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


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "birth_date",
        ]
        extra_kwargs = {"email": {"required": True}}

    def validate_email(self, value: str):
        if not value.endswith("@drdjango.ir"):
            raise serializers.ValidationError(
                "آدرس ایمیل شما حتما باید برای سایت دکترجنگو باشد."
            )
        return value

    def validate(self, attrs):
        first_name = attrs.get("first_name")
        last_name = attrs.get("last_name")
        if (first_name and len(first_name) <= 2) or (last_name and len(last_name) <= 2):
            raise serializers.ValidationError(
                {"name_length": "نام و نام خانوادگی باید بیش از ۲ کاراکتر باشد."}
            )
        return super().validate(attrs)


# class CustomerSerializer(serializers.Serializer):
#     first_name = serializers.CharField(max_length=255)
#     last_name = serializers.CharField(max_length=255)
#     email = serializers.EmailField()
#     phone_number = serializers.CharField(max_length=255)
#     birth_date = serializers.DateField(required=False)

#     def create(self, validated_data):
#         Customer.objects.create(**validated_data)
#         return validated_data


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


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "customer_id",
            "customer_name",
            "customer_info",
            "city",
            "street",
            "alley",
            "building_number",
            "building_name",
            "floor",
            "unit",
            "zip_code",
        ]

    customer_name = serializers.StringRelatedField(read_only=True, source="customer")
    customer_info = CustomerSerializer(source="customer")
    city = CitySerializer()


# class AddressSerializer(serializers.Serializer):
#     customer_id = serializers.PrimaryKeyRelatedField(read_only=True)
#     customer_name = serializers.StringRelatedField(read_only=True, source="customer")
#     customer_info = CustomerSerializer(source="customer")
#     city = CitySerializer()
#     street = serializers.CharField(max_length=255)
#     alley = serializers.CharField(max_length=255)
#     building_number = serializers.IntegerField()
#     building_name = serializers.CharField(max_length=255)
#     floor = serializers.IntegerField()
#     unit = serializers.IntegerField()
#     zip_code = serializers.CharField(max_length=10)


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            "quantity",
            "price",
            "product",
        ]

    product = ProductSerializer()


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "id",
            "customer",
            "status",
            "items",
        ]

    customer = CustomerSerializer()
    status = serializers.CharField(source="get_status_display")
    items = OrderItemSerializer(many=True)
