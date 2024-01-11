import numpy as np
import random

s=np.arange(-5, 7, dtype=float)

r = np.repeat(s, 2).reshape((12,2))

for i in range(len(r)):
    r[i,1]=random.randint(0, 30)
    print("afattoo: ", r[i,1] )


print(r)

win_size=3#secondi della finestra

window = np.ones((1,win_size))
window=window[0]*(1/win_size)

print(window)
sub =r[:,0]
print(sub)
c=np.convolve(sub,window, mode='same')
print(c)


r[:,1]=c

print(r)


for i in range(4):
    print("ok")