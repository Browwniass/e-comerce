import requests

from django.db import transaction

from payments.models import Order, Payment


class PaymentService:

    @staticmethod
    def create_payment(order: Order) -> dict:
        """
        Create and send payment information to external provider
        """

        # Leave only one active payment with the pending status.
        Payment.objects.filter(order=order, status="pending").update(status="failed")

        payment = Payment.objects.create(
            order=order,
            amount=order.total_amount,
            provider="mockpayment"
        )

        try:
            response = requests.post(
                "http://127.0.0.1:8000/api/mock-gateway/",
                json={
                    "amount": {"value": str(payment.amount), "currency": "RUB"},
                    "payment_method_data": {"type": "bank_card"},
                    "confirmation": {
                        "type": "redirect",
                        "return_url": "http://127.0.0.1:8000/api/carts/",
                    },
                    "description": f"Заказ {payment.order.id}",
                },
                timeout = 5  # Limiting time for connection
            )
            response.raise_for_status()  # raise Error if request was`t successful
            data = response.json()
        except requests.RequestException:
            payment.status = "failed"
            payment.save(update_fields=["status"])
            raise requests.RequestException(
                "Request error with payment creation on external provider occurred"
            )

        payment.external_payment_id = data.get("payment_id")
        confirmation_url = data.get("confirmation_url")

        if not payment.external_payment_id or not confirmation_url:
            payment.status = "failed"
            payment.save(update_fields=["status"])
            raise ValueError("Invalid response from payment provider")

        payment.save(update_fields=["external_payment_id", "status",])

        return {"confirmation_url": data["confirmation_url"]}
