from django.urls import path

from . import views

urlpatterns = [
    path("categories/", views.get_categories, name="categories"),
    path("category/<int:pk>/", views.get_category, name="category"),
    path("products/", views.get_products, name="products"),
    path("product/<int:pk>/", views.get_product, name="product"),
    path("addresses/", views.get_addresses, name="addresses"),
    path("address/<int:pk>/", views.get_address, name="address"),
    path("customers/", views.GetCustomers.as_view(), name="customers"),
    # path("customers/", views.get_customers, name="customers"),
    path("customer/<int:pk>/", views.GetCustomer.as_view(), name="customer"),
    # path("customer/<int:pk>/", views.get_customer, name="customer"),
    path("orders/", views.GetOrders.as_view(), name="orders"),
    # path("orders/", views.get_orders, name="orders"),
    path("order/<int:pk>/", views.GetOrder.as_view(), name="order"),
    # path("order/<int:pk>/", views.get_order, name="order"),
]

