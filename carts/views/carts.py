from carts.models import Cart, CartItem
from carts.serializers.carts import CartsItemSerializer
from common.views.mixins import LCRDViewSet

class CartsView(LCRDViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartsItemSerializer

    def get_queryset(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return cart.items.all()

    def perform_create(self, serializer):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)
