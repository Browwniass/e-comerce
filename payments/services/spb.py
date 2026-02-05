class SBPPaymentService:

    @staticmethod
    def create_payment(*, payment, user):
        """
        Здесь будет HTTP-запрос в банк / агрегатор.
        Сейчас — заглушка.
        """

        external_id = f"sbp_{payment.id}"

        return {
            "external_id": external_id,
            "payment_url": f"https://bank.example/pay/{external_id}",
            # или qr_code
        }