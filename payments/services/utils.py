def total_price(items):
    total = 0  #

    for item in items:
        if item.quantity > item.product.stock:
            return -1
        total += item.quantity * item.product.price

    return total