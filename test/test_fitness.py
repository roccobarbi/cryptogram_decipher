import unittest
from src import calculate_fitness


class TestFitnessCaesar(unittest.TestCase):
    def test_calculate_no_errors(self):
        try:
            fitness = calculate_fitness("abcdefghijklmnopqrstuvwxyz", "en")
        except:
            self.fail("calculate_fitness raised an exception")

    def test_returns_a_number(self):
        fitness = calculate_fitness("abcdefghijklmnopqrstuvwxyz", "en")
        self.assertTrue(type(fitness) == float or type(fitness) == int, "calculate_fitness did not return a number")

    def test_higher_for_real_text(self):
        fitness_alphabet = calculate_fitness("abcdefghijklmnopqrstuvwxyz", "en")
        fitness_text = calculate_fitness("the quick brown fox jumps over the lazy dog")
        self.assertGreater(fitness_text, fitness_alphabet, "the fitness of the alphabet is higher than a real text")

    def test_real_higher_than_ciphered(self):
        fitness_ciphertext = calculate_fitness("wkh txlfn eurzq ira mxpsv ryhu wkh odcb grj", "en")
        fitness_plaintext = calculate_fitness("the quick brown fox jumps over the lazy dog")
        self.assertGreater(fitness_plaintext, fitness_ciphertext,
                           "the fitness of the ciphertext is higher than the real text")

    def test_partial_decode_in_the_middle(self):
        fitness_ciphertext = calculate_fitness("wkh txlfn eurzq ira mxpsv ryhu wkh odcb grj", "en")
        fitness_partialdecode = calculate_fitness("the wxlfn kurzq ira mxpsv ryhu the odcb grj", "en")
        fitness_plaintext = calculate_fitness("the quick brown fox jumps over the lazy dog")
        print(str(fitness_ciphertext))
        print(str(fitness_partialdecode))
        print(str(fitness_plaintext))
        self.assertGreater(fitness_plaintext, fitness_partialdecode,
                           "the fitness of the partial decode is higher than the real text")
        self.assertGreater(fitness_partialdecode, fitness_ciphertext,
                           "the fitness of the ciphertext is higher than the partial decode")


if __name__ == '__main__':
    unittest.main()
