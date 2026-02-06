import uuid

from django.db import transaction


class FakePaymentService:
    """
    Stub provider for local development and tests.
    """

    @transaction.atomic
    def create_payment(self, *, payment):
        external_id = str(uuid.uuid4())

        payment.external_payment_id = external_id
        payment.status = "pending"
        payment.save(
            update_fields=[
                "external_payment_id",
                "status",
            ]
        )

        return {"payment_url": f"/stub-pay/{external_id}"}
