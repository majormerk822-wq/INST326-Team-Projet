# check_inventory(sku) -> int
def check_inventory(sku):
    """
    Returns the current stock level of the given SKU.
    """
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
