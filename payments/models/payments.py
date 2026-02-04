from django.db import models

class Payment(models.Model):
    PAYMENT_STATUS = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    )
    order = models.ForeignKey(
        'payments.Order',
        on_delete=models.CASCADE,
        related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default='pending',
    )
    provider = models.CharField(max_length=50)
    external_payment_id = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)