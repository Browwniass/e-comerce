from django.db import transaction
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from payments.models.orders import OrderItem, Order
from payments.services import utils


class OrderCreateView(APIView):
    """
    Create Order based on user's cart
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart = request.user.cart
        items_qr = list(cart.items.select_related("product"))
        # Check if user even have smth to buy
        if not items_qr:
            return Response(
                {"detail": "Cart is empty"},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            # Calculate total amount and validate product stock availability
            total = utils.total_price(items_qr)
            if total == -1:
                return Response(
                    {"detail": "Not enough stock"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            # Ensure the user has only one active unpaid order
            Order.objects.filter(
                user=request.user,
                status="created"
            ).update(status="canceled")

            # Create new order
            order = Order.objects.create(
                user=request.user,
                total_amount=total,
            )

            cart_items = []

            # Processing an order from the items in the cart
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
