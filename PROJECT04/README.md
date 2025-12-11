# Clothing Store Management System

A Python-based system for managing **inventory, sales, loyalty rewards, and returns** for a clothing store.  
Supports shirts, mugs, SKU-based stock tracking, tiered rewards, and JSON data persistence.

---

## Overview

Retail stores often struggle with stock accuracy, loyalty tracking, and consistent sales/returns handling.  
This project solves these problems by providing:

- OOP models for **Products**, **Customers**, **Orders**, **Rewards**
- Functional tools for **inventory**, **returns**, and **checkout**
- A **Strategy-based loyalty system** (Bronze / Silver / Gold / Platinum)
- Simple **JSON persistence** for saving store data
- A full **unit + integration test suite**

---

## Team Members

| Name | Role |
|------|------|
| **Major Thompson** | Product models, loyalty system, integration tests, docs |
| **Ricardo Koenig** | Cart & POS logic, inventory helpers, workflow tests |
| **Ashwin Pugazhendhi** | Returns/refunds, persistence, documentation |

---

## Installation

python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows
No external packages required.

📁 Project Structure
kotlin

clothing-store-system/
├── store_system.py
├── testone.py
├── system_tests.py
├── test_integration.py
└── data/
Basic Usage
Create products & cart
python

from store_system import Shirt, Mug, Cart

shirt = Shirt("SHIRT-RED-M", 2500, "M", "Red")
mug = Mug("MUG-WHITE-12", 1200, 12)

cart = Cart()
cart.add_item(shirt, 2)
cart.add_item(mug, 1)
print(cart.total_price_cents())
Loyalty program
python

from store_system import Customer, Order, GoldReward, LoyaltyProgram

customer = Customer(1, "M001", "Alice", "Gold", 0)
order = Order(1, "O100", "M001", "Delivered", 6200)

program = LoyaltyProgram(GoldReward())
program.add_customer(customer)
program.add_order(order)
program.apply_points("O100")
Inventory & returns (functional API)
python

from store_system import add_to_inventory, scan_item, finalize_sale, process_return

add_to_inventory("SHIRT-RED-M", 10)
cart = []
scan_item(cart, "SHIRT-RED-M")
order = finalize_sale(cart, member_id="M001")

process_return(order["id"], [{"sku": "SHIRT-RED-M", "qty": 1}])
Architecture Summary
OOP Components

AbstractProduct, Shirt, Mug

ProductVariant, InventoryMovement

Customer, Order

Cart

Loyalty (Strategy Pattern)

RewardStrategy

BronzeReward, GoldReward, PlatinumReward

LoyaltyProgram

Functional Inventory & Sales

scan_item(), calculate_cart_total(), finalize_sale()

add_to_inventory(), remove_from_inventory()

validate_return_eligibility(), process_return()

Persistence

JSON save/load via save_all(), load_all()

Running Tests
bash

python -m unittest discover -v
Or individually:

bash

python testone.py
python system_tests.py
python test_integration.py
Test coverage includes:

Product descriptions & pricing

Cart totals

Loyalty point calculations

Sale workflow (cart → order → loyalty)

Inventory limits & returns

Inactive product blocking

Known Limitations
Uses global in-memory state (not ideal for large apps)

No GUI or CLI

JSON files instead of a real database

Some integration tests are TODOs

Future Enhancements
Migrate to a structured database

Add CLI or web UI (Flask / FastAPI)

Expand promotions/coupons

Improve error handling

More complete persistence and integration tests
