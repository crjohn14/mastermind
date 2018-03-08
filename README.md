# Mastermind

Solution for Praetorians's Mastermind Challenge

Chris Johnson

Start Date: 21 Feb 2018

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
gave the same minimum for each guess which made it just waste time.

Level 4 requires a different strategy due to the ~128 million permutations (although it was fun to watch my RAM fill up
before the program crashed).  First the correct set of weapons is determined by guessing from a set of all possible
weapon combinations, which is only 177,100.  Once the correct set of weapons is determined, further guesses are made
from permutations of only those weapons.

Maintaining an open TCP connection was key to completing levels 5 and 6.  Requests would occasionally take longer than
the 10 second timeout period without using a requests session object.