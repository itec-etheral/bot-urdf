import pybullet as p
import sensor_road_constants as sr_cnst
import numpy as np


class IRSensor(object):

    """
    sensor_pos_vector3 =  vector3 list for the position
    """

    def __init__(self):
        self._sensor_pos_vector3 = []

    def initialize_sensor(self, position):
        if len(position) is 3:
            self._sensor_pos_vector3 = position
        else:
            raise ValueError("The position has to be a 3 length list")

    def _have_position(self) -> bool:
        if len(self._sensor_pos_vector3) is 3:
            return True

        return False

    def get_position(self) -> list:
        if self._have_position():
            return self._sensor_pos_vector3
        else:
            raise Exception("Sensor position not initialized!")

    def get_sensor_response(self, road_object_position) -> float:  # reference to the current point in the road
        """
        it returns a value between [0, 1] 
            - for big distances the value goes towards 1
            - for small distances the value goes towards 0
            (0 when the sensor it's on the middle of the road, 1 when it's on the MAX_MARGIN_VALUE)
        """

        if self._have_position():

            response = (np.array([road_object_position[0], road_object_position[1]])
                        - np.array([self._sensor_pos_vector3[0], self._sensor_pos_vector3[1]]))
            # difference and transform it
            # in a np array -> narray for further calculations (take in consideration only the x and y axis)
            response_mag = np.sum(response*response) ** 0.5  # magnitude
            mapped_responde = response_mag / sr_cnst.consts_obj.MAX_ROAD_MARGIN
            # how the distance > MAX_ROAD_MARGIN -> the value it's mapped between [0,1]
            # if the value is >1 it means the robot it's out of it's boundaries
            return mapped_responde
        else:
            raise Exception("Sensor position not initialized!")




