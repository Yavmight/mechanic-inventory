import unittest
from logic import is_low_stock, get_low_stock_parts

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


class TestGetLowStockParts(unittest.TestCase):
    def setUp(self):
        self.parts = [
            {'name': 'Brake Pad',  'quantity': 2,  'low_stock_threshold': 5},
            {'name': 'Oil Filter', 'quantity': 10, 'low_stock_threshold': 5},
            {'name': 'Spark Plug', 'quantity': 4,  'low_stock_threshold': 10},
            {'name': 'Air Filter', 'quantity': 20, 'low_stock_threshold': 5},
        ]

    def test_returns_only_low_stock(self):
        result = get_low_stock_parts(self.parts)
        self.assertEqual(len(result), 2)

    def test_correct_parts_flagged(self):
        result = get_low_stock_parts(self.parts)
        names = [p['name'] for p in result]
        self.assertIn('Brake Pad', names)
        self.assertIn('Spark Plug', names)

    def test_empty_list(self):
        self.assertEqual(get_low_stock_parts([]), [])


if __name__ == '__main__':
    unittest.main()