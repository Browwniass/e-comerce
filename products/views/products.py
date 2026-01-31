from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.exceptions import NotFound
from rest_framework.filters import SearchFilter, OrderingFilter
from products.filters import ProductsFilter
from common.views.mixins import LCRUDViewSet
from products.models.products import Product
from common.permissions import AdminOrReadOnly
from products.serializers.products import (ProductListSerializer,
                                           ProductDetailSerializer)

class ProductsListView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    permission_classes = [AdminOrReadOnly]
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    search_fields = ('name',)
    ordering_fields = ['name', 'price']
    filterset_class = ProductsFilter
    ordering = ['name']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductDetailSerializer
        return ProductListSerializer

class ProductsDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    lookup_field = 'id'
    permission_classes = [AdminOrReadOnly]


    def get_object(self):
        obj = super().get_object()
        if obj.slug != self.kwargs['slug']:
            raise NotFound('Wrong product slug')
        return obj

class ProductsModelView(LCRUDViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_serializer_class(self):
        if self.action in [
            'update',
            'partial_update',
            'retrieve',
            'delete',
            'create',
        ]:
            return ProductDetailSerializer
        return self.serializer_class

