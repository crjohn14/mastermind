
from itertools import permutations, combinations
from mastermind import minimax, remove_codes, remove_codes_4, determine_weapons, random_guess



lvl_info = {'numGladiators': 2, 'numGuesses': 8, 'numRounds': 1, 'numWeapons': 5}
guess_set = set(permutations(range(lvl_info['numWeapons']), lvl_info['numGladiators']))
guess = random_guess(guess_set)
print(guess_set)
print('len(guess_set): {}'.format(len(guess_set)))
print('Guess: {}'.format(guess))
guess_set2 = remove_codes(guess_set, guess, [1,0])
print('len(guess_set): {}'.format(len(guess_set2)))
guess_mini = minimax(guess_set2, lvl_info['numGladiators'])
print('minimax guess: {}'.format(guess_mini))
