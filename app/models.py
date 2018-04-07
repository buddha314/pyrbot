import json
import math
import numpy as np
from services import d, angle

class Agent:
    def __init__(self, xpos, ypos, name, speed):
        self.name = name
        self.speed = speed
        self.xpos=xpos
        self.ypos=ypos

    def moveTo(self, target):
        a = angle(self, target)
        self.moveAlong(a,speed=self.speed)
        return 0

    """
    Moves in the direction of the specified angle
    """
    def moveAlong(self, angle, speed=None):
        if speed is None:
            speed = self.speed
        self.xpos = self.xpos + speed * math.cos(angle)
        self.ypos = self.ypos + speed * math.sin(angle)
        return 0


    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)

    def chooseAction(self, abins):
        c = np.random.choice(range(len(abins)+1))
        if c > len(abins):
            c = -1
        return c


"""
import math
from app import models
jose = models.RadiusAngleTiler(r_min=0, r_max=500, nbins=7)
jose.feature_vec(r=147,a=0.72)
"""
class RadiusAngleTiler:
    def __init__(self, r_min, r_max, nbins, a_min=-math.pi, a_max=math.pi):
        self.nbins = nbins
        self.r_min = r_min
        self.r_max = r_max
        self.a_min = a_min
        self.a_max = a_max
        self.setup_rbins()
        self.setup_abins()

    def setup_rbins(self):
        intv = (self.r_max-self.r_min)/(self.nbins-1.0)
        overlap = intv - 1.0*(self.r_max - self.r_min)/self.nbins
        self.rbins = [
          [self.r_min + i*(intv-overlap), self.r_min + (i+1)*(intv - overlap)+overlap] for i in range(self.nbins)
        ]

    def setup_abins(self):
        intv = (self.a_max-self.a_min)/(self.nbins-1.0)
        overlap = intv - 1.0*(self.a_max - self.a_min)/self.nbins
        self.abins = [
          [self.a_min + i*(intv-overlap), self.a_min + (i+1)*(intv - overlap)+overlap] for i in range(self.nbins)
        ]

    def feature_vec(self, a, r):
        features = [0] * (len(self.rbins)+ len(self.abins))
        for i in range(self.nbins):
            if r >= self.rbins[i][0] and r <= self.rbins[i][1]:
                features[i] = 1
            if a >= self.abins[i][0] and a <= self.abins[i][1]:
                features[self.nbins + i] = 1
        return features
