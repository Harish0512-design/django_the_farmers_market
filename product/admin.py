from django.contrib import admin
from .models import Discount, Product, CheckOut, Cart

# Register your models here.
admin.site.register(Discount)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CheckOut)
