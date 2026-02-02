from common.permissions import AdminOrReadOnly
from common.views.mixins import LCRUDViewSet
from products.models.categories import Category
from products.serializers.categories import CategorySerializer

class CategoriesView(LCRUDViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AdminOrReadOnly]