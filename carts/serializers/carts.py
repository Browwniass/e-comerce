from rest_framework import serializers

from products.models.products import Product
from carts.models.carts import Cart, CartItem
from products.serializers.products import ProductShortSerializer

class CartsShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('user',)
        read_only_fields = ('user',)

class CartsItemSerializer(serializers.ModelSerializer):
    product = ProductShortSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True
    )

    class Meta:
        model = CartItem
        fields = (
            'id',
            'cart',
            'product',
            'product_id',
            'quantity',
        )
        read_only_fields = ('cart',)
