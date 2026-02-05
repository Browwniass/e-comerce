import uuid

class FakePaymentService:

    @staticmethod
    def create_payment(*, payment):
        external_id = str(uuid.uuid4())

        payment.external_payment_id = external_id
        payment.status = payment.Status.PENDING
        payment.save(update_fields=["external_payment_id", "status"])

        return {
            "payment_url": f"/fake-pay/{external_id}"
        }