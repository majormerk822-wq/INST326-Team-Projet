# Clothing Store Management System

## Project Title and Description

This project is a Python-based inventory and sales system for a department store that sells **shirts only**. The program allows the store to track inventory, handle transactions, apply loyalty discounts, and manage product returns efficiently.

---

## 👥 Team Member Names and Roles

- **Major Thompson** — Inventory Functions /Loyalty Functions & Documentation  
- **Ricardo Koenig** — Sales Functions /Loyalty Functions & Documentation  
- **Ashwin Pugazhendhi** — Returns/Exchanges Functions /Loyalty Functions & Documentation  

---

## 🧠 Domain Focus and Problem Statement

### Domain Focus:
Retail inventory and point-of-sale systems for department stores.

### Problem Statement:
Clothing companies often struggle with:

- Knowing how much stock they have  
- Tracking which items are selling  
- Handling returns and stockouts  
- Keeping consistent sales records  
- Managing loyalty programs and discounts  

This project solves these problems using a logical function-based Python system.

---

## Usage Examples for Key Functions

```python
# Scan a product into the cart
cart = []
cart = scan_item(cart, "SHIRT-RED-M")

# Check inventory
stock = check_inventory("SHIRT-RED-M")

# Calculate total
total = calculate_cart_total(cart)

# Finalize sale
order = finalize_sale(cart, member_id="CUST123")

# Validate member
valid = validate_member_id("CUST123")

# Apply loyalty discount
discount = compute_loyalty_discount("CUST123", 5000)
```

---

## Function Library Overview and Organization

### Inventory Functions
- `check_inventory(sku)`
- `add_to_inventory(sku, qty)`
- `remove_from_inventory(sku, qty)`
- `calculate_stock_level(sku)`
- `is_product_in_stock(sku, qty)`

### Sales Functions
- `scan_item(cart, sku)`
- `calculate_cart_total(cart)`
- `generate_order_code(order_id)`
- `finalize_sale(cart, member_id=None)`

### Customer Loyalty Functions
- `validate_member_id(member_id)`
- `compute_loyalty_discount(member_id, total_cents)`
- `award_loyalty_points(member_id, total_cents)`

### Returns & Exchanges Functions
- `validate_return_eligibility(order_id, return_items)`
- `calculate_refund_total(order_id, return_items)`
- `process_return(order_id, return_items)`

---

##  Contribution Guidelines for Team Members

- Each team member is responsible for 3–5 functions.
- Follow PEP 8 and use meaningful names.
-Clear communication with entire team
