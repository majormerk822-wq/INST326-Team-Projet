import unittest
from store_system import Shirt, Mug, Cart, Customer, Order, GoldReward, LoyaltyProgram, inventory_movements, remove_from_inventory

class TestIntegration(unittest.TestCase):

    def test_cart_order_loyalty_flow(self):
        cart = Cart()
        shirt = Shirt("SHIRT-RED-M", 2500, "M", "Red")
        mug = Mug("MUG-WHITE-12", 1200, 12)
        cart.add_item(shirt, 2)
        cart.add_item(mug, 1)

        # Customer and Order
        c = Customer(1, "M001", "Alice", "Gold", 0)
        o = Order(1, "O100", "M001", "Delivered", cart.total_price_cents())

        # Loyalty Program
        program = LoyaltyProgram(GoldReward())
        program.add_customer(c)
        program.add_order(o)

        earned = program.apply_points("O100")

        self.assertEqual(earned, 124)
        self.assertEqual(c.points, 124)

    def test_finalize_sale_reduces_inventory(self):
        # TODO: add test that calls finalize_sale() and checks inventory
        pass

    def test_process_return_increases_inventory(self):
        # TODO: create an order, return it, and check stock level goes up
        pass

    def test_discount_applied_for_gold_customer(self):
        # TODO: simulate gold customer order, verify discount is applied
        pass

    def test_scan_item_adds_to_cart_correctly(self):
        # TODO: use scan_item() to simulate scanning a SKU into the cart
        pass


if __name__ == "__main__":
    unittest.main()





def test_order_discount_inventory_loyalty(self):
    # Setup product and inventory
    inventory_movements.clear()
    inventory_movements.extend([
        {"sku": "SHIRT-BLUE-L", "qty_change": 5},
    ])
    product_variants["SHIRT-BLUE-L"] = {
        "sku": "SHIRT-BLUE-L",
        "price_cents": 2700,
        "active": True
    }

    # Setup customer with Silver tier (5% discount)
    customers["CUST456"] = {
        "member_id": "CUST456",
        "name": "Bob",
        "tier": "SILVER",
        "points": 400
    }

    # Create cart and scan item
    cart = []
    scan_item(cart, "SHIRT-BLUE-L")  # 1 x $27.00

    # Finalize sale
    order = finalize_sale(cart, member_id="CUST456")

    # Expect discount: 5% of $27.00 = $1.35 → total should be $25.65 = 2565 cents
    self.assertEqual(order["total_cents"], 2565)

    # Inventory should have decreased by 1
    stock = calculate_stock_level("SHIRT-BLUE-L")
    self.assertEqual(stock, 4)

    # Loyalty points earned should be floor(2565 / 100) = 25
    self.assertEqual(customers["CUST456"]["points"], 425)



def test_process_return_flow(self):
    # Reset inventory, orders, and order items
    inventory_movements.clear()
    orders.clear()
    order_items.clear()

    # Setup inventory and product
    inventory_movements.append({"sku": "SHIRT-RED-M", "qty_change": 5})
    product_variants["SHIRT-RED-M"] = {
        "sku": "SHIRT-RED-M",
        "price_cents": 2500,
        "active": True
    }

    # Place an order (simulate purchase of 2 shirts)
    cart = []
    scan_item(cart, "SHIRT-RED-M")
    scan_item(cart, "SHIRT-RED-M")
    order = finalize_sale(cart)

    original_stock = calculate_stock_level("SHIRT-RED-M")  # Should be 3 now
    self.assertEqual(original_stock, 3)

    # Process return of 1 item
    return_items = [{"sku": "SHIRT-RED-M", "qty": 1}]
    return_order = process_return(order_id=order["id"], return_items=return_items)

    # Check return order status and amount
    self.assertEqual(return_order["status"], "RETURN")
    self.assertEqual(return_order["total_cents"], 2500)

    # Check inventory is restocked (should go back up to 4)
    new_stock = calculate_stock_level("SHIRT-RED-M")
    self.assertEqual(new_stock, 4)






def test_inactive_product_scan_blocked(self):
    # Setup a product and mark it inactive
    product_variants["SHIRT-BLUE-L"] = {
        "sku": "SHIRT-BLUE-L",
        "price_cents": 2700,
        "active": False  # Make it inactive
    }

    cart = []

    # Try to scan the inactive product
    with self.assertRaises(ValueError) as context:
        scan_item(cart, "SHIRT-BLUE-L")

    self.assertIn("not found or inactive", str(context.exception))


