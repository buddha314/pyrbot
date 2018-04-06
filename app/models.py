import json

class Agent:
    def __init__(self, xpos, ypos, name, speed):
        self.name = name
        self.speed = speed
        self.xpos=xpos
        self.ypos=ypos

    def moveTo(self, target):
        newx = self.speed * (target.xpos - self.xpos) + self.xpos
        newy = self.speed * (target.ypos - self.ypos) + self.ypos
        #print(" me: (%s, %s)  it: (%s, %s)   v: (%s,%s)" % (self.xpos, self.ypos, target.xpos, target.ypos, newx, newy))
        return (newx, newy)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)
