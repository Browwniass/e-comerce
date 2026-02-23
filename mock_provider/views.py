import uuid
import requests
from rest_framework import status

from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from config import settings


class MockGatewayCreateView(APIView):
    """
    View for simulating creating payment instance on external api
    """

    permission_classes = (AllowAny,)

    def post(self, *args, **kwargs):
        """
        Create payment instance
        """

        payment_id = str(uuid.uuid4())
        confirmation_url = f"http://127.0.0.1:8000/api/mock-gateway/{payment_id}/"

        return Response(
            {
                "confirmation_url": confirmation_url,
                "payment_id": payment_id,
            },
        status=status.HTTP_201_CREATED)


class MockGatewayPayView(APIView):
    """
    View for simulating redirection to external api where payment is processed
    """

    permission_classes = (AllowAny,)

    def get(self, request, external_id):
        # request for a successfully paid order
        response = requests.post(
            "http://127.0.0.1:8000/api/payments/webhook/",
            json={
                "payment_id" : external_id,
                "event" : "success"
            },
            headers={
                "X-Webhook-Secret": settings.PAYMENT_WEBHOOK_SECRET_KEY,
            }
        )
        print(response)
        return Response(
            {"detail": "Payment successful"},
            status=status.HTTP_201_CREATED
        )