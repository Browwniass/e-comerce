from django.contrib import admin
from products.models import Category
from products.models.products import Product

admin.site.register(Product)
admin.site.register(Category)