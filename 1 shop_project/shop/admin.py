from django.contrib import admin

from .models import *

admin.site.register(Category)
admin.site.register(Discount)
admin.site.register(Product)
admin.site.register(Comment)
admin.site.register(Customer)
admin.site.register(Country)
admin.site.register(Province)
admin.site.register(City)
admin.site.register(Address)
admin.site.register(Basket)
admin.site.register(BasketItem)
admin.site.register(Order)
admin.site.register(OrderItem)

