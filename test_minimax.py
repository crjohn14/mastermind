
from itertools import permutations
from mastermind import minimax, remove_codes, random_guess

file_minimax = open('minimax.txt', 'w')

lvl_info = {'numGladiators': 4, 'numGuesses': 8, 'numRounds': 1, 'numWeapons': 7}
guess_set = set(permutations(range(lvl_info['numWeapons']), lvl_info['numGladiators']))
guess = random_guess(guess_set)
file_minimax.write('len(guess_set): {}'.format(len(guess_set)))
file_minimax.write('Guess: {}'.format(guess))
guess_set2 = remove_codes(guess_set, guess, [4,2])
file_minimax.write('remove_codes(guess_set, guess, [4,2])')
file_minimax.write('len(guess_set): {}'.format(len(guess_set2)))
guess_mini = minimax(guess_set2, lvl_info['numGladiators'])
file_minimax.write('minimax guess: {}'.format(guess_mini))