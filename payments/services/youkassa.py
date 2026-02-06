import uuid
from yookassa import Payment


def create_payment(*, payment, user):
    idempotence_key = str(uuid.uuid4())
    yok_payment = Payment.create(
        {
            "amount": {"value": str(payment.amount), "currency": "RUB"},
            "payment_method_data": {"type": "bank_card"},
            "confirmation": {
                "type": "redirect",
                "return_url": "http://127.0.0.1:8000/api/payments/",
            },
            "description": f"Заказ {payment.order.id}",
        },
        idempotence_key,
    )

    payment.external_payment_id = yok_payment.id
    payment.status = "pending"
    payment.save(update_fields=["external_payment_id", "status"])

    return yok_payment
