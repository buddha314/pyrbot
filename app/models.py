import json
import math, random
import numpy as np
from services import d, angle
from config import *

class Agent:

    def __init__(self, xpos, ypos, name, speed
        , action_space_dims, state_space_dims
        , stage_width, stage_height):
        self.name = name
        self.speed = speed
        self.xpos=xpos
        self.ypos=ypos
        self.stage_width=stage_width
        self.stage_height=stage_height
        self.memories=[]
        self.theta = [random.random() for _ in range(state_space_dims+action_space_dims)]
        self.theta_hat = self.theta

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
        self.xpos = (self.xpos + speed * math.cos(angle)) % self.stage_width
        self.ypos = (self.ypos + speed * math.sin(angle)) % self.stage_height
        return 0


    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)

    #def chooseAction(self, available_actions, state):
    def chooseAction(self, options):
        l = len(options['available_actions'])
        choices = [0]*l
        for i in range(l):
            v = [0]*l
            v[i] = 1
            choices[i] = np.concatenate([options['state'], v]).dot(self.theta_hat)
        c = np.argmax(choices)
        choice = [0]*l
        choice[c] = 1
        #print("RR choices %s" % choices)
        #print("RR best choice: %s" % np.argmax(choices))
        c = np.random.choice(range(l))
        if c == l-1:
            print("I'M STAYING RIGHT HERE!!!")
        return choice

    def addMemory(self, m):
        self.memories.append(m)

    def update_theta(self):
        print("memories cached: %s" % len(self.memories))
        self.theta_hat = self.theta
        return 0


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

    def state_vec(self, a, r):
        features = [0] * (len(self.rbins)+ len(self.abins))
        for i in range(self.nbins):
            if r >= self.rbins[i][0] and r <= self.rbins[i][1]:
                features[i] = 1
            if a >= self.abins[i][0] and a <= self.abins[i][1]:
                features[self.nbins + i] = 1
        return features

class Memory:
    def __init__(self, episode, step
        ,current_state, current_action):
        self.episode = episode
        self.step=step
        self.current_state = current_state
        self.current_action = current_action

class DM:
    def __init__(self, tiler, action_space_dims, state_space_dims):
        self.tiler = tiler
        self.action_space_dims = action_space_dims
        self.state_space_dims = state_space_dims
        self.game_over = False

    def get_current_state(self, player, opponent):
        r = d(player, opponent)
        a = angle(player, opponent)
        state = self.tiler.state_vec(a=a, r=r)
        return state

    def present_options(self, step, player, opponent):
        #r = d(player, opponent)
        #a = angle(player, opponent)
        #state = self.tiler.state_vec(a=a, r=r)
        state = self.get_current_state(player=player, opponent=opponent)
        available_actions = [1] * (len(self.tiler.abins) +1)  # last is None
        # Check to add or remove actions at this point
        r = {}
        r['available_actions']=available_actions
        r['state']=state
        return r

    def present_update(self, step, player, choice, npc):
        # Choice is a vector, this is inelegant, but I'll fix it later
        c = np.argmax(choice)
        #if choice < self.action_space_dims - 1:
        if c < self.action_space_dims - 1:
            player.moveAlong(self.tiler.abins[c][1])
        npc.moveTo(player)

        reward = 0
        if step > steps:
            reward=escape_reward
            self.game_over=True
        if d(player, npc) <= capture_distance:
            reward = capture_penalty
            self.game_over=True
        return reward

    def game_over(self):
        return self.game_over
