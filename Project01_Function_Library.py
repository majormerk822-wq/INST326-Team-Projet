#Database Dictionaries 
product_variants [id, sku, size, color, prie_cents, active]
inventory_movements [id, sku, qty_change]
customers [id, member_id, name, tier, points]
orders [id, order_code, member_id, status, total_cents]
order_items [id, order_id, sku, qty]


#INVENTORY FUNCTIONS 
check_inventory(sku) -> int 
def check_inventory(sku):
    """
    Returns the current stock level of the given SKU.
    """
    total = 0
    for movement in inventory_movements:
        if movement["sku"] == sku:
            total += movement["qty_change"]
    return total

add_to_inventory(sku, qty) -> dict
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
    
remove_from_inventory(sku, qty) -> dict

calculate_stock_level(sku) -> int

is_product_in_stock(sku, qty) -> bool
inventory_movements = [
    {"sku": "SHIRT-RED-M", "qty_change": 10},
    {"sku": "SHIRT-BLUE-L", "qty_change": 5},
]

def calculate_stock_level(sku):
    """Add up all stock movements for one product."""
    total = 0
    for move in inventory_movements:
        if move["sku"] == sku:
            total = total + move["qty_change"]
    return total


def is_product_in_stock(sku, qty):
    """
    Check if the given product has at least 'qty' available.
    Returns True if enough stock, False otherwise.
    """
    current_stock = calculate_stock_level(sku)

    if current_stock >= qty:
        return True
    else:
        return False


#SALES FUNCTIONS
scan_item(cart, sku) -> list
def scan_item(cart, sku):
    """
    Adds a product to the cart by SKU.
    If it's already in the cart, increment the quantity.
    """
    # Check if product exists and is active
    product = next((p for p in product_variants if p["sku"] == sku and p["active"]), None)
    if product is None:
        raise ValueError(f"Product with SKU '{sku}' not found or inactive.")

    # Check if SKU is already in the cart
    for item in cart:
        if item["sku"] == sku:
            item["qty"] += 1
            return cart

    # If not in cart, add it with qty = 1
    cart.append({
        "sku": sku,
        "price_cents": product["price_cents"],
        "qty": 1
    })

    return cart

calculate_cart_total(cart) -> total_cents
def calculate_cart_total(cart):
    """
    Returns the total price (in cents) of all items in the cart.
    """
    total = 0
    for item in cart:
        total += item["qty"] * item["price_cents"]
    return total

generate_order_code(order_id) -> string
def generate_order_code(order_id):
    if order_id < 0:
        print("Order ID must be positive.")
        return None

    order_str = str(order_id)

    while len(order_str) < 4:
        order_str = "0" + order_str

    order_code = "ORD-" + order_str

    return order_code
finalize_sale(cart, member_id=None) -> order


#CUSTOMER LOYALTY FUNCTIONS 
validate_member_id(member_id) -> bool
def validate_member_id(member_id):
    """
    Returns True if a customer with the given member_id exists.
    """
    for customer in customers:
        if customer["member_id"] == member_id:
            return True
    return False

compute_loyalty_discount(member_id, total_cents) -> discount_cents
def compute_loyalty_discount(member_id, total_cents):
    """
    Returns the discount (in cents) for a member based on their loyalty tier.
    """
    # Find the customer
    customer = next((c for c in customers if c["member_id"] == member_id), None)
    if customer is None:
        return 0

    # Get tier and discount rate
    tier = customer.get("tier", "NONE")
    discount_rates = {
        "NONE": 0.00,
        "SILVER": 0.05,
        "GOLD": 0.10
    }
    rate = discount_rates.get(tier, 0.00)

    return round(total_cents * rate)

award_loyalty_points(member_id, total_cents) -> int
customers = {
    "CUST123": {"member_id": "CUST123", "name": "Alice", "tier": "GOLD", "points": 1500},
    "CUST456": {"member_id": "CUST456", "name": "Bob", "tier": "SILVER", "points": 400},
}

def award_loyalty_points(member_id, total_cents):
    """
    Add loyalty points to a customer.
    1 point is earned for every $1 spent.
    (100 cents = 1 dollar)

    member_id: customer ID
    total_cents: total amount spent in cents
    """
    if member_id not in customers:
        print("Customer not found.")
        return None

    points_earned = total_cents // 100   

    customers[member_id]["points"] = customers[member_id]["points"] + points_earned

    print("Added", points_earned, "points to", customers[member_id]["name"])
    print("Total points now:", customers[member_id]["points"])

    return customers[member_id]["points"]


validate_return_eligibility(order_id, return_items) -> bool

calculate_refund_total(order_id, return_items) -> refund_cents
product_variants = {
    "SHIRT-RED-M": {"price_cents": 2500},  
    "SHIRT-BLUE-L": {"price_cents": 2700}, 
}

order_items = [
    {"order_id": 1, "sku": "SHIRT-RED-M", "qty": 2},
    {"order_id": 1, "sku": "SHIRT-BLUE-L", "qty": 1},
]


def calculate_refund_total(order_id, return_items):
    """
    Compute how much to refund (in cents) for the returned items.

    order_id: which order the return belongs to
    return_items: list of {"sku": ..., "qty": ...}
    """
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
        total_refund = total_refund + refund_amount

    return total_refund
process_return(order_id, return_items) -> return_order


