#Database Dictionaries 
product_variants [id, sku, size, color, prie_cents, active]
inventory_movements [id, sku, qty_change]
customers [id, member_id name, tier, points]
orders [id, order_code, member_id, status, total_cents]
order_items [id, order_id, sku, qty]


#INVENTORY FUNCTIONS 
check_inventory(sku) -> int
add_to_inventory(sku, qty) -> dict
remove_from_inventory(sku, qty) -> dict
calculate_stock_level(sku) -> int
is_product_in_stock(sku, qty) -> bool


#SALES FUNCTIONS
scan_item(cart, sku) -> list
calculate_cart_total(cart) -> total_cents
generate_order_code(order_id) -> string
finalize_sale(cart, member_id=None) -> order


#CUSTOMER LOYALTY FUNCTIONS 
validate_member_id(member_id) -> bool
compute_loyalty_discount(member_id, total_cents) -> discount_cents
award_loyalty_points(member_id, total_cents) -> int



# RETURNS / EXCHANGES FUNCTIONS 
validate_return_eligibility(order_id, return_items) -> bool
calculate_refund_total(order_id, return_items) -> refund_cents
process_return(order_id, return_items) -> return_order
