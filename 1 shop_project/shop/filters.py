import django_filters
from django_filters import filters
from .models import Product


class ProductFilter(django_filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="price", lookup_expr="lte")
    title = filters.CharFilter(field_name="title", lookup_expr="contains")
    description = filters.CharFilter(field_name="description", lookup_expr="contains")

    class Meta:
        model = Product
        fields = ["category"]
