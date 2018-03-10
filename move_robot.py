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

# robot.go_forward(20, 100)

p.setRealTimeSimulation(1)

while 1:
    force = 0
    key_input = p.getKeyboardEvents()
    if p.B3G_RIGHT_ARROW in key_input.keys() and key_input[p.B3G_RIGHT_ARROW] == p.KEY_IS_DOWN:
        print("RIGHT")
        robot.turn_right()

    if p.B3G_LEFT_ARROW in key_input.keys() and key_input[p.B3G_LEFT_ARROW] == p.KEY_IS_DOWN:
        print("LEFT")
        robot.turn_left()

    if (not p.B3G_LEFT_ARROW in key_input.keys())\
            or (not p.B3G_RIGHT_ARROW in key_input.keys()):
        print("AHEAD")
        robot.turn_ahead()

    if p.B3G_UP_ARROW in key_input.keys() and key_input[p.B3G_UP_ARROW] == p.KEY_IS_DOWN:
        print("ACCELERATE")
        force += 15
        robot.go_forward(200, force)

    elif p.B3G_DOWN_ARROW in key_input.keys() and key_input[p.B3G_DOWN_ARROW] == p.KEY_IS_DOWN:
        print("DEACCELERATE")
        force -= 15
        robot.go_forward(200, force)
