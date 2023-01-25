from pykinect2 import PyKinectV2
from pykinect2 import PyKinectRuntime

class LeftPunch(object):
    """
    The LeftPunch Class is used to sense whether or the body in frame is punching to the left or not.
    You need to call this class again once instanciated to update the data.
    Attributes:
    - read (bool): whether or not the body is punching or not
    Methods:
    - __call__(kinect: PyKinectV2, body: PyKinectRuntime.KinectBody) -> None : updates the read according to whether or not the body is punching or not.
    - get_speed_threshhold() -> int : get the speed threashold needed to be reached to allow a punch to be recognised
    - set_speed_threshhold(x: int) -> None : set the speed threashold needed to be reached to allow a punch to be recognised.
    """

    def __init__(self):
        """
        Creates the LeftPunch object
        """
        self._olddelt = 0
        self._speed_threshhold = 20
        self.read = False


    def __call__(self, kinect: PyKinectV2,
                 body: PyKinectRuntime.KinectBody) -> None:
        """
        Calling LeftPunch with these perameters updates the read according to whether or not the body is punching or not.
        Parameters:
        - kinect (PyKinectV2): A reference to a PyKinectRuntime object.
        - body (PyKinectRuntime.KinectBody): A body being tracked in the frame.
        """

        joints = body.joints
        joint_points = kinect.body_joints_to_color_space(joints)
        point_id = PyKinectV2.JointType_HandLeft
        point = joints[point_id].TrackingState

        # both joints are not tracked
        if point == PyKinectV2.TrackingState_NotTracked:
            return
        # both joints are not *really* tracked
        if point == PyKinectV2.TrackingState_Inferred:
            return

        pointpos = (joint_points[point_id].x, joint_points[point_id].y)

        # a=0.9 == fast react      a=0.1 == slow react
        a = 0.4  # change per itteration
        """
        y[i] = a⋅x[i] + (1-a)⋅y[i-1]
            - y is the output
            - [i] denotes the sample number
            - x is the input
            - a is a constant which sets the cutoff frequency (a value between 0 and 1)
        """
        delt = a * pointpos[0] + (1 - a) * self._olddelt

        move = round(delt - self._olddelt, 3)
        self._olddelt = delt

        if move < -self._speed_threshhold:
            self.read = True
            return
        else:
            self.read = False
            return

    def get_speed_threshhold(self) -> int:
        """
        Gets the speed threashold needed to be reached to allow a punch to be recognised.
        Returns:
        - int: the speed threashold needed to be reached to allow a punch to be recognised.
        """
        return self._speed_threshhold

    def set_speed_threshhold(self, x : int) -> None:
        """
        Sets the speed threashold needed to be reached to allow a punch to be recognised.
        Parameters:
        x (int): the new speed threashold needed to be reached to allow a punch to be recognised.
        """
        self._speed_threshhold = x



class RightPunch(object):
    """
    The RightPunch Class is used to sense whether or the body in frame is punching to the right or not.
    You need to call this class again once instanciated to update the data.
    Attributes:
    - read (bool): whether or not the body is punching or not
    Methods:
    - __call__(kinect: PyKinectV2, body: PyKinectRuntime.KinectBody) -> None : updates the read according to whether or not the body is punching or not.
    - get_speed_threshhold() -> int : get the speed threashold needed to be reached to allow a punch to be recognised.
    - set_speed_threshhold(x: int) -> None : set the speed threashold needed to be reached to allow a punch to be recognised.
    """

    def __init__(self):
        """
        Creates the RightPunch object
        """
        self._olddelt = 0
        self._speed_threshhold = 20
        self.read = False

    def __call__(self, kinect: PyKinectV2,
                 body: PyKinectRuntime.KinectBody) -> bool:
        """
        Calling RightPunch with these perameters updates the read according to whether or not the body is punching or not.
        Parameters:
        - kinect (PyKinectV2): A reference to a PyKinectRuntime object.
        - body (PyKinectRuntime.KinectBody): A body being tracked in the frame.
        """
        joints = body.joints
        joint_points = kinect.body_joints_to_color_space(joints)
        point_id = PyKinectV2.JointType_HandRight
        point = joints[point_id].TrackingState

        # both joints are not tracked
        if point == PyKinectV2.TrackingState_NotTracked:
            return
        # both joints are not *really* tracked
        if point == PyKinectV2.TrackingState_Inferred:
            return

        pointpos = (joint_points[point_id].x, joint_points[point_id].y)

        # a=0.9 == fast react      a=0.1 == slow react
        a = 0.4  # change per itteration
        """
        y[i] = a⋅x[i] + (1-a)⋅y[i-1]
            - where:y is the output
            - [i] denotes the sample number
            - x is the input
            - a is a constant which sets the cutoff frequency (a value between 0 and 1)
        """
        delt = a * pointpos[0] + (1 - a) * self._olddelt

        move = round(delt - self._olddelt, 3)
        self._olddelt = delt

        if move > self._speed_threshhold:
            self.read = True
            return
        else:
            self.read = False
            return

    def get_speed_threshhold(self) -> int:
        """
        Gets the speed threashold needed to be reached to allow a punch to be recognised.
        Returns:
        - int: the speed threashold needed to be reached to allow a punch to be recognised.
        """
        return self._speed_threshhold

    def set_speed_threshhold(self, x : int) -> None:
        """
        Sets the speed threashold needed to be reached to allow a punch to be recognised.
        Parameters:
        x (int): the new speed threashold needed to be reached to allow a punch to be recognised.
        """
        self._speed_threshhold = x
