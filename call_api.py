"""Module for mastermind.py to call Praetorian's mastermind API

functions:
get_header - prepare headers for subsequent API calls
get_level - request level information
get_hash - request hash after completing the challenge
post_guess - post a guess and receive response
post_reset - reset user to level 1
"""

import requests, json

BASE_URL = 'https://mastermind.praetorian.com'

s = requests.Session()

#file_request_time = open('request_times.txt', 'w') # DEBUG

def get_header():
    """Prepare headers for subsequent API calls"""
    EMAIL = 'cjohnson@cm.utexas.edu'  # my email
    r = s.post('{0}/api-auth-token/'.format(BASE_URL), data={'email': EMAIL})
    #headers = r.json()  # > {'Auth-Token': 'AUTH_TOKEN'}
    #headers['Content-Type'] = 'application/json'

    print(s.headers)
    s.headers.update(r.json)
    s.headers.update({'Content-Type' : 'application/json'})
    print(s.headers)

    return

def get_level(level_number, headers):
    """request level information from mastermind"""
    r = requests.get('{0}/level/{1}/'.format(BASE_URL, level_number), headers=headers)
    #file_request_time.write('get_level: ' + str(r.elapsed.total_seconds()) + '\n')
    return r.json()  # > {'numGladiators': 4, 'numGuesses': 8, 'numRounds': 1, 'numWeapons': 6}

def post_guess(level_number, guess, headers):
    """post guess to mastermind"""
    r = requests.post('{0}/level/{1}/'.format(BASE_URL, level_number), data=json.dumps({'guess': guess}), headers=headers)
    print('Request duration: {0:.3f} seconds'.format(r.elapsed.total_seconds())) # DEBUG
    #file_request_time.write('post_guess: ' + str(r.elapsed.total_seconds()) + '\n') # DEBUG
    return r.json()  # > {'response': [2, 1]}

def get_hash(headers):
    """request hash for completing mastermind"""
    r = requests.get('{0}/hash/'.format(BASE_URL), headers=headers)
    return r.json()

def post_reset(headers):
    """post reset to start back at level 1"""
    r = requests.post('{0}/reset/'.format(BASE_URL), headers=headers)
    return r.json()