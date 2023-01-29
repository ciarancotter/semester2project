from pykinect2 import PyKinectV2
from pykinect2 import PyKinectRuntime


class Jump(object):
    """
    The Jump Class is used to sense whether or the body in frame is jumping or not
    You need to call this class again once instanciated to update the data.

    Attributes:
        read (bool): whether or not the body is jumping or not
        magnitude (int): speed over the threshold 

    Methods:
        __call__(kinect: PyKinectV2, body: PyKinectRuntime.KinectBody) -> None : updates the read according to whether or not the body is jumping or not.
        get_speed_threshhold() -> int : get the speed threashold needed to be reached to allow a jump to be recognised
        set_speed_threshhold(x: int) -> None : set the speed threashold needed to be reached to allow a jump to be recognised.
    """

    def __init__(self):
        """
        Creates the Jump object
        """
        self._olddelt = 0
        self._speed_threshhold = 15
        self.read = False
        self.magnitude = 0

    def __call__(self, body: PyKinectRuntime.KinectBody, depth, joint_points, joint_points_depth) -> None:
        """
        Calling Jump with these perameters updates the read according to whether or not the body is jumping or not.

        Args:
            kinect (PyKinectV2): A reference to a PyKinectRuntime object.
            body (PyKinectRuntime.KinectBody): A body being tracked in the frame.
        """
        joints = body.joints
        point_id = PyKinectV2.JointType_SpineShoulder
        point = joints[point_id].TrackingState

        # both joints are not tracked
        if point == PyKinectV2.TrackingState_NotTracked:
            return
        # both joints are not *really* tracked
        if point == PyKinectV2.TrackingState_Inferred:
            return

        posy = joint_points[point_id].y

        # a=0.9 == fast react      a=0.1 == slow react
        max_change_per_itteration = 0.4  # change per itteration
        delt = max_change_per_itteration * posy + (1 -  max_change_per_itteration) * self._olddelt

        move = round(delt - self._olddelt, 3)
        self._olddelt = delt

        if move < -self._speed_threshhold:
            self.read = True
            self.magnitude = -(move + self._speed_threshhold)
            return
        else:
            self.read = False
            self.magnitude = 0
            return

    def get_speed_threshhold(self) -> int:
        """
        Gets the speed threashold needed to be reached to allow a jump to be recognised.

        Returns:
            int: the speed threashold needed to be reached to allow a jump to be recognised.
        """
        return self._speed_threshhold

    def set_speed_threshhold(self, x: int) -> None:
        """
        Sets the speed threashold needed to be reached to allow a jump to be recognised.

        Args:
            x (int): the new speed threashold needed to be reached to allow a jump to be recognised.
        """
        self._speed_threshhold = x