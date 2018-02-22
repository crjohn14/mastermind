import requests, json, sys


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
        r = requests.get('https://mastermind.praetorian.com/level/{0}/'.format(level), headers=headers)
        lvl_info = r.json()  # > {'numGladiators': 4, 'numGuesses': 8, 'numRounds': 1, 'numWeapons': 6}
        print_level_info(level, lvl_info)

        # defeat the gladiators!!!
        while(True):
            # input integers separated by commas; weapons begin from 0
            weapon = input('Choose your weapons!:')
            guess = list(map(int, weapon.split(',')))
            # accept judgement from the mastermind
            r = requests.post('https://mastermind.praetorian.com/level/1/', data=json.dumps({'guess': guess}), headers=headers)
            judgement = r.json()  # > {'response': [2, 1]}

            print(judgement) # DEBUG

            if 'response' in judgement:
                # print judgement
                print('correct weapons: {0} / {1}'.format(judgement['response'][0], lvl_info['numWeapons']))
                print('correct gladiators: {0} / {1}'.format(judgement['response'][1], lvl_info['numGladiators']))
            elif 'error' in judgement:
                # error; probably because 10 sec passed
                print(judgement['error'])
                break
            elif 'message' in judgement:
                print('YOU HAVE SLAIN YOUR OPPONENTS!!!')
                print('The mastermind allows you to continue to the next level')
                level += 1
                break
            else:
                print('Judgement was not prepared for.  Code more...')
                sys.exit(0)

    # VICTORY - now get the hash
    r = requests.post('https://mastermind.praetorian.com/hash/', headers=headers)
    hash = r.json()
    print('Victory is yours.')
    print('Hash: {}'.format(hash['hash']))
    print(hash)


def get_header():
    email = 'cjohnson@cm.utexas.edu'  # my email
    r = requests.post('https://mastermind.praetorian.com/api-auth-token/', data={'email': email})
    r.json()
    headers = r.json()  # > {'Auth-Token': 'AUTH_TOKEN'}
    headers['Content-Type'] = 'application/json'
    return headers



def print_level_info(level, lvl_info):
    print()
    print('LEVEL {0}'.format(level))
    print('rounds: {0[numRounds]:d}'.format(lvl_info))
    print('guesses: {0[numGuesses]:d}'.format(lvl_info))
    print('weapons: {0[numWeapons]:d}'.format(lvl_info))
    print('gladiators: {0[numGladiators]:d}'.format(lvl_info))
    print()

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