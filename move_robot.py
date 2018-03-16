import pybullet as p
import pybullet_data
from goodbot import Goodbot
from Road import Road
from threading import Timer
from sensor_road_constants import Const

phyCl = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

plane = p.loadURDF("plane.urdf") # load the plane
p.setGravity(0, 0, -10) # set gravity
p.setRealTimeSimulation(1)
p.resetDebugVisualizerCamera(5.18, 88, -449, [0, 0, 13])

consts_obj = Const()  # Const instance to call the class
print("ROAD HAS: ", consts_obj.NUMBER_OF_POINTS(), " POINTS!")

#print(Const.NUMBER_OF_POINTS())
#p.configureDebugVisualizer(p.COV_ENABLE_WIREFRAME, 1)

road = Road()
road.create_road()

robot = Goodbot("goodbot.urdf", road.get_road_points()[len(road.get_road_points()) * 3 //4].get_road_point_position() )

p.setRealTimeSimulation(1)

velocity = 0

rarr = p.B3G_RIGHT_ARROW
larr = p.B3G_LEFT_ARROW
uarr = p.B3G_UP_ARROW
darr = p.B3G_DOWN_ARROW

velocity = 30
force = 100
p.setGravity(0, 0, -30)

#velocitySlider = p.addUserDebugParameter("velocity",0,100,30) #30 is just fine, it doesnt matter much what it is
#forceSlider = p.addUserDebugParameter("force",0,200,100) #100 works best with -30 z axis gravity

#gravityXSlider = p.addUserDebugParameter("gravity x",-30,0,0) # we keep this on 0
#gravityYSlider = p.addUserDebugParameter("gravity y",-30,0,0) # 0 aswell
#gravityZSlider = p.addUserDebugParameter("gravity z",-30,0,-30) # determined to work best

save_length = 0;
total_data = 0;
write_list = [];

file = open('training_data.txt', 'a')

#caminfo = 88.0000991821289, -449.00006103515625, 5.179999828338623, (0.26104751229286194, 0.9333941340446472, 13.440003395080566)
# yaw, pitch, dist, target
#def test():
#    print(p.getDebugVisualizerCamera())
#
#t = Timer(15.0, test)
#t.start()

while 1:

    sensors_list = robot.get_output_sensor_for_near_road_points(road)

    is_right = 0
    is_left = 0
    is_forward = 0
    is_backward = 0
    out_li = []

#    for i in range(2, 8):
#        p.changeVisualShape(1, i, rgbaColor= [1-sensors_list[i - 2], 0, 0, 1])

#    velocity = p.readUserDebugParameter(velocitySlider)
#    force = p.readUserDebugParameter(forceSlider)

#    gX = p.readUserDebugParameter(gravityXSlider)
#    gY = p.readUserDebugParameter(gravityYSlider)
#    gZ = p.readUserDebugParameter(gravityZSlider)
#    p.setGravity(gX, gY, gZ)

    kin = p.getKeyboardEvents()

    if rarr in kin.keys() and kin[rarr] == p.KEY_IS_DOWN:
        robot.turn_right()
        is_right = 1
    elif larr in kin.keys() and kin[larr] == p.KEY_IS_DOWN:
        robot.turn_left()
        is_left = 1
    else: #if not (larr in kin.keys() or rarr in kin.keys()):
        robot.turn_ahead()
    if uarr in kin.keys() and kin[uarr] == p.KEY_IS_DOWN:
        robot.go_forward(velocity, force)
        is_forward = 1
    elif darr in kin.keys() and kin[darr] == p.KEY_IS_DOWN:
        robot.go_forward(-velocity, force)
        is_backward = 1
    else:
        robot.go_forward(0, 0)

    out_li = [is_right, is_left, is_forward, is_backward]

    print(sensors_list[1:5])
    print(out_li)

    write_list = write_list + sensors_list[1:5] + out_li
    print(write_list)

    save_length += 1
    print(save_length)

    if(save_length >= 100):
        temp_str2= ''
        print('SAVING...')
        for i in range(0, 8*100, 8): # range(x, y, z) -> y = nr of outputs * 100, z = nr of outputs
            temp_str = ''
            for j in range(8): # range(x) -> x = nr of outputs
                temp_str += ((str(write_list[i+j]) + '\n') if not (j == 0) and (j % 7 == 0) else str(write_list[i+j]) + ' ') # change the 7 to nr of outputs - 1
            temp_str2 += temp_str
        print('SAVED')
        print(temp_str2, file=file)
        save_length = 0
        write_list = []
