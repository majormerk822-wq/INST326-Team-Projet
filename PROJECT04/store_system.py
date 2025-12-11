# check_inventory(sku) -> int
def check_inventory(sku):
    
    total = 0
    for movement in inventory_movements:
        if movement["sku"] == sku:
            total += movement["qty_change"]
    return total


# add_to_inventory(sku, qty) -> dict
def add_to_inventory(sku, qty):
    """Add stock (like receiving new shirts)."""
    if qty <= 0:
        print("Quantity must be positive.")
        return None
    if sku not in product_variants:
        print("SKU not found.")
        return None
    inventory_movements.append({"sku": sku, "qty_change": qty})
    new_qty = calculate_stock_level(sku)
    print(f"Added {qty} units to {sku}. New stock: {new_qty}")
    return {"sku": sku, "new_qty": new_qty}


# remove_from_inventory(sku, qty) -> dict
def remove_from_inventory(sku, qty):
    if qty <= 0:
        print("Quantity must be positive")
        return None

    if not any(p["sku"] == sku for p in product_variants):
        print("SKU not found")
        return None

    current_stock = calculate_stock_level(sku)
    if current_stock < qty:
        print(f"Insufficient stock. Available: {current_stock}, Requested: {qty}")
        return None

    inventory_movements.append({"sku": sku, "qty_change": -qty})
    new_qty = calculate_stock_level(sku)
    print(f"Removed {qty} units from {sku}. New stock: {new_qty}")
    return {"sku": sku, "new_qty": new_qty}


# calculate_stock_level(sku) -> int
def calculate_stock_level(sku):
    """Add up all stock movements for one product."""
    total = 0
    for move in inventory_movements:
        if move["sku"] == sku:
            total = total + move["qty_change"]
    return total


# is_product_in_stock(sku, qty) -> bool
inventory_movements = [
    {"sku": "SHIRT-RED-M", "qty_change": 10},
    {"sku": "SHIRT-BLUE-L", "qty_change": 5},
]

def is_product_in_stock(sku, qty):
    current_stock = calculate_stock_level(sku)
    return current_stock >= qty


# scan_item(cart, sku) -> list
def scan_item(cart, sku):
    product = next((p for p in product_variants if p["sku"] == sku and p["active"]), None)
    if product is None:
        raise ValueError(f"Product with SKU '{sku}' not found or inactive.")
    for item in cart:
        if item["sku"] == sku:
            item["qty"] += 1
            return cart
    cart.append({
        "sku": sku,
        "price_cents": product["price_cents"],
        "qty": 1
    })
    return cart


# calculate_cart_total(cart) -> total_cents
def calculate_cart_total(cart):
    total = 0
    for item in cart:
        total += item["qty"] * item["price_cents"]
    return total


# generate_order_code(order_id) -> string
def generate_order_code(order_id):
    if order_id < 0:
        print("Order ID must be positive.")
        return None
    order_str = str(order_id)
    while len(order_str) < 4:
        order_str = "0" + order_str
    return "ORD-" + order_str


# finalize_sale(cart, member_id=None) -> order
def finalize_sale(cart, member_id=None):
    if not cart:
        print("Cart is empty.")
        return None
    total_cents = calculate_cart_total(cart)
    discount_cents = 0
    if member_id and validate_member_id(member_id):
        discount_cents = compute_loyalty_discount(member_id, total_cents)
        total_cents -= discount_cents
    new_order_id = len(orders) + 1
    order_code = generate_order_code(new_order_id)
    order = {
        "id": new_order_id,
        "order_code": order_code,
        "member_id": member_id,
        "status": "PAID",
        "total_cents": total_cents
    }
    orders.append(order)
    for item in cart:
        order_item = {
            "id": len(order_items) + 1,
            "order_id": new_order_id,
            "sku": item["sku"],
            "qty": item["qty"]
        }
        order_items.append(order_item)
        remove_from_inventory(item["sku"], item["qty"])
    if member_id and validate_member_id(member_id):
        award_loyalty_points(member_id, total_cents)
    print(f"Order {order_code} finalized. Total: ${total_cents / 100:.2f}")
    return order


# validate_member_id(member_id) -> bool
def validate_member_id(member_id):
    for customer in customers:
        if customer["member_id"] == member_id:
            return True
    return False


# compute_loyalty_discount(member_id, total_cents) -> discount_cents
def compute_loyalty_discount(member_id, total_cents):
    customer = next((c for c in customers if c["member_id"] == member_id), None)
    if customer is None:
        return 0
    tier = customer.get("tier", "NONE")
    discount_rates = {
        "NONE": 0.00,
        "SILVER": 0.05,
        "GOLD": 0.10
    }
    return round(total_cents * discount_rates.get(tier, 0.00))


# award_loyalty_points(member_id, total_cents) -> int
customers = {
    "CUST123": {"member_id": "CUST123", "name": "Alice", "tier": "GOLD", "points": 1500},
    "CUST456": {"member_id": "CUST456", "name": "Bob", "tier": "SILVER", "points": 400},
}

def award_loyalty_points(member_id, total_cents):
    if member_id not in customers:
        print("Customer not found.")
        return None
    points_earned = total_cents // 100
    customers[member_id]["points"] += points_earned
    print("Added", points_earned, "points to", customers[member_id]["name"])
    print("Total points now:", customers[member_id]["points"])
    return customers[member_id]["points"]


# validate_return_eligibility(order_id, return_items) -> bool
def validate_return_eligibility(order_id, return_items):
    order = next((o for o in orders if o["id"] == order_id), None)
    if order is None:
        print(f"Order {order_id} not found.")
        return False
    if order["status"] != "PAID":
        print(f"Order {order_id} cannot be returned (status: {order['status']}).")
        return False
    for return_item in return_items:
        sku = return_item["sku"]
        qty = return_item["qty"]
        order_item = next((oi for oi in order_items if oi["order_id"] == order_id and oi["sku"] == sku), None)
        if order_item is None:
            print(f"SKU {sku} not found in order {order_id}.")
            return False
        if order_item["qty"] < qty:
            print(f"Insufficient quantity of {sku} in order. Available: {order_item['qty']}, Requested: {qty}")
            return False
    return True


# calculate_refund_total(order_id, return_items) -> refund_cents
product_variants = {
    "SHIRT-RED-M": {"price_cents": 2500},
    "SHIRT-BLUE-L": {"price_cents": 2700},
}

order_items = [
    {"order_id": 1, "sku": "SHIRT-RED-M", "qty": 2},
    {"order_id": 1, "sku": "SHIRT-BLUE-L", "qty": 1},
]

def calculate_refund_total(order_id, return_items):
    total_refund = 0
    for item in return_items:
        sku = item["sku"]
        qty = item["qty"]
        if sku in product_variants:
            price = product_variants[sku]["price_cents"]
        else:
            print("SKU not found:", sku)
            continue
        refund_amount = price * qty
        total_refund += refund_amount
    return total_refund


# process_return(order_id, return_items) -> return_order
def process_return(order_id, return_items):
    if not validate_return_eligibility(order_id, return_items):
        print(f"Return for order {order_id} is not eligible.")
        return None
    refund_cents = calculate_refund_total(order_id, return_items)
    new_return_order_id = len(orders) + 1
    return_order_code = generate_order_code(new_return_order_id)
    original_order = next((o for o in orders if o["id"] == order_id), None)
    member_id = original_order["member_id"] if original_order else None
    return_order = {
        "id": new_return_order_id,
        "order_code": return_order_code,
        "member_id": member_id,
        "status": "RETURN",
        "total_cents": refund_cents
    }
    orders.append(return_order)
    for return_item in return_items:
        sku = return_item["sku"]
        qty = return_item["qty"]
        order_item = {
            "id": len(order_items) + 1,
            "order_id": new_return_order_id,
            "sku": sku,
            "qty": qty
        }
        order_items.append(order_item)
        inventory_movements.append({"sku": sku, "qty_change": qty})
    print(f"Return order {return_order_code} created. Refund: ${refund_cents / 100:.2f}")
    return return_order

#Project 02

# class ProductVariant
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
        self._active = False

    def get_price_dollars(self):
        return self._price_cents / 100.0

    def __str__(self):
        return f"{self._color} Shirt ({self._size}) - ${self.get_price_dollars():.2f}"


# class InventoryMovement
class InventoryMovement:
    def __init__(self, id, sku, qty_change):
        if not sku or not isinstance(qty_change, int):
            raise ValueError("Invalid inventory movement data")

        self._id = id
        self._sku = sku
        self._qty_change = qty_change

    @property
    def sku(self):
        return self._sku

    @property
    def qty_change(self):
        return self._qty_change

    def __str__(self):
        direction = "Added" if self._qty_change > 0 else "Removed"
        return f"{direction} {abs(self._qty_change)} units of {self._sku}"


# class Customer
class Customer:
    def __init__(self, id, member_id, name, tier, points=0):
        if not isinstance(id, int) or id <= 0:
            raise ValueError("id must be a positive int")
        if not member_id or not isinstance(member_id, str):
            raise ValueError("invalid member_id")
        if not name or not isinstance(name, str):
            raise ValueError("invalid name")
        if tier not in ["Bronze", "Silver", "Gold", "Platinum"]:
            raise ValueError("invalid tier")
        if not isinstance(points, int) or points < 0:
            raise ValueError("invalid points")
        self._id = id
        self._member_id = member_id
        self._name = name
        self._tier = tier
        self._points = points

    @property
    def id(self):
        return self._id

    @property
    def member_id(self):
        return self._member_id

    @property
    def name(self):
        return self._name

    @property
    def tier(self):
        return self._tier

    @tier.setter
    def tier(self, t):
        if t not in ["Bronze", "Silver", "Gold", "Platinum"]:
            raise ValueError("invalid tier")
        self._tier = t

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, p):
        if not isinstance(p, int) or p < 0:
            raise ValueError("invalid points")
        self._points = p

    def add_points(self, n):
        if n < 0:
            raise ValueError("negative points")
        self._points += n

    def redeem_points(self, n):
        if n < 0 or n > self._points:
            raise ValueError("invalid redeem")
        self._points -= n

    def upgrade_tier(self):
        tiers = ["Bronze", "Silver", "Gold", "Platinum"]
        i = tiers.index(self._tier)
        if i < len(tiers) - 1:
            self._tier = tiers[i + 1]

    def reset_points(self):
        self._points = 0

    def __str__(self):
        return f"{self._name} [{self._tier}] - {self._points} pts"

    def __repr__(self):
        return f"Customer({self._id}, '{self._member_id}', '{self._name}', '{self._tier}', {self._points})"


# class Order
class Order:
    def __init__(self, id, order_code, member_id, status, total_cents=0):
        if not isinstance(id, int) or id <= 0:
            raise ValueError("id must be a positive int")
        if not order_code or not isinstance(order_code, str):
            raise ValueError("invalid order_code")
        if not member_id or not isinstance(member_id, str):
            raise ValueError("invalid member_id")
        if status not in ["Pending", "Shipped", "Delivered", "Cancelled"]:
            raise ValueError("invalid status")
        if not isinstance(total_cents, int) or total_cents < 0:
            raise ValueError("invalid total_cents")
        self._id = id
        self._order_code = order_code
        self._member_id = member_id
        self._status = status
        self._total_cents = total_cents

    @property
    def id(self):
        return self._id

    @property
    def order_code(self):
        return self._order_code

    @property
    def member_id(self):
        return self._member_id

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, s):
        if s not in ["Pending", "Shipped", "Delivered", "Cancelled"]:
            raise ValueError("invalid status")
        self._status = s

    @property
    def total_cents(self):
        return self._total_cents

    @total_cents.setter
    def total_cents(self, t):
        if not isinstance(t, int) or t < 0:
            raise ValueError("invalid total_cents")
        self._total_cents = t

    def add_charge(self, cents):
        if cents < 0:
            raise ValueError("negative charge")
        self._total_cents += cents

    def apply_discount(self, cents):
        if cents < 0 or cents > self._total_cents:
            raise ValueError("invalid discount")
        self._total_cents -= cents

    def cancel_order(self):
        if self._status != "Cancelled":
            self._status = "Cancelled"

    def mark_shipped(self):
        if self._status == "Pending":
            self._status = "Shipped"

    def __str__(self):
        return f"Order {self._order_code} [{self._status}] - ${self._total_cents/100:.2f}"

    def __repr__(self):
        return f"Order({self._id}, '{self._order_code}', '{self._member_id}', '{self._status}', {self._total_cents})"



#PROJECT 03 
from abc import ABC, abstractmethod


# Abstract Product & Subclasses

class AbstractProduct(ABC):
    def __init__(self, sku, price_cents):
        self._sku = sku
        self._price_cents = price_cents

    @abstractmethod
    def get_description(self):
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


# Cart Class
class Cart:
    def __init__(self):
        self.items = []  
    def add_item(self, product, qty):
        self.items.append((product, qty))

    def total_price_cents(self):
        return sum(prod._price_cents * qty for prod, qty in self.items)

    def print_receipt(self):
        for prod, qty in self.items:
            print(f"{prod.get_description()} x {qty} - ${prod.get_price_dollars() * qty:.2f}")
        print(f"Total: ${self.total_price_cents() / 100:.2f}")

# Reward Strategy Pattern
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


# Customer and Order Classes
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

# Loyalty Program Class

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

