import requests, json, sys, random
from itertools import permutations, combinations

base_url = 'https://mastermind.praetorian.com'

def main():
    # check Python version
    if sys.version_info < (3, 0):
        sys.exit('Python version < 3.0 does not support modern TLS versions. You will have trouble connecting to our API using Python 2.X.')

    # initialize headers
    headers = get_header()
    #print(headers)  # DEBUG

    # play the game
    post_reset(headers)

    done = False
    level = 1
    while(not done):
        # request level info from the mastermind
        lvl_info = request_level(level, headers)

        if 'numWeapons' in lvl_info:
            print_level_info(level, lvl_info)
        elif 'error' in lvl_info:
            print(lvl_info['error'])
            continue
        elif 'hash':
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
            level += fight_gladiators(guess_set, level, lvl_info, headers)
        else:
            # determine the correct weapons in level 4
            weapon_set = set(combinations(range(lvl_info['numWeapons']), lvl_info['numGladiators']))
            correct_weapons = determine_weapons(weapon_set, level, headers)
            # build permutations with only correct weapons
            guess_set = set(permutations(correct_weapons, lvl_info['numGladiators']))
            level += fight_gladiators(guess_set, level, lvl_info, headers)

    sys.exit(0)

"""Prepare headers for subsequent API calls"""
def get_header():
    email = 'cjohnson@cm.utexas.edu'  # my email
    r = requests.post('https://mastermind.praetorian.com/api-auth-token/', data={'email': email})
    r.json()
    headers = r.json()  # > {'Auth-Token': 'AUTH_TOKEN'}
    headers['Content-Type'] = 'application/json'
    return headers

"""request level information from mastermind"""
def request_level(level_number, headers):
    r = requests.get(base_url + '/level/' + str(level_number) + '/', headers=headers)
    return r.json()  # > {'numGladiators': 4, 'numGuesses': 8, 'numRounds': 1, 'numWeapons': 6}

"""post guess to mastermind"""
def post_guess(level_number, guess, headers):
    r = requests.post(base_url + '/level/' + str(level_number) + '/', data=json.dumps({'guess': guess}), headers=headers)
    return r.json()  # > {'response': [2, 1]}

"""request hash for completing mastermind"""
def get_hash(headers):
    r = requests.post(base_url + '/hash/', headers=headers)
    return r.json()

"""post reset to start back at level 1"""
def post_reset(headers):
    r = requests.post(base_url + '/reset/', headers=headers)
    return r.json()

"""Print level information"""
def print_level_info(level, lvl_info):
    print()
    print('LEVEL {0}'.format(level))
    print('rounds: {0[numRounds]:d}'.format(lvl_info))
    print('guesses: {0[numGuesses]:d}'.format(lvl_info))
    print('weapons: {0[numWeapons]:d}'.format(lvl_info))
    print('gladiators: {0[numGladiators]:d}\n'.format(lvl_info))

"""Generator for unique permutations of an iterable - 
https://stackoverflow.com/questions/6284396/permutations-with-unique-values"""
def unique_permutations(iterable, r=None):
    # TODO not sure i need this
    previous = tuple()
    for p in permutations(sorted(iterable), r):
        if p > previous:
            previous = p
            yield p

"""Choose a random guess from the guess set"""
def random_guess(guess_set):
    return random.sample(guess_set, 1)[0]

"""Remove codes from a set that wouldn't give the same response from the mastermind"""
def remove_codes(code_set, guess, response):
    correct_weapons = response[0]
    correct_gladiators = response[1]
    new_code_set = set(code_set)
    new_code_set.remove(tuple(guess))
    for code in code_set:
        # test code weapons
        if correct_weapons > len(set(code) & set(guess)):
            new_code_set.remove(code)
        else:
            # test code positions (gladiators)
            count = 0
            for pos in range(0, len(code)):
                if guess[pos] == code[pos]:
                    count += 1
            if correct_gladiators > count:
                new_code_set.remove(code)
    return new_code_set

"""choose a random element from the guess set, receive judgement from mastermind, then update the set if necessary
    :return level increment"""
def fight_gladiators(guess_set, level, lvl_info, headers):
    # defeat the gladiators!!!
    while (True):
        # random guess from the set
        guess = list(random_guess(guess_set))
        print("Guess set size : {}".format(len(guess_set)))
        print("Guess: {}".format(guess))

        # accept judgement from the mastermind
        judgement = post_guess(level, guess, headers)

        if 'response' in judgement:
            # print judgement
            print('correct weapons: {0} / {1}'.format(judgement['response'][0], lvl_info['numGladiators']))
            print('correct gladiators: {0} / {1}\n'.format(judgement['response'][1], lvl_info['numGladiators']))
            # remove guesses from guess set that wouldn't give the same judgement
            guess_set = remove_codes(guess_set, guess, judgement['response'])
        elif 'error' in judgement:
            # error; probably because 10 sec passed or no more guesses
            print(judgement['error'])
            return 0
        elif 'message' in judgement:
            print('YOU HAVE SLAIN YOUR OPPONENTS!!!')
            print(judgement['message'])
            return 1
        else:
            print('Judgement was not prepared for.  Code more...')
            sys.exit(0)

"""level 4 - determine correct weapons"""
def determine_weapons(weapon_set, level, headers):
    while (True):
        guess_weapons = list(random_guess(weapon_set))
        judgement = post_guess(level, guess_weapons, headers)

        if 'response' in judgement:
            num_correct_weapons = judgement['response'][0]
            if num_correct_weapons == 6:
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
            sys.exit(0)

"""level 4 - remove codes"""
def remove_codes_4(code_set, guess, response):
    correct_weapons = response[0]
    new_code_set = set(code_set)
    new_code_set.remove(tuple(guess))
    for code in code_set:
        # test code weapons
        if correct_weapons > len(set(code) & set(guess)):
            new_code_set.remove(code)
    return new_code_set

if __name__ == "__main__":
    main()

# TODO
# KEYERROR: 'response' line 34
#   - happened after 4th guess
#   - happened when guessing after waiting 10 sec (cursor also stopped blinking)
# error message if run out of turns
# message to continue if ran out of turns
# deal with multiple rounds per level?
#   - “roundsLeft”: 24} in response after moving to next level
#   - later levels have multiple rounds, no time between rounds, level resets if round is lost
# figure how to transition into next level
#   - {“message”: “Onto the next level”}
# level resets after 10 sec between guesses
# get hash when game completes
# allow user to reset game to lvl 1