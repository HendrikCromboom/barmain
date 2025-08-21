import unittest
import server

class TestMain(unittest.TestCase):
    def test_something(self):
        self.assertEqual(server.something("something"), "something something something")

if __name__ == "__main__":
    unittest.main()

