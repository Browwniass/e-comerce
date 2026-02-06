import json
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from payments.models.orders import Order
from payments.models.payments import Payment
from payments.serializers.payments import PaymentCreateSerializer
from payments.services import youkassa


class PaymentCreateView(APIView):

    def post(self, request):
        serializer = PaymentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order_id = serializer.validated_data["order_id"]

        try:
            order = Order.objects.get(id=order_id, user=request.user, status="created")
        except Order.DoesNotExist:
            return Response(
                {"detail": "Order does not exist or already paid"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        payment = Payment.objects.create(
            order=order, amount=order.total_amount, provider="sbp"
        )

        payment_data = youkassa.create_payment(
            payment=payment,
            user=request.user,
        )

        payment.external_payment_id = payment_data["external_id"]
        payment.save(update_fields=["external_payment_id"])

        return Response(
            {
                "payment_url": payment_data.get("payment_url"),
                "qr_code": payment_data.get("qr_code"),
            },
            status=status.HTTP_201_CREATED,
        )


class PaymentWebhookView(APIView):

    def post(self, request):
        data = json.loads(request.body)

        if data["event"] == "payment.succeeded":
            payment = Payment.objects.get(external_payment_id=data["payment_id"])

            payment.status = "paid"
            payment.save(update_fields=["status"])

            order = payment.order
            order.status = "paid"
            order.save(update_fields=["status"])

        return Response({"detail": "Payment succeeded"}, status=status.HTTP_200_OK)
