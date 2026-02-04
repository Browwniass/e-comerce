from django.db import transaction
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from payments.models.orders import OrderItem, Order


class OrderCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart = request.user.cart
        items_qr = list(cart.items.select_related('product'))

        if not items_qr:
            return Response(
                {'detail': 'Cart is empty'},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            total = 0
            for item in items_qr:
                if item.quantity > item.product.stock:
                    return Response(
                        {'detail': 'Item quantity exceeds stock quantity'},
                    )
                total += item.quantity * item.product.price

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
                'order_id': order.id,
                'status': order.status,
                'total_amount': order.total_amount,
            },
            status=status.HTTP_201_CREATED
        )
