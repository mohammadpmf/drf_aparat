from rest_framework import serializers

class CategorySerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255)
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class ProductSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField()
    slug = serializers.SlugField()
    price = serializers.DecimalField(max_digits=15, decimal_places=2)
    inventory = serializers.IntegerField()
    # category = serializers.PrimaryKeyRelatedField(read_only=True)
    category = serializers.StringRelatedField(read_only=True)