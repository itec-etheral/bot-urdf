import pybullet as p
from URDFObjects import URDFObject
from IRSensor import IRSensor
from numpy import array

class Goodbot(URDFObject):

	def __init__(self, bot_path: str, spawn_coords: list): #, road): #bot_path is a string; coords is a list 3 of floats (spawn coordinates)
		""" We instantiate the bot with the path to its urdf + a road object which the sensors will read off of """
		super(Goodbot, self).__init__(bot_path, spawn_coords, scale_factor=0.5) # loads the bot in as a self._obj
		p.setJointMotorControl2(self._obj, 9, controlMode = p.VELOCITY_CONTROL, targetVelocity = 0, force = 0) #unblocks the front wheels
		p.setJointMotorControl2(self._obj, 10, controlMode = p.VELOCITY_CONTROL, targetVelocity = 0, force = 0)
		self._sensors = self._attach_sensors_to_robot()

	def go_forward(self, vel, force):
		""" vel is the velocity of the wheels (speed); force is the force used to get the wheels to spin that fast """
		p.setJointMotorControl2(self._obj, 0, controlMode = p.VELOCITY_CONTROL, targetVelocity = -vel, force = force)
		p.setJointMotorControl2(self._obj, 1, controlMode = p.VELOCITY_CONTROL, targetVelocity = -vel, force = force)
	
	def turn_right(self):
 		p.setJointMotorControl2(self._obj, 8, p.POSITION_CONTROL, targetPosition=-45) #turns the front wheels by -45 degrees

	def turn_left(self):
 		p.setJointMotorControl2(self._obj, 8, p.POSITION_CONTROL, targetPosition=45) #turns the front wheels by +45 degrees

	def turn_ahead(self):
		p.setJointMotorControl2(self._obj, 8, p.POSITION_CONTROL, targetPosition=0) #turns the front wheels by +45 degrees

	@staticmethod
	def number_of_sensosr() -> int:
		return 6

	@staticmethod
	def start_joint_sensor_number() -> int:
		return 2

	def _attach_sensors_to_robot(self) -> list:
		sensors = []

		for current_joint in range(Goodbot.start_joint_sensor_number(), Goodbot.number_of_sensosr()
				+ Goodbot.start_joint_sensor_number()):
			sensor = IRSensor()
			sensor_position = list(array(p.getLinkState(self._obj, current_joint)[0]))
			# + array(p.getBasePositionAndOrientation(self._obj)[0]))
			# global sensor position

			# store in positions in a list
			sensor.initialize_sensor(sensor_position)
			sensors.append(sensor)

		return sensors

	def get_sensors_response(self, current_road_point_position, attach=True) -> list:
		# a list of len(number_of_sensosr()) outputs
		output = []
		# compute the global position of the sensors ( it changes every time the
		# car moves)

		if attach:  # this func it is used also in other logic that does not need this recomputation
			self._sensors = self._attach_sensors_to_robot()

		for sensor in self._sensors:
			output.append(sensor.get_sensor_response(current_road_point_position))

		return output

	def get_sensors(self) -> list:
		return self._sensors

	def get_output_sensor_for_near_road_points(self, road) -> list:
		# get output sensor from the point that you are on top of

		self._sensors = self._attach_sensors_to_robot()
		# retake the sensors position

		for road_point in road.get_road_points():
			road_point_pos = road_point.get_road_point_position()
			distance_on_x_axis = self._sensors[2].get_position()[0] - road_point_pos[0]
			distance_on_y_axis = self._sensors[2].get_position()[1] - road_point_pos[1]
			distance = (distance_on_x_axis**2 + distance_on_y_axis**2) ** 0.5

			if distance <= 0.472269:  # empiric number that works just fine (the error it is so big cuz we check
				# the distance with the second sensor position that it usually it is not exactly on top of the line
				# and we compute both x and y axis that both will never be exactly on the line
				return self.get_sensors_response(road_point_pos, attach=False)

		return None

	
