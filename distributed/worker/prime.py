from math import sqrt
from itertools import count, islice
from random import random
from time import sleep

def is_prime(n):
    # stolen from StackOverflow #4114167
    sleep(random())  # to intentionally make slower
    return n > 1 and all(n%i for i in islice(count(2), int(sqrt(n)-1)))
