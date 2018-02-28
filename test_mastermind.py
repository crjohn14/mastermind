import unittest
from itertools import permutations, combinations
from mastermind import minimax, remove_codes, remove_codes_4, determine_weapons, random_guess

class MyTest(unittest.TestCase):

    def test_remove_codes1(self):
        guess_set = set(permutations([1, 2, 3], 3))
        new_set = remove_codes(guess_set, (2, 3, 1), [3, 1])
        answer = set([(1, 3, 2), (2, 1, 3), (3, 2, 1)])
        self.assertEqual(new_set, answer)

    def test_remove_codes2(self):
        guess_set = set(permutations([1, 2, 3, 4], 3))
        new_set = remove_codes(guess_set, (2, 3, 1), [2, 1])
        answer = set([(4,3,2), (3,4,1), (2,4,3), (2,1,4), (4,2,1), (1,3,4)])
        self.assertEqual(new_set, answer)



if __name__ == '__main__':
    unittest.main()