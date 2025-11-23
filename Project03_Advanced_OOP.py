from abc import ABC, abstractmethod


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



shirt = Shirt("SHIRT-RED-M", 2500, "M", "Red")
mug = Mug("MUG-WHITE-12", 1200, 12)

cart = Cart()
cart.add_item(shirt, 2)
cart.add_item(mug, 1)

cart.print_receipt()

from abc import ABC, abstractmethod

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

c = Customer(1, "M001", "Alice", "Gold", 0)
o = Order(1, "O100", "M001", "Delivered", 5000)  

program = LoyaltyProgram(GoldReward())
program.add_customer(c)
program.add_order(o)

earned = program.apply_points("O100")
print(f"Points earned: {earned}")
print(c)
