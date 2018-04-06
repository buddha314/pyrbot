import math
import scipy.spatial.distance
import numpy as np

def d(me, you):
    dst = scipy.spatial.distance.euclidean([me.xpos, me.ypos], [you.xpos, you.ypos])
    return dst

def angle(me, you):
    t = (you.ypos - me.ypos) / (you.xpos - me.xpos)
    a = math.cos(t)
    return a
