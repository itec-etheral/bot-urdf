import pybullet as p
import pybullet_data

class Goodbot:

#	self.bot = 0;	

	def __init__(self, bot_path, spawn_coords): #, road): #bot_path is a string; coords is a list 3 of floats (spawn coordinates)
		""" We instantiate the bot with the path to its urdf + a road object which the sensors will read off of """
		self.bot = p.loadURDF(bot_path, spawn_coords) # loads the bot in
		p.setJointMotorControl2(self.bot, 9, controlMode = p.VELOCITY_CONTROL, targetVelocity = 0, force = 0) #unblocks the front wheels
		p.setJointMotorControl2(self.bot, 10, controlMode = p.VELOCITY_CONTROL, targetVelocity = 0, force = 0) 

	
	def goForward(self, vel, force):
		""" vel is the velocity of the wheels (speed); force is the force used to get the wheels to spin that fast """
		p.setJointMotorControl2(self.bot, 0, controlMode = p.VELOCITY_CONTROL, targetVelocity = -vel, force = force)
		p.setJointMotorControl2(self.bot, 1, controlMode = p.VELOCITY_CONTROL, targetVelocity = -vel, force = force)
	
	def turnRight(self):
 		p.setJointMotorControl2(self.bot, 8, p.POSITION_CONTROL, targetPosition=-45) #turns the front wheels by -45 degrees

	def turnLeft(self):
 		p.setJointMotorControl2(self.bot, 8, p.POSITION_CONTROL, targetPosition=45) #turns the front wheels by +45 degrees
	
