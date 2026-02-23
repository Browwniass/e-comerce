import json

from requests import RequestException
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from payments.models.orders import Order
from payments.models.payments import Payment
from payments.serializers.payments import PaymentCreateSerializer
from payments.services.mockpayment import PaymentService


class PaymentCreateView(APIView):
    """
    Create a payment and return a URL for external provider to pay for an order
    """

    def post(self, request):
        serializer = PaymentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order_id = serializer.validated_data["order_id"]

        try:
            order = Order.objects.get(id=order_id, user=request.user, status="created")
        except Order.DoesNotExist:
            return Response(
                {"detail": "Order does not exist or already paid"},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            payment_data = PaymentService.create_payment(order=order)
        except RequestException as err:
            return Response(
                {"detail": str(err)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        except ValueError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        return Response(
            {"confirmation_url": payment_data.get("confirmation_url")},
            status=status.HTTP_201_CREATED,
        )


