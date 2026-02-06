from django.db import models


class Order(models.Model):
    ORDER_STATUS = (
        ("created", "Created"),
        ("paid", "Paid"),
        ("canceled", "Canceled"),
        ("refunded", "Refunded"),
    )

    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="orders"
    )
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default="created")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"order[{self.id}]"


class OrderItem(models.Model):
    order = models.ForeignKey(
        "payments.Order", on_delete=models.CASCADE, related_name="order_items"
    )
    product_id = models.IntegerField()
    product_name = models.CharField(max_length=190)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product_id} [{self.quantity}]"
