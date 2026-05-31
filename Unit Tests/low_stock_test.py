import unittest
from logic import is_low_stock

class TestIsLowStock(unittest.TestCase):
    def test_below_threshold(self):
        self.assertTrue(is_low_stock(3, 5))

    def test_above_threshold(self):
        self.assertFalse(is_low_stock(10, 5))

    def test_exact_threshold(self):
        self.assertTrue(is_low_stock(5, 5))

    def test_zero_quantity(self):
        self.assertTrue(is_low_stock(0, 5))

    def test_custom_threshold(self):
        self.assertFalse(is_low_stock(8, 3))

if __name__ == '__main__':
    unittest.main()