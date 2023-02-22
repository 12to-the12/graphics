
import time
import random
rep = 10_000
a = time.time()
for x in range(rep):
    print('hello!\nmy name is Donald Glover, what is your perspective on love')
b = time.time()
print(((b-a)*1000)/rep, 'ms')