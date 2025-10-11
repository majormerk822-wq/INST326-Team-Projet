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
remove_from_inventory(sku, qty) -> dict
calculate_stock_level(sku) -> int
is_product_in_stock(sku, qty) -> bool


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

    # Calculate and return rounded discount
    return round(total_cents * rate)

award_loyalty_points(member_id, total_cents) -> int



# RETURNS / EXCHANGES FUNCTIONS 
validate_return_eligibility(order_id, return_items) -> bool
calculate_refund_total(order_id, return_items) -> refund_cents
process_return(order_id, return_items) -> return_order
