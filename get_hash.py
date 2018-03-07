import sys, random, time
from itertools import permutations, combinations
from call_api import post_reset, post_guess, get_header, get_level, get_hash


def main():
    # check Python version
    if sys.version_info < (3, 0):
        sys.exit('Python version < 3.0 does not support modern TLS versions. You will have trouble connecting to our API using Python 2.X.')

    headers = get_header()
    level = 7
    lvl_info = get_level(level, headers)
    print(lvl_info)

    hash = get_hash(headers)
    file_hash = open('hash.txt', 'w')
    file_hash.write(str(hash))
    print(hash)

if __name__ == "__main__":
    main()
