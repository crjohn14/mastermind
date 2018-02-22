import requests, json, sys
if sys.version_info < (3,0):
  sys.exit('Python version < 3.0 does not support modern TLS versions. You will have trouble connecting to our API using Python 2.X.')
email = 'cjohnson@cm.utexas.edu' # my email
r = requests.post('https://mastermind.praetorian.com/api-auth-token/', data={'email':email})
r.json()
headers = r.json()  # > {'Auth-Token': 'AUTH_TOKEN'}
headers['Content-Type'] = 'application/json'

# play the game
done = False
level = 1
while(not done):
  # request level info from the mastermind
  r = requests.get('https://mastermind.praetorian.com/level/{0}/'.format(level), headers=headers)
  lvlinfo = r.json()  # > {'numGladiators': 4, 'numGuesses': 8, 'numRounds': 1, 'numWeapons': 6}

  # print level info
  print('# of rounds: {0[numRounds]:d}'.format(lvlinfo))
  print('# of guesses: {0[numGuesses]:d}'.format(lvlinfo))
  print('# of weapons: {0[numWeapons]:d}'.format(lvlinfo))
  print('# of gladiators: {0[numGladiators]:d}'.format(lvlinfo))

  # defeat the gladiators!!!
  for guessNum in range(0, lvlinfo['numGuesses']):
    # input integers separated by commas
    weapon = input('Choose your weapons!:')
    guess = list(map(int, weapon.split(',')))
    # accept judgement from the mastermind
    r = requests.post('https://mastermind.praetorian.com/level/1/', data=json.dumps({'guess': [1, 2, 3, 4]}), headers=headers)
    judgement = r.json()  # > {'response': [2, 1]}

    # level up and break if all gladiators are defeated
    if (judgement['response'][0] == lvlinfo['numWeapons']) and (judgement['response'][1] == lvlinfo['numGladiators']):
      print('YOU HAVE SLAIN YOUR OPPONENTS!!!')
      print('The mastermind allows you to continue to the next level')
      level =+ 1
      break
    else:
      # print judgement
      print('# of correct weapons: {0} / {1}'.format(judgement['response'][0], lvlinfo['numWeapons']))
      print('# of correct gladiators: {0} / {1}'.format(judgement['response'][1], lvlinfo['numGladiators']))


  else:
    # did not complete level
    pass

# VICTORY - now get the hash
r = requests.post('https://mastermind.praetorian.com/hash/', headers=headers)

# TODO
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