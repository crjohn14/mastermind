"""Module for mastermind.py to call Praetorian's mastermind API

functions:
init_header - prepare headers for subsequent API calls
get_level - request level information
get_hash - request hash after completing the challenge
post_guess - post a guess and receive response
post_reset - reset user to level 1
"""

import requests, json

BASE_URL = 'https://mastermind.praetorian.com'

s = requests.Session()

def init_header():
    """Prepare headers for subsequent API calls"""
    EMAIL = 'cjohnson@cm.utexas.edu'  # my email
    r = s.post('{0}/api-auth-token/'.format(BASE_URL), data={'email': EMAIL})
    s.headers.update({'Content-Type' : 'application/json'})
    s.headers.update(r.json()) # > {'Auth-Token': 'AUTH_TOKEN'}
    return

def get_level(level_number):
    """request level information from mastermind"""
    r = s.get('{0}/level/{1}/'.format(BASE_URL, level_number))
    return r.json()  # > {'numGladiators': 4, 'numGuesses': 8, 'numRounds': 1, 'numWeapons': 6}

def post_guess(level_number, guess):
    """post guess to mastermind"""
    r = s.post('{0}/level/{1}/'.format(BASE_URL, level_number), data=json.dumps({'guess': guess}))
    return r.json()  # > {'response': [2, 1]}

def get_hash():
    """request hash for completing mastermind"""
    r = s.get('{0}/hash/'.format(BASE_URL))
    return r.json()

def post_reset():
    """post reset to start back at level 1"""
    r = s.post('{0}/reset/'.format(BASE_URL))
    return r.json()