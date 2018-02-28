import requests, json

BASE_URL = 'https://mastermind.praetorian.com'

"""Prepare headers for subsequent API calls"""
def get_header():
    email = 'cjohnson@cm.utexas.edu'  # my email
    r = requests.post('{0}/api-auth-token/'.format(BASE_URL), data={'email': email})
    r.json()
    headers = r.json()  # > {'Auth-Token': 'AUTH_TOKEN'}
    headers['Content-Type'] = 'application/json'
    return headers

"""request level information from mastermind"""
def get_level(level_number, headers):
    r = requests.get('{0}/level/{1}/'.format(BASE_URL, level_number), headers=headers)
    return r.json()  # > {'numGladiators': 4, 'numGuesses': 8, 'numRounds': 1, 'numWeapons': 6}

"""post guess to mastermind"""
def post_guess(level_number, guess, headers):
    r = requests.post('{0}/level/{1}/'.format(BASE_URL, level_number), data=json.dumps({'guess': guess}), headers=headers)
    print('Request duration: {0:.3f} seconds'.format(r.elapsed.total_seconds())) # DEBUG
    return r.json()  # > {'response': [2, 1]}

"""request hash for completing mastermind"""
def get_hash(headers):
    r = requests.post('{0}/hash/'.format(BASE_URL), headers=headers)
    return r.json()

"""post reset to start back at level 1"""
def post_reset(headers):
    r = requests.post('{0}/reset/'.format(BASE_URL), headers=headers)
    return r.json()