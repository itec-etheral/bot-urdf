from RoadPoint import RoadPoint
from sensor_road_constants import consts_obj
from numpy import arange


class Road(object):

    """
    Road generator that uses RoadPoint class as atoms
    self._road_points = list that contains all the road points
    """

    def __init__(self):
        self._road_points = []

    def get_road_points(self) -> list:
        return self._road_points

    def create_road(self): 
        
        for pos in self._road_vec3_generator():
            road_point = RoadPoint(pos)
            self._road_points.append(road_point)

        for pos in self._road_vec3_generator(conj_y=True):
            road_point = RoadPoint(pos)
            self._road_points.append(road_point)

    def _road_vec3_generator(self, conj_y=False) -> list:
        
        centralized_max_x = consts_obj.MAX_ROAD_DISTANCE / 2

        x = arange(-centralized_max_x, centralized_max_x, consts_obj.ROAD_POINTS_STEP)
        # domain of points to generate coordonates centered in 0

        a = consts_obj.A_ROAD_ELLIPSE
        b = consts_obj.B_ROAD_ELLIPSE

        if a < centralized_max_x:
            raise TypeError("consts_obj.A_ROAD_ELLIPSE is to small -> complex numbers will be generated")
        
        for local_x in x.tolist():
            local_y = b/a * (((a - local_x) * (a + local_x)) ** 0.5)
            # this equation was generated from the ellipse equation, therefor
            # the road will be generated like a ellipse

            if conj_y:
                local_y = -local_y
            
            if -0.3 * centralized_max_x < local_x < 0.3 * centralized_max_x:
                local_x = local_x + consts_obj.DEVIATION_ROAD
                if conj_y:
                    local_y = local_y - consts_obj.DEVIATION_ROAD
                else:
                    local_y = local_y + consts_obj.DEVIATION_ROAD
                    
            yield [local_x, local_y, 0]

    