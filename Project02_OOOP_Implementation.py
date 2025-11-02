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

class Customer:
    def __init__(self, id, member_id, name, tier, points=0):
        if not isinstance(id, int) or id <= 0: raise ValueError("id must be a positive int")
        if not member_id or not isinstance(member_id, str): raise ValueError("invalid member_id")
        if not name or not isinstance(name, str): raise ValueError("invalid name")
        if tier not in ["Bronze", "Silver", "Gold", "Platinum"]: raise ValueError("invalid tier")
        if not isinstance(points, int) or points < 0: raise ValueError("invalid points")
        self._id, self._member_id, self._name, self._tier, self._points = id, member_id, name, tier, points

    @property
    def id(self): return self._id
    @property
    def member_id(self): return self._member_id
    @property
    def name(self): return self._name
    @property
    def tier(self): return self._tier
    @tier.setter
    def tier(self, t):
        if t not in ["Bronze", "Silver", "Gold", "Platinum"]: raise ValueError("invalid tier")
        self._tier = t
    @property
    def points(self): return self._points
    @points.setter
    def points(self, p):
        if not isinstance(p, int) or p < 0: raise ValueError("invalid points")
        self._points = p

    def add_points(self, n): 
        if n < 0: raise ValueError("negative points")
        self._points += n

    def redeem_points(self, n):
        if n < 0 or n > self._points: raise ValueError("invalid redeem")
        self._points -= n

    def upgrade_tier(self):
        tiers = ["Bronze", "Silver", "Gold", "Platinum"]
        i = tiers.index(self._tier)
        if i < len(tiers) - 1: self._tier = tiers[i + 1]

    def reset_points(self): self._points = 0

    def __str__(self): return f"{self._name} [{self._tier}] - {self._points} pts"
    def __repr__(self): return f"Customer({self._id}, '{self._member_id}', '{self._name}', '{self._tier}', {self._points})"

class Order:
    def __init__(self, id, order_code, member_id, status, total_cents=0):
        if not isinstance(id, int) or id <= 0: raise ValueError("id must be a positive int")
        if not order_code or not isinstance(order_code, str): raise ValueError("invalid order_code")
        if not member_id or not isinstance(member_id, str): raise ValueError("invalid member_id")
        if status not in ["Pending", "Shipped", "Delivered", "Cancelled"]: raise ValueError("invalid status")
        if not isinstance(total_cents, int) or total_cents < 0: raise ValueError("invalid total_cents")
        self._id, self._order_code, self._member_id, self._status, self._total_cents = id, order_code, member_id, status, total_cents

    @property
    def id(self): return self._id
    @property
    def order_code(self): return self._order_code
    @property
    def member_id(self): return self._member_id
    @property
    def status(self): return self._status
    @status.setter
    def status(self, s):
        if s not in ["Pending", "Shipped", "Delivered", "Cancelled"]: raise ValueError("invalid status")
        self._status = s
    @property
    def total_cents(self): return self._total_cents
    @total_cents.setter
    def total_cents(self, t):
        if not isinstance(t, int) or t < 0: raise ValueError("invalid total_cents")
        self._total_cents = t

    def add_charge(self, cents):
        if cents < 0: raise ValueError("negative charge")
        self._total_cents += cents

    def apply_discount(self, cents):
        if cents < 0 or cents > self._total_cents: raise ValueError("invalid discount")
        self._total_cents -= cents

    def cancel_order(self):
        if self._status != "Cancelled": self._status = "Cancelled"

    def mark_shipped(self):
        if self._status == "Pending": self._status = "Shipped"

    def __str__(self): return f"Order {self._order_code} [{self._status}] - ${self._total_cents/100:.2f}"
    def __repr__(self): return f"Order({self._id}, '{self._order_code}', '{self._member_id}', '{self._status}', {self._total_cents})"


