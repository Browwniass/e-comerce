from django.db import models


class Cart(models.Model):
    user = models.OneToOneField(
        "users.User", on_delete=models.CASCADE, related_name="cart"
    )

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    def __str__(self):
        return self.user.username


class CartItem(models.Model):
    cart = models.ForeignKey("Cart", on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        "products.Product", on_delete=models.CASCADE, related_name="cart_product"
    )
    quantity = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Продукт_корзины"
        verbose_name_plural = "Продукты_корзины"
        unique_together = ("cart", "product")

    def __str__(self):
        return f"{self.cart} x {self.product}"
