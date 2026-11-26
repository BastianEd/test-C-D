import unittest

class TestBasico(unittest.TestCase):
    def test_ok(self):
        self.assertEqual(1 + 1, 2)

if __name__ == '__main__':
    unittest.main()
