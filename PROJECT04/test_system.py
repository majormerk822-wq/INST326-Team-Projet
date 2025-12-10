# system_tests.py

import unittest
from store_system import Shirt, Mug, Cart, Customer, Order, GoldReward, LoyaltyProgram

class TestSystemWorkflow(unittest.TestCase):

    def test_complete_sale_with_loyalty(self):
        # Step 1: Create products
        shirt = Shirt("SHIRT-RED-M", 2500, "M", "Red")
        mug = Mug("MUG-WHITE-12", 1200, 12)

        # Step 2: Create and fill cart
        cart = Cart()
        cart.add_item(shirt, 1)
        cart.add_item(mug, 2)

        # Step 3: Checkout simulation
        total = cart.total_price_cents()
        self.assertEqual(total, 2500 + 1200 * 2)

        # Step 4: Create customer and order
        customer = Customer(1, "CUST789", "Charlie", "Gold", 0)
        order = Order(1, "ORD-0001", "CUST789", "Delivered", total)

        # Step 5: Apply loyalty program
        program = LoyaltyProgram(GoldReward())
        program.add_customer(customer)
        program.add_order(order)
        earned_points = program.apply_points("ORD-0001")

        # Gold tier earns 2x points
        expected_points = (total // 100) * 2
        self.assertEqual(earned_points, expected_points)
        self.assertEqual(customer.points, expected_points)

        # Optional: print for visibility
        print(f"Customer {customer.name} earned {earned_points} points on ${total/100:.2f} purchase.")

if __name__ == "__main__":
    unittest.main()



def test_return_workflow(self):
    # Step 1: Add item to inventory and customer to system
    add_to_inventory("SHIRT-RED-M", 10)
    customer = Customer(1, "CUST999", "David", "Silver", 0)

    # Step 2: Build cart and finalize order
    cart = Cart()
    shirt = Shirt("SHIRT-RED-M", 2500, "M", "Red")
    cart.add_item(shirt, 2)
    order = finalize_sale(cart_data_to_dict(cart), member_id="CUST999")

    # Step 3: Simulate return
    return_items = [{"sku": "SHIRT-RED-M", "qty": 2}]
    return_order = process_return(order["id"], return_items)

    # Step 4: Assertions
    self.assertIsNotNone(return_order)
    self.assertEqual(return_order["status"], "RETURN")
    self.assertEqual(return_order["total_cents"], 2500 * 2)

    # Inventory should be replenished
    new_stock = calculate_stock_level("SHIRT-RED-M")
    self.assertGreaterEqual(new_stock, 10)

    # Optional: Print for visibility
    print(f"Return {return_order['order_code']} processed. Refund: ${return_order['total_cents'] / 100:.2f}")



def test_inventory_limit_and_successful_purchase(self):
    # Step 1: Add limited stock to inventory
    add_to_inventory("SHIRT-RED-M", 2)

    # Step 2: Attempt to buy more than in stock (should fail)
    cart = Cart()
    shirt = Shirt("SHIRT-RED-M", 2500, "M", "Red")
    cart.add_item(shirt, 3)  # trying to add 3, but only 2 in stock

    can_fulfill = is_product_in_stock(shirt.sku, 3)
    self.assertFalse(can_fulfill)

    # Step 3: Now build valid cart within stock
    cart = Cart()
    cart.add_item(shirt, 2)

    can_fulfill = is_product_in_stock(shirt.sku, 2)
    self.assertTrue(can_fulfill)

    # Step 4: Register customer and finalize order
    customer = Customer(2, "CUST777", "Erica", "Gold", 0)
    total = cart.total_price_cents()
    order = finalize_sale(cart_data_to_dict(cart), member_id="CUST777")

    # Step 5: Apply loyalty program
    program = LoyaltyProgram(GoldReward())
    program.add_customer(customer)
    program.add_order(order)
    earned = program.apply_points(order["order_code"])

    # Step 6: Assert everything updated
    self.assertEqual(earned, (total // 100) * 2)
    self.assertEqual(customer.points, earned)
    self.assertEqual(calculate_stock_level("SHIRT-RED-M"), 0)

    # Optional: print for visibility
    print(f"Order {order['order_code']} for {customer._name}: {earned} points earned.")
