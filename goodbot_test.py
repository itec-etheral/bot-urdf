import pybullet as p
import pybullet_data
from goodbot import Goodbot

phyCl = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

plane = p.loadURDF("plane.urdf") # load the plane
p.setGravity(0, 0, -10) # set gravity
p.setRealTimeSimulation(1)

robot = Goodbot("goodbot.urdf", [0, 0, 1])

robot.goForward(20, 100)
robot.turnRight()
