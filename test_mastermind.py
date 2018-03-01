import unittest
from itertools import permutations, combinations
from mastermind import minimax, remove_codes, remove_codes_4, determine_weapons, random_guess

class MyTest(unittest.TestCase):

    def test_remove_codes_1(self):
        guess_set = set(permutations([1, 2, 3], 3))
        new_set = remove_codes(guess_set, (2, 3, 1), [3, 1])
        answer = set([(1, 3, 2), (2, 1, 3), (3, 2, 1)])
        self.assertEqual(new_set, answer)

    def test_remove_codes_2(self):
        guess_set = set(permutations([1, 2, 3, 4], 3))
        new_set = remove_codes(guess_set, (2, 3, 1), [2, 1])
        answer = set([(4,3,2), (3,4,1), (2,4,3), (2,1,4), (4,2,1), (1,3,4)])
        self.assertEqual(new_set, answer)

    def test_remove_codes_3(self):
        guess_set = set(permutations([1, 2, 3, 4], 3))
        new_set = remove_codes(guess_set, (2, 3, 1), [2, 2])
        answer = set([(2,3,4), (4,3,1), (2,4,1)])
        self.assertEqual(new_set, answer)

    def test_remove_codes_4_1(self):
        weapon_set = set(combinations([1,2,3,4], 3))
        new_set = remove_codes_4(weapon_set, (1, 2, 3), [2, 1])
        answer = set([(2,3,4), (1,2,4), (1,3,4)])
        self.assertEqual(new_set, answer)

    def test_remove_codes_4_2(self):
        weapon_set = set(combinations([1,2,3,4,5], 3))
        new_set = remove_codes_4(weapon_set, (1, 2, 3), [2, 1])
        answer = set([(2,3,4), (1,2,4), (1,3,4), (1,3,5), (2,3,5), (1,2,5)])
        self.assertEqual(new_set, answer)

    def test_remove_codes_4_3(self):
        weapon_set = set(combinations([1,2,3,4,5,6], 3))
        new_set = remove_codes_4(weapon_set, (1, 2, 3), [2, 1])
        answer = set([(2,3,4), (1,2,4), (1,3,4), (1,3,5), (2,3,5), (1,2,5), (2,3,6), (1,3,6), (1,2,6)])
        self.assertEqual(new_set, answer)



if __name__ == '__main__':
    unittest.main()