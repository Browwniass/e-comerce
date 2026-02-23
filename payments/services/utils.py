def total_price(items):
    """Calculate the total price of a list of items"""
    total = 0

    for item in items:
        if item.quantity > item.product.stock:
            return -1
        total += item.quantity * item.product.price

    return total