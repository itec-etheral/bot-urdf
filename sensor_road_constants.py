def constant(f): # readonly decorative
    def fset(self, value):
        raise TypeError
    def fget(self):
        return f()
    return property(fget, fset)


class Const(object):
    """
    class used for sensor and road constants
    """

    @constant # readonly decorative
    def MAX_ROAD_MARGIN() -> float:
        # the right and left extremes of the road (with - for the left side)
        return 3.2

    @constant 
    def IRSENSOR_URDF_PATH() -> str:
        return "lego\lego.urdf"

    @constant
    def ROADPOINT_URDF_PATH() -> str:
        return "D:\\Projects\\Python\\bullet_car_learner_ripo\\bullet-learning\\duck2.urdf"

    @constant
    def ROBOT_URDF_PATH() -> str:
        return "goodbot.urdf"

    @constant
    def MAX_ROAD_DISTANCE() -> int:
        return 20
    
    @constant
    def ROAD_POINTS_STEP() -> float:
        return 0.0001

    @constant
    def A_ROAD_ELLIPSE() -> float: # it has to be >= MAX_ROAD_DISTANCE/2 to work
        return 10

    @constant
    def B_ROAD_ELLIPSE() -> float:
        return 4.0

    @constant
    def DEVIATION_ROAD() -> float:
        return 0.6

    def NUMBER_OF_POINTS(self) -> float:
        return float(self.MAX_ROAD_DISTANCE) * 2 / self.ROAD_POINTS_STEP

    @constant
    def ROAD_POINT_ERROR() -> float:
        return 0.472269


consts_obj = Const()  # Const instance to call the class
print("ROAD HAS: ", consts_obj.NUMBER_OF_POINTS(), " POINTS!")
