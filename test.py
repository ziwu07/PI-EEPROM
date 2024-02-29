import gpiozero
from time import sleep

a = int("ea", 16)
for i in range(8):
    print((a >> i) & 1)
