import pickle
from random import shuffle

alphabet = "abcdefghijklmnopqrstuvwxyz"
num = '1234567890'

r1 = list(alphabet)
shuffle(r1)
r1 = ''.join(r1)

rb1 = list(num)
shuffle(rb1)
rb1 = ''.join(rb1)

r2 = list(alphabet)
shuffle(r2)
r2 = ''.join(r2)

rb2 = list(num)
shuffle(rb2)
rb2 = ''.join(rb2)

r3 = list(alphabet)
shuffle(r3)
r3 = ''.join(r3)

rb3 = list(num)
shuffle(rb3)
rb3 = ''.join(rb3)

with open("Rotors.setting", "wb") as file:
    pickle.dump((r1, rb1, r2, rb2, r3, rb3), file)
