from carts.models import Cart, CartItem
from carts.serializers.carts import CartsItemSerializer, CartsItemDetailSerializer
from common.views.mixins import LCRDViewSet, LCRUDViewSet

class CartsView(LCRUDViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartsItemSerializer

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return CartsItemDetailSerializer
        return self.serializer_class

    def get_queryset(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return cart.items.all()

    def perform_create(self, serializer):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)
