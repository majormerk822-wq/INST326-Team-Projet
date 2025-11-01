class ProductVariant:

    def __init__(self, id, sku, size, color, price_cents, active=True):
        if not sku or not isinstance(price_cents, int) or price_cents < 0:
            raise ValueError("Invalid product data")

        self._id = id
        self._sku = sku
        self._size = size
        self._color = color
        self._price_cents = price_cents
        self._active = active

    @property
    def sku(self):
        return self._sku

    @property
    def price_cents(self):
        return self._price_cents

    @property
    def is_active(self):
        return self._active

    def deactivate(self):
        """Mark this product as inactive."""
        self._active = False

    def get_price_dollars(self):
        """Return the price in dollars (float)."""
        return self._price_cents / 100.0

    def __str__(self):
        return f"{self._color} Shirt ({self._size}) - ${self.get_price_dollars():.2f}"

class InventoryMovement:

    def __init__(self, id, sku, qty_change):
        if not sku or not isinstance(qty_change, int):
            raise ValueError("Invalid inventory movement data")

        self._id = id
        self._sku = sku
        self._qty_change = qty_change

    @property
    def sku(self):
        """Get the SKU this movement is for."""
        return self._sku

    @property
    def qty_change(self):
        """Return how much quantity changed (positive or negative)."""
        return self._qty_change

    def __str__(self):
        direction = "Added" if self._qty_change > 0 else "Removed"
        return f"{direction} {abs(self._qty_change)} units of {self._sku}"
