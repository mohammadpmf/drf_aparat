from django.urls import path

from . import views

urlpatterns = [
    path("categories/", views.get_categories, name="categories"),
    path("category/<int:pk>/", views.get_category, name="category"),
    path("products/", views.get_products, name="products"),
    path("product/<int:pk>/", views.get_product, name="product"),
    path("addresses/", views.get_addresses, name="addresses"),
    path("address/<int:pk>/", views.get_address, name="address"),
]
