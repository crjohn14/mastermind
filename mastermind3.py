import requests, json, sys, random
from itertools import permutations

base_url = 'https://mastermind.praetorian.com'

def main():
    # check Python version
    if sys.version_info < (3, 0):
        sys.exit('Python version < 3.0 does not support modern TLS versions. You will have trouble connecting to our API using Python 2.X.')

    # initialize headers
    headers = get_header()

    # play the game
    done = False
    level = 1
    while(not done):
        # request level info from the mastermind
        lvl_info = request_level(level, headers)  # > {'numGladiators': 4, 'numGuesses': 8, 'numRounds': 1, 'numWeapons': 6}

        print(lvl_info)

        print_level_info(level, lvl_info)

        # produce a set of all possible guesses
        guess_set = set(unique_permutations(range(lvl_info['numWeapons']), lvl_info['numGladiators']))

        #print(guess_set)  #DEBUG

        # defeat the gladiators!!!
        while(True):
            # random guess from the set
            guess = list(random_guess(guess_set))
            print("Guess: {}".format(guess))
            # accept judgement from the mastermind
            r = requests.post('https://mastermind.praetorian.com/level/1/', data=json.dumps({'guess': guess}), headers=headers)
            judgement = r.json()  # > {'response': [2, 1]}

            if 'response' in judgement:
                # print judgement
                print('correct weapons: {0} / {1}'.format(judgement['response'][0], lvl_info['numGladiators']))
                print('correct gladiators: {0} / {1}'.format(judgement['response'][1], lvl_info['numGladiators']))
                # remove guesses from guess set that wouldn't give the same judgement
                guess_set = remove_codes(guess_set, guess, judgement['response'])
            elif 'error' in judgement:
                # error; probably because 10 sec passed or no more guesses
                print(judgement['error'])
                break
            elif 'message' in judgement:
                print('YOU HAVE SLAIN YOUR OPPONENTS!!!')
                print(judgement['message'])
                level += 1
                break
            else:
                print('Judgement was not prepared for.  Code more...')
                sys.exit(0)

    # VICTORY - now get the hash
    r = requests.post('https://mastermind.praetorian.com/hash/', headers=headers)
    hash = r.json()
    print('Victory is yours!!!')
    print('Hash: {}'.format(hash['hash']))
    print(hash)

"""Prepare headers for subsequent API calls"""
def get_header():
    email = 'crjohn14@asu.edu'  # my email
    r = requests.post('https://mastermind.praetorian.com/api-auth-token/', data={'email': email})
    headers = r.json()  # > {'Auth-Token': 'AUTH_TOKEN'}
    headers['Content-Type'] = 'application/json'
    return headers

def request_level(level_number, headers):
    r = requests.get(base_url + '/level/' + level_number + '/', headers=headers)
    return r.json()  # > {'numGladiators': 4, 'numGuesses': 8, 'numRounds': 1, 'numWeapons': 6}

"""Print level information"""
def print_level_info(level, lvl_info):
    print()
    print('LEVEL {0}'.format(level))
    print('rounds: {0[numRounds]:d}'.format(lvl_info))
    print('guesses: {0[numGuesses]:d}'.format(lvl_info))
    print('weapons: {0[numWeapons]:d}'.format(lvl_info))
    print('gladiators: {0[numGladiators]:d}'.format(lvl_info))
    print()

"""Generator for unique permutations of an iterable - 
https://stackoverflow.com/questions/6284396/permutations-with-unique-values"""
def unique_permutations(iterable, r=None):
    previous = tuple()
    for p in permutations(sorted(iterable), r):
        if p > previous:
            previous = p
            yield p

"""Select a random guess from the guess set"""
def random_guess(guess_set):
    return random.sample(guess_set, 1)[0]

"""Remove codes from a set that wouldn't give the same response from the mastermind"""
def remove_codes(code_set, guess, response):
    # TODO maybe use del list instead of set.remove()
    correct_weapons = response[0]
    correct_gladiators = response[1]
    new_code_set = set(code_set)
    new_code_set.remove(tuple(guess))
    for code in code_set:
        # test code positions (gladiators)
        count = 0
        for pos in range(0, len(code)):
            if guess[pos] == code[pos]:
                count += 1
        if correct_gladiators > count:
            new_code_set.remove(code)
        # test code weapons
        if correct_weapons > len(set(code) & set(guess)):
            new_code_set.remove(code)
    print(new_code_set) #DEBUG
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