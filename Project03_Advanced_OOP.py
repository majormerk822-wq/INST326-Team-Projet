from abc import ABC, abstractmethod

# -------------------------------
# Abstract Product & Subclasses
# -------------------------------

class AbstractProduct(ABC):
    def __init__(self, sku, price_cents):
        self._sku = sku
        self._price_cents = price_cents

    @abstractmethod
    def get_description(self):
        """Must be implemented by subclasses"""
        pass

    def get_price_dollars(self):
        return self._price_cents / 100.0

    def __str__(self):
        return f"{self._sku} - ${self.get_price_dollars():.2f}"

class Shirt(AbstractProduct):
    def __init__(self, sku, price_cents, size, color):
        super().__init__(sku, price_cents)
        self._size = size
        self._color = color

    def get_description(self):
        return f"{self._color} Shirt (Size {self._size})"

class Mug(AbstractProduct):
    def __init__(self, sku, price_cents, capacity_oz):
        super().__init__(sku, price_cents)
        self._capacity_oz = capacity_oz

    def get_description(self):
        return f"Mug - {self._capacity_oz} oz"

# -------------------------------
# Cart Class
# -------------------------------

class Cart:
    def __init__(self):
        self.items = []  # list of tuples (product, qty)

    def add_item(self, product, qty):
        self.items.append((product, qty))

    def total_price_cents(self):
        return sum(prod._price_cents * qty for prod, qty in self.items)

    def print_receipt(self):
        for prod, qty in self.items:
            print(f"{prod.get_description()} x {qty} - ${prod.get_price_dollars() * qty:.2f}")
        print(f"Total: ${self.total_price_cents() / 100:.2f}")

# -------------------------------
# Reward Strategy Pattern
# -------------------------------

class RewardStrategy(ABC):
    @abstractmethod
    def calculate(self, order):
        pass

class BronzeReward(RewardStrategy):
    def calculate(self, order):
        return order.total_cents // 100

class GoldReward(BronzeReward):
    def calculate(self, order):
        base = super().calculate(order)
        return base * 2

class PlatinumReward(RewardStrategy):
    def calculate(self, order):
        return (order.total_cents // 100) * 3

# -------------------------------
# Customer and Order Classes
# -------------------------------

class Customer:
    def __init__(self, id, member_id, name, tier, points=0):
        self._id = id
        self._member_id = member_id
        self._name = name
        self._tier = tier
        self._points = points

    @property
    def member_id(self): return self._member_id
    @property
    def name(self): return self._name
    @property
    def points(self): return self._points
    def add_points(self, n): self._points += n

    def __str__(self):
        return f"{self._name} [{self._tier}] - {self._points} pts"

class Order:
    def __init__(self, id, order_code, member_id, status, total_cents=0):
        self._id = id
        self._order_code = order_code
        self._member_id = member_id
        self._status = status
        self._total_cents = total_cents

    @property
    def order_code(self): return self._order_code
    @property
    def member_id(self): return self._member_id
    @property
    def total_cents(self): return self._total_cents

# -------------------------------
# Loyalty Program Class
# -------------------------------

class LoyaltyProgram:
    def __init__(self, strategy: RewardStrategy):
        self.strategy = strategy
        self.customers = {}
        self.orders = {}

    def add_customer(self, customer):
        self.customers[customer.member_id] = customer

    def add_order(self, order):
        self.orders[order.order_code] = order

    def apply_points(self, order_code):
        order = self.orders[order_code]
        customer = self.customers[order.member_id]

        points = self.strategy.calculate(order) 
        customer.add_points(points)
        return points
