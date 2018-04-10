import math, random
import scipy.spatial.distance
import numpy as np

def d(me, you):
    dst = scipy.spatial.distance.euclidean([me.xpos, me.ypos], [you.xpos, you.ypos])
    return dst

def angle(me, you):
    a = np.arctan2(you.ypos - me.ypos, you.xpos - me.xpos)
    return a

"""
flask shell

import numpy as np
import random
from app.services import linearSGD

# Fake some data
a1 = 2  *1.8 +    3*7.1
a2 = 0.5*1.8 +  0.75*7.1
a3 = 4.23*1.8 + 4.24*7.1
a4 = 3.01*1.8 + 9.17*7.1
a5 = 0.97*1.8 + 0.71*7.1

X = np.array([
  [2,3]
, [0.5, 0.75]
, [4.23, 4.24]
, [3.01, 9.17]
, [0.97, 0.71]
])
y = np.array([a1, a2, a3, a4, a5])
z = linearSGD(X, y, 0.01, 0.1)
print(z)
"""
def linearSGD(X, y, epsilon, eta):
    eta = 0.01
    epsilon = 0.1
    samples = 3 # Start with the average
    av = np.average(y)
    theta = [av] * X.shape[1]
    loss = 1000
    j = 0
    while loss > epsilon and j < 1000:
        r = range(X.shape[0])
        random.shuffle(r)
        for i in r[:samples]:
            theta = theta - eta * (X[i,].dot(theta) - y[i]) * X[i,]
        y_hat = X.dot(theta)
        err = y_hat - y
        loss = np.linalg.norm(err)
        j += 1
    return theta
