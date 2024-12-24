import unittest
from app.main import add, subtract

class TestMathOperations(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(1, 2), 3)
        self.assertEqual(add(-2, 1), -1)

    def test_subtract(self):
        self.assertEqual(subtract(2, 1), 1)
        self.assertEqual(subtract(0, 0), 0)

if __name__ == '__main__':
    unittest.main()