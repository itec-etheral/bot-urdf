from sensor_road_constants import consts_obj
import pybullet as p


class RoadPoint(object):

    """
    Used as part of the big road
    self._road_point_position = vector3 list for position
    :param: num_road_points: static attribute for the draw line logic
    """

    num_road_points = 0

    def __init__(self, road_point_position):
        self._road_point_position = road_point_position
        if RoadPoint.num_road_points % 1000 == 0:
            to_road_point_position = [self._road_point_position[0] + consts_obj.ROAD_POINTS_STEP * 1000,
                                      self._road_point_position[1] + consts_obj.ROAD_POINTS_STEP * 1000,
                                      self._road_point_position[2]]
            p.addUserDebugLine(self._road_point_position, to_road_point_position, lineColorRGB=[0.9, 0.1, 0.1])

        RoadPoint.num_road_points += 1

    def get_road_point_position(self):
        return self._road_point_position
