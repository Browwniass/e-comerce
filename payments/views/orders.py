from django.db import transaction
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from payments.models.orders import OrderItem, Order
from payments.services import utils


class OrderCreateView(APIView):
    """
    Make Order based on user''s cart
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Get user's cart and then all of his items
        cart = request.user.cart
        items_qr = list(cart.items.select_related("product"))

        if not items_qr:
            return Response(
                {"detail": "Cart is empty"},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Use transaction so that actions are atomic.
        with transaction.atomic():
            # calculate total amount and check if there are enough products for sale
            total = utils.total_price(items_qr)
            if total == -1:
                return Response(
                    {"detail": "Item quantity exceeds stock quantity"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            order = Order.objects.create(
                user=request.user,
                total_amount=total,
            )

            cart_items = []

            for item in items_qr:
                cart_items.append(
                    OrderItem(
                        order=order,
                        product_id=item.product.id,
                        product_price=item.product.price,
                        quantity=item.quantity,
                    )
                )

            OrderItem.objects.bulk_create(cart_items)
            cart.items.all().delete()

        return Response(
            {
                "order_id": order.id,
                "status": order.status,
                "total_amount": order.total_amount,
            },
            status=status.HTTP_201_CREATED,
        )
