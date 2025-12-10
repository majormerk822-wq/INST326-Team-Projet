# testone.py

import unittest
from store_system import Shirt, Mug, Cart, Customer, Order, GoldReward, LoyaltyProgram

class TestProductClasses(unittest.TestCase):

    def test_shirt_description(self):
        shirt = Shirt("SHIRT-RED-M", 2500, "M", "Red")
        self.assertEqual(shirt.get_description(), "Red Shirt (Size M)")
        self.assertEqual(shirt.get_price_dollars(), 25.00)

    def test_mug_description(self):
        mug = Mug("MUG-WHITE-12", 1200, 12)
        self.assertEqual(mug.get_description(), "Mug - 12 oz")
        self.assertEqual(mug.get_price_dollars(), 12.00)


class TestCart(unittest.TestCase):

    def test_cart_total_price(self):
        cart = Cart()
        shirt = Shirt("SHIRT-RED-M", 2500, "M", "Red")
        mug = Mug("MUG-WHITE-12", 1200, 12)
        cart.add_item(shirt, 2)
        cart.add_item(mug, 1)
        self.assertEqual(cart.total_price_cents(), 2500 * 2 + 1200)

    def test_cart_empty(self):
        cart = Cart()
        self.assertEqual(cart.total_price_cents(), 0)


class TestLoyaltyProgram(unittest.TestCase):

    def test_apply_points_gold_reward(self):
        c = Customer(1, "M001", "Alice", "Gold", 0)
        o = Order(1, "O100", "M001", "Delivered", 5000)
        program = LoyaltyProgram(GoldReward())
        program.add_customer(c)
        program.add_order(o)
        earned = program.apply_points("O100")
        self.assertEqual(earned, 100)  # 5000 // 100 * 2
        self.assertEqual(c.points, 100)


if __name__ == "__main__":
    unittest.main()


