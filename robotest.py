import pybullet as p
import pybullet_data

phyCl = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

p.setGravity(0, 0, -10) # set gravity

plane = p.loadURDF("plane.urdf") # load the plane
bot = p.loadURDF("robotel2.0.urdf", [0, 0, 1]) # load the bot in

totalJoints = p.getNumJoints(bot) # total bot joints

print('\njoints: {}\n'.format(totalJoints))

for i in range(totalJoints):
	print("{}\n".format(p.getJointInfo(bot, i)))
	
#print('\n\n')
#print(p.getJointInfo(bot, 0))

rearWheelVelocitySlider = p.addUserDebugParameter("rearWheelsVelocity",-30,30,0)
maxForceRWSlider = p.addUserDebugParameter("maxForceRWs",0,30,15)

turnVelocitySlider = p.addUserDebugParameter("turnVelocity",-30,30,0)
maxTurnForceSlider = p.addUserDebugParameter("maxTurnForce",0,30,15)

fwVelocitySlider = p.addUserDebugParameter("fwVelocity",-30,30,0)
maxFWForceSlider = p.addUserDebugParameter("maxFWForce",0,30,15)

p.setRealTimeSimulation(1)

while(True):

	rearWheelVelocity = p.readUserDebugParameter(rearWheelVelocitySlider)
	maxForceRW = p.readUserDebugParameter(maxForceRWSlider)

	turnVelocity = p.readUserDebugParameter(turnVelocitySlider)
	maxTurnForce = p.readUserDebugParameter(maxTurnForceSlider)

	fwVelocity = p.readUserDebugParameter(fwVelocitySlider)
	maxFWForce = p.readUserDebugParameter(maxFWForceSlider)

	p.setJointMotorControl2(bodyUniqueId = bot, jointIndex = 0, controlMode = p.VELOCITY_CONTROL, targetVelocity = turnVelocity, force = maxTurnForce)
	p.setJointMotorControl2(bodyUniqueId = bot, jointIndex = 1, controlMode = p.VELOCITY_CONTROL, targetVelocity = fwVelocity, force = maxFWForce)
	p.setJointMotorControl2(bodyUniqueId = bot, jointIndex = 2, controlMode = p.VELOCITY_CONTROL, targetVelocity = rearWheelVelocity, force = maxForceRW)
	p.setJointMotorControl2(bodyUniqueId = bot, jointIndex = 3, controlMode = p.VELOCITY_CONTROL, targetVelocity = rearWheelVelocity, force = maxForceRW)

