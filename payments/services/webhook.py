import json

from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from config import settings
from payments.models import Payment
from products.models import Product


class PaymentWebhookView(APIView):
    """
    Handle webhook callbacks from the payment provider
    """

    permission_classes = []
    authentication_classes = []

    @transaction.atomic
    def post(self, request):
        secret = request.headers.get("X-Webhook-Secret")
        # Validate webhook secret from external payment provider
        if secret != settings.PAYMENT_WEBHOOK_SECRET_KEY:
            return Response(
                {"detail": "Invalid webhook secret"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        data = json.loads(request.body)
        # Get and lock the payment row to prevent concurrent updates
        try:
            payment = (
                Payment.objects
                .select_related("order")
                .select_for_update()
                .get(external_payment_id=data["payment_id"])
            )
        except Payment.DoesNotExist:
            return Response(
                {"detail": "Payment not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Check if payment was already paid
        if payment.status == "paid":
            return Response(
                {"detail": f"Payment already was done"},
                status=status.HTTP_200_OK
            )

        order = payment.order

        event = data["event"]

        if event == "success":
            items = order.order_items.all()
            product_ids = [item.product_id for item in items]

            # Locking products stock to prevent concurrent updates
            products = Product.objects.filter(id__in=product_ids).select_for_update()
            products_dict = {product.pk: product for product in products}

            for item in items:
                product = products_dict[item.product_id]
                # Validating and updating products stock after successful payment
                if product.stock < item.quantity:
                    return Response(
                        {"detail": "Not enough stock"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                product.stock -= item.quantity
                product.save(update_fields=["stock"])

            payment.status = "paid"
            order.status = "paid"

        elif event == "canceled":
            payment.status = "canceled"

        else:
            return Response(
                {"detail": f"Payment failed"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        payment.save(update_fields=["status"])
        order.save(update_fields=["status"])

        return Response(
            {"detail": f"Payment {payment.status}"},
            status=status.HTTP_200_OK
        )
