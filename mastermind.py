"""Solution for Praetorians's Mastermind Challenge
Chris Johnson
Date: 21 Feb 2018

The challenge is a variation of the board game Mastermind in which 1 player creates a code and the other player guesses
until the code is found or they run out of turns.  After each guess they are told how many code elements were correct
and how many code positions were correct.  This version simulates fighting a number of gladiators, each of which are
weak to a specific weapon.  The player is given the number of gladiators and the number of possible weapons at the start
of each level.  The player is told how many gladiators were defeated and how many weapons were correct after each guess.

https://www.praetorian.com/challenges/mastermind

This solution utilizes a variation of Knuth's 5-guess algorithm .
(https://en.wikipedia.org/wiki/Mastermind_(board_game)#Algorithms)

The algorithm:
1. Build a set, S, of all possible permutations
2. Randomly select a guess from S
3. Submit the guess and get a response
4. If the guess was correct, then continue to the next level
5. Else, Remove all codes from S that would not give the same response
6. Repeat from step 2

Minimax was found to not be necessary when selecting guesses.  Initial testing showed that my implementation of minimax
gave a similar minimum for each guess which made it just waste time.

Level 4 requires a different strategy due to the ~128 million permutations (although it was fun to watch my RAM fill up
before the program crashed).  First the correct set of weapons is determined by guessing from a set of all possible
weapon combinations, which is only 177,100.  Once the correct set of weapons is determined, further guesses are made
from permutations of only those weapons.

Maintaining an open TCP connection was key to completing levels 5 and 6.  Requests would occasionally take longer than
the 10 second timeout period without using a requests session object.
"""

import sys, random, time
from itertools import permutations, combinations
from call_api import post_reset, post_guess, init_header, get_level, get_hash

def main():
    # check Python version
    if sys.version_info < (3, 0):
        sys.exit('Python version < 3.0 does not support modern TLS versions. You will have trouble connecting to our API using Python 2.X.')

    init_header()
    post_reset()

    done = False
    level = 1
    while(not done):
        lvl_info = get_level(level)

        if 'numWeapons' in lvl_info:
            print_level_info(level, lvl_info)
        elif 'error' in lvl_info:
            print(lvl_info['error'])
            # check for win
            if level > 6:
                hash_json = get_hash()
                print(hash_json)
                if 'hash' in hash_json:
                    file_hash = open('hash.txt', 'w')
                    file_hash.write(hash_json['hash'])
                    file_hash.close()
                    sys.exit(0)
            continue
        elif 'hash' in lvl_info:
            print('Victory is yours!!!')
            print('Hash: {}'.format(lvl_info['hash']))
            done = True
        else:
            print('Did not expect result from level request.  Code more...')
            print(lvl_info)
            sys.exit(0)

        # fight the gladiators!
        if level != 4:
            # build set of possible permutations, guess, check, remove from set and repeat if necessary
            guess_set = set(permutations(range(lvl_info['numWeapons']), lvl_info['numGladiators']))
            level += fight_gladiators(guess_set, level, lvl_info)
        else:
            # determine the correct weapons in level 4 from weapon combinations
            weapon_set = set(combinations(range(lvl_info['numWeapons']), lvl_info['numGladiators']))
            correct_weapons = determine_weapons(weapon_set, level)
            print('correct weapons: {}\n'.format(correct_weapons))
            if correct_weapons == ():
                continue
            # build permutations with only correct weapons
            guess_set = set(permutations(correct_weapons, lvl_info['numGladiators']))
            level += fight_gladiators(guess_set, level, lvl_info)

    sys.exit(0)

def print_level_info(level, lvl_info):
    """Print level information"""
    print()
    print('LEVEL {0}'.format(level))
    print('rounds: {0[numRounds]:d}'.format(lvl_info))
    print('guesses: {0[numGuesses]:d}'.format(lvl_info))
    print('weapons: {0[numWeapons]:d}'.format(lvl_info))
    print('gladiators: {0[numGladiators]:d}\n'.format(lvl_info))

def random_guess(guess_set):
    """Choose a random guess from the guess set"""
    return random.sample(guess_set, 1)[0]

def remove_codes(code_set, guess, response):
    """Remove codes from the code_set if they wouldn't give the same response

    Args:
        code_set: set of codes to filter
        guess: the guess that produced response
        response: the APIs response to guess

    Returns:
        set: new set with codes removed
    """
    correct_weapons = response[0]
    correct_gladiators = response[1]
    new_code_set = set(code_set)
    for code in code_set:
        # test code weapons
        if correct_weapons != len(set(code) & set(guess)):
            new_code_set.remove(code)
        else:
            # test code positions (gladiators)
            count = 0
            for pos in range(0, len(code)):
                if guess[pos] == code[pos]:
                    count += 1
            if correct_gladiators != count:
                new_code_set.remove(code)
    return new_code_set

def fight_gladiators(guess_set, level, lvl_info):
    """Choose a random element from the guess set, post guess, receive judgement, then update the set if necessary

    Args:
        guess_set: set to choose a guess from
        level: current level
        lvl_info: response from get_level
        headers: header for API

    Returns:
        int: level increment
    """
    while (True):
        # random guess from the set
        guess = random_guess(guess_set)
        print("Guess set size: {}".format(len(guess_set)))
        print("Guess: {}".format(guess))
        # accept judgement from the mastermind
        judgement = post_guess(level, guess)

        if 'response' in judgement:
            # print judgement
            print('correct weapons: {0} / {1}'.format(judgement['response'][0], lvl_info['numGladiators']))
            print('correct gladiators: {0} / {1}\n'.format(judgement['response'][1], lvl_info['numGladiators']))
            # remove guesses from guess_set that wouldn't give the same judgement
            guess_set = remove_codes(guess_set, guess, judgement['response'])
        elif 'error' in judgement:
            # error; probably because 10 sec passed or no more guesses
            print(judgement['error'])
            return 0
        elif 'message' in judgement:
            # level complete
            print('YOU HAVE SLAIN YOUR OPPONENTS!!!')
            print(judgement['message'])
            return 1
        elif 'roundsLeft' in judgement:
            # accounts for extra rounds in levels > 4
            print('YOU HAVE SLAIN YOUR OPPONENTS!!!')
            print('Rounds left: {}'.format(judgement['roundsLeft']))
            return 0
        else:
            print('Judgement was not prepared for.  Code more...')
            print(judgement)
            sys.exit(0)

def determine_weapons(weapon_set, level):
    """level 4 - determine correct weapons"""
    count = 0
    print('Determining correct weapon set.')
    while (True):
        count += 1
        guess_weapons = list(random_guess(weapon_set))
        judgement = post_guess(level, guess_weapons)
        if 'response' in judgement:
            num_correct_weapons = judgement['response'][0]
            if num_correct_weapons == 6:
                print('Required {} guesses.'.format(count))
                return guess_weapons
            else:
                # remove guesses from guess set that wouldn't give the same judgement
                weapon_set = remove_codes_4(weapon_set, guess_weapons, judgement['response'])
        elif 'error' in judgement:
            # error; probably because 10 sec passed or no more guesses
            print(judgement['error'])
            return ()
        else:
            print('Judgement was not prepared for.  Code more...')
            print(judgement)
            sys.exit(0)

def remove_codes_4(code_set, guess, response):
    """level 4 - remove codes without considering position"""
    correct_weapons = response[0]
    new_code_set = set(code_set)
    for code in code_set:
        # test code weapons
        if correct_weapons != len(set(code) & set(guess)):
            new_code_set.remove(code)
    return new_code_set

def minimax(guess_set, num_gladiators):
    """minimax - calculate how many possibilities in the set would be eliminated for each possible response

    NOT IMPLEMENTED/INCOMPLETE - while testing it appeared that each response had the same minimum although the other
    scores were different.  Because minimax chooses the maximum minimum this algorithm would do nothing but waste time.
    TODO - Maybe choose the code with the highest average score?

    Returns:
        tuple: code with highest minimum score
    """
    ret = ()
    ret_score = 0
    for code in guess_set:
        score = 1000000
        print('code: {}'.format(code)) # DEBUG
        for second in range(num_gladiators):
            for first in range(num_gladiators + 1):
                if second <= first:
                    # calc score
                    guess_set_temp = remove_codes(guess_set, code, [first, second])
                    score_temp = len(guess_set) - len(guess_set_temp)
                    print('response: {0}  score: {1}'.format([first, second], score_temp))  # DEBUG
                    if score_temp < score:
                        score = score_temp
        if score > ret_score:
            ret_score = score
            ret = code
    print('ret_score: {}'.format(ret_score))
    return ret

if __name__ == "__main__":
    main()
