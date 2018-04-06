import math
import scipy.spatial.distance
def d(me, you):
    dst = scipy.spatial.distance.euclidean([me.xpos, me.ypos], [you.xpos, you.ypos])
    return dst
