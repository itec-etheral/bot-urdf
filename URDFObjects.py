# import pybullet_data
import pybullet as p

class URDFObject(object):
    """
    class to process all the URDF references 
    usually inherited by other object creator classes
    """

    def __init__(self, urdf_path, sensor_pos_vector3): 
        # p.setAdditionalSearchPath(pybullet_data.getDataPath())
        if len(sensor_pos_vector3) == 3:
            self._obj = p.loadURDF(urdf_path, sensor_pos_vector3)
        else:
            raise ValueError("use a 3 length sensor_pos_vector3 list as argument")

    def get_sensor_obj(self):
        return self._obj
