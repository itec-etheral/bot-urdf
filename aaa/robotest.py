import pybullet as p
import pybullet_data

phyCl = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

p.setGravity(0, 0, -10) # set gravity

plane = p.loadURDF("plane.urdf") # load the plane
bot = p.loadURDF("finalbot.urdf", [0, 0, 1]) # load the bot in

totalJoints = p.getNumJoints(bot) # total bot joints

print('\njoints: {}\n'.format(totalJoints))

for i in range(totalJoints):
	print("{}\n".format(p.getJointInfo(bot, i)))
	
#print('\n\n')
#print(p.getJointInfo(bot, 0))

lwVelocitySlider = p.addUserDebugParameter("LWheelVelocity",-100,100,0)
rwVelocitySlider = p.addUserDebugParameter("RWheelVelocity",-100,100,0)
maxForceRWSlider = p.addUserDebugParameter("maxForceRWs",0,300,15)

turnVelocitySlider = p.addUserDebugParameter("turnVelocity",-30,30,0)
maxTurnForceSlider = p.addUserDebugParameter("maxTurnForce",0,30,15)

fwVelocitySlider = p.addUserDebugParameter("forwardWheelsVelocity",-30,30,0)
maxFWForceSlider = p.addUserDebugParameter("maxFWForce",0,30,15)

p.setRealTimeSimulation(1)

p.changeDynamics(bot, 9, rollingFriction=0)
p.changeDynamics(bot, 8, rollingFriction=0)

redSlider = p.addUserDebugParameter("red",0,1,1)
greenSlider = p.addUserDebugParameter("green",0,1,0)
blueSlider = p.addUserDebugParameter("blue",0,1,0)
alphaSlider = p.addUserDebugParameter("alpha",0,1,0.5)



while(True):

	red = p.readUserDebugParameter(redSlider)
	green = p.readUserDebugParameter(greenSlider)
	blue = p.readUserDebugParameter(blueSlider)
	alpha = p.readUserDebugParameter(alphaSlider)
	p.changeVisualShape(bot,5,rgbaColor=[red,green,blue,alpha])

	lWheelVelocity = p.readUserDebugParameter(lwVelocitySlider)
	rWheelVelocity = p.readUserDebugParameter(rwVelocitySlider)
	maxForceRW = p.readUserDebugParameter(maxForceRWSlider)

	turnVelocity = p.readUserDebugParameter(turnVelocitySlider)
	maxTurnForce = p.readUserDebugParameter(maxTurnForceSlider)

	fwVelocity = p.readUserDebugParameter(fwVelocitySlider)
	maxFWForce = p.readUserDebugParameter(maxFWForceSlider)

	p.setJointMotorControl2(bodyUniqueId = bot, jointIndex = 0, controlMode = p.VELOCITY_CONTROL, targetVelocity = lWheelVelocity, force = maxForceRW) #LWheel
	p.setJointMotorControl2(bodyUniqueId = bot, jointIndex = 1, controlMode = p.VELOCITY_CONTROL, targetVelocity = rWheelVelocity, force = maxForceRW) #RWheel

	p.setJointMotorControl2(bodyUniqueId = bot, jointIndex = 8, controlMode = p.VELOCITY_CONTROL, targetVelocity = turnVelocity, force = maxTurnForce)

	p.setJointMotorControl2(bodyUniqueId = bot, jointIndex = 9, controlMode = p.VELOCITY_CONTROL, targetVelocity = fwVelocity, force = maxFWForce)
#	p.setJointMotorControl2(bodyUniqueId = bot, jointIndex = 10, controlMode = p.VELOCITY_CONTROL, targetVelocity = fwVelocity, force = maxFWForce)
