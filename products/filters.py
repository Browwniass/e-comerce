import django_filters

from products.models.products import Product


class ProductsFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            "name": ["exact", "lt", "gt"],
            "price": ["exact", "lt", "gt"],
            "category": ["exact"],
        }
