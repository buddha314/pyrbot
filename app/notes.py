import pybullet as p
import numpy as np
import math
import time
import pybullet_data

DURATION = 10000
R2_SPEED = 300
DUCK_SPEED = 5
DUCK_RADIUS = 4
DUCK_FLIGHT_ALTITUDE = 0.5

def runLikeDuck(i, currentPos) :
    v = DUCK_SPEED * (DUCK_RADIUS*np.array([math.cos((i+1)/180), math.sin((i+1)/180), DUCK_FLIGHT_ALTITUDE]) - np.array(currentPos))
    #v = DUCK_RADIUS*np.array([math.cos(i/360.), math.sin(i/360.), 0])
    print(v)
    return v


physicsClient = p.connect(p.GUI)#or p.DIRECT for non-graphical version
p.setAdditionalSearchPath(pybullet_data.getDataPath()) #optionally
print("data path: %s " % pybullet_data.getDataPath())
p.setGravity(0,0,-10)
planeId = p.loadURDF("plane.urdf")
cubeStartPos = [0,0,1]
cubeStartOrientation = p.getQuaternionFromEuler([0,0,0])
boxId = p.loadURDF("r2d2.urdf",cubeStartPos, cubeStartOrientation)
gemId = p.loadURDF("duck_vhacd.urdf", [2,2,1],  p.getQuaternionFromEuler([0,0,0]) )
for i in range (DURATION):
    p.stepSimulation()
    time.sleep(1./240.)
    gemPos, gemOrn = p.getBasePositionAndOrientation(gemId)
    cubePos, cubeOrn = p.getBasePositionAndOrientation(boxId)
    oid, lk, frac, pos, norm = p.rayTest(cubePos, gemPos)[0]
    #rt = p.rayTest(cubePos, gemPos)
    #print("rayTest: %s" % rt[0][1])
    #print("rayTest: Norm: ")
    #print(norm)
    cubeVec = np.array([R2_SPEED * (gemPos[k]-cubePos[k]) for k in range(len(gemPos))])
    #duckVec = np.array([-DUCK_SPEED * (gemPos[i]-cubePos[i]) for i in range(len(gemPos))])
    duckVec = runLikeDuck(i, gemPos)
    #vec = p.getQuaternionFromEuler([300*(gemPos[0] - cubePos[0]), 300*(gemPos[1] - cubePos[1]), 0])

    p.applyExternalForce(objectUniqueId=boxId, linkIndex=-1, forceObj=cubeVec
        ,posObj=pos, flags=p.WORLD_FRAME)
    p.applyExternalForce(objectUniqueId=gemId, linkIndex=-1, forceObj=duckVec
        ,posObj=gemPos, flags=p.WORLD_FRAME)
print(cubePos,cubeOrn)
p.disconnect()
