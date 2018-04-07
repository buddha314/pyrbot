import math
import scipy.spatial.distance
import numpy as np

def d(me, you):
    dst = scipy.spatial.distance.euclidean([me.xpos, me.ypos], [you.xpos, you.ypos])
    return dst

def angle(me, you):
    a = np.arctan2(you.ypos - me.ypos, you.xpos - me.xpos)
    return a
