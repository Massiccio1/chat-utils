import numpy as np
import random
import my_utils

url = 'https://www.youtube.com/watch?v=YspBTHE-55I' # 1:32:00

res1, res2 = my_utils.parse(url, 0.7, 50)

print(res1)
print(res2)




# x = np.array([1, 3, 7, 2, 9 ,8])
# ind = np.argsort(x)
# print(x)
# print(x[ind])
# print(np.flip(x[ind]))

# # print(x.shape[0])