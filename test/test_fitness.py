import unittest
from src import calculate_fitness


class TestFitnessCaesar(unittest.TestCase):
    def test_calculate_no_errors(self):
        try:
            fitness = calculate_fitness("abcdefghijklmnopqrstuvwxyz", "en")
            print(str(fitness))
        except:
            self.fail("calculate_fitness raised an exception")


if __name__ == '__main__':
    unittest.main()
