from URDFObjects import URDFObject
from sensor_road_constants import consts_obj
import pybullet as p


class RoadPoint(object):

    """
    Used as part of the big road
    self._road_point_postion = vector3 list for position
    """

    def __init__(self, road_point_position):
        self._road_point_postion = road_point_position

    def get_road_point_position(self):
        return self._road_point_postion
