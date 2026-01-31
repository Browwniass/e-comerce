from rest_framework import serializers
from products.models.products import Product

class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'price',
            'category',
        )
        read_only_fields = ('id',)

class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('__all__')
        read_only_fields = ('id', 'created_at', 'updated_at', 'slug')