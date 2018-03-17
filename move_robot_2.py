import pybullet as p
import pybullet_data
from goodbot import Goodbot
from Road import Road
import numpy as np
from sensor_road_constants import Const
import TrainData

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

nn_direction, nn_velocity = TrainData.get_train_weights(100)

print()

while 1:

    sensors_list = np.transpose(np.array([robot.get_output_sensor_for_near_road_points(road)[1:5]]))

    if sensors_list.shape[0] == 4:
        output_sensor_direction = np.transpose(nn_direction.model_output(sensors_list))[0]
        output_sensor_velocity = np.transpose(nn_velocity.model_output(sensors_list))[0]


        if output_sensor_direction[0] > output_sensor_direction[1]:
            robot.turn_right()
        elif output_sensor_direction[0] < output_sensor_direction [1]:
            robot.turn_left()

        if output_sensor_velocity[0] > output_sensor_velocity [1]:
            robot.go_forward(velocity, force)
        else:
            robot.go_forward(-velocity, force)




