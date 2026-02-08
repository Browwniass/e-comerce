from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.exceptions import NotFound
from rest_framework.filters import OrderingFilter

from common.permissions import AdminOrReadOnly
from common.views.mixins import LCRUDViewSet
from products.filters import ProductsFilter
from products.models.products import Product
from products.models.categories import Category
from products.serializers.products import (
    ProductListSerializer,
    ProductDetailSerializer,
    ProductCategorySerializer,
)


class ProductsListView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    permission_classes = [AdminOrReadOnly]
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    search_fields = ("name",)
    ordering_fields = ["name", "price"]
    filterset_class = ProductsFilter
    ordering = ["name"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ProductDetailSerializer
        return ProductListSerializer


class ProductsDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    lookup_field = "id"
    permission_classes = [AdminOrReadOnly]

    def get_object(self):
        obj = super().get_object()
        if obj.slug != self.kwargs["slug"]:
            raise NotFound("Wrong product slug")
        return obj


class ProductsCategoryView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [AdminOrReadOnly]

    def get_queryset(self):
        if "categories_slug" in self.kwargs:
            return Product.objects.select_related("category").filter(
                category__slug=self.kwargs["categories_slug"]
            )
        return self.queryset

    def perform_create(self, serializer):
        if "categories_slug" in self.kwargs:
            category = Category.objects.get(slug=self.kwargs["categories_slug"])
            serializer.save(category=category)


class ProductsModelView(LCRUDViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_serializer_class(self):
        if self.action in [
            "update",
            "partial_update",
            "retrieve",
            "delete",
            "create",
        ]:
            return ProductDetailSerializer
        return self.serializer_class
