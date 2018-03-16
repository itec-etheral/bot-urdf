import pybullet as p
import pybullet_data
from goodbot import Goodbot
from Road import Road

phyCl = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

plane = p.loadURDF("plane.urdf") # load the plane
p.setGravity(0, 0, -10) # set gravity
p.setRealTimeSimulation(1)

road = Road()
road.create_road()

robot = Goodbot("goodbot.urdf", [0, 0, 1])


p.setRealTimeSimulation(1)

while 1:
    pass