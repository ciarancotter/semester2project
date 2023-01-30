from numpy import ndarray
from pykinect2 import PyKinectV2
from pykinect2 import PyKinectRuntime
from math import degrees, atan


class LeftWalk(object):
    """
    The LeftWalk Class is used to sense whether or the body in frame has its left calf rased or not.
    You need to call this class again once instanciated to update the data.

    Attributes:
        read (bool): whether or not the body has its left calf rased or not
        magnitude (int): angle over the threshold 

    Methods:
        __call__(kinect: PyKinectV2, body: PyKinectRuntime.KinectBody) -> None : updates the read according to whether or not the body is rasing its left calf or not.
        get_angle_threshhold() -> int : get the angle threashold needed to be reached to allow the motion to be recognised
        set_angle_threshhold(x: int) -> None : set the angle threashold needed to be reached to allow the motion to be recognised.
    """

    def __init__(self):
        """
        Creates the LeftWalk object
        """
        self._angle_threshhold = 20
        self.read = False
        self.magnitude = 0

    def __call__(self, body: PyKinectRuntime.KinectBody, depth:ndarray, joint_points:ndarray, joint_points_depth:ndarray) -> None:
        """
        Calling LeftWalk with these perameters updates the read according to whether or not the body is rasing its left calf or not.

        Args:
            body (PyKinectRuntime.KinectBody): A body being tracked in the frame.
            depth (ndarray): The array of depth points from the kinect
            joint_points (ndarray): The array of joint point poitions from the kinect
            joint_points_depth (ndarray): The array of joint depths from the kinect
        """

        joints = body.joints
        knee_point_id = PyKinectV2.JointType_KneeLeft
        ankle_point_id = PyKinectV2.JointType_AnkleLeft
        points = (knee_point_id, ankle_point_id)

        for i in points:
            point = joints[i].TrackingState
            # both joints are not tracked
            if point == PyKinectV2.TrackingState_NotTracked:
                return None, None, None
            # both joints are not *really* tracked
            if point == PyKinectV2.TrackingState_Inferred:
                return None, None, None

        # slope = rise/run
        rise = joint_points[ankle_point_id].y-joint_points[knee_point_id].y
        run = joint_points[knee_point_id].x-joint_points[ankle_point_id].x
        slope = (rise/run)

        angle = 90-degrees(atan(slope))
        if angle > 90:
            angle = 0

        if angle > self._angle_threshhold:
            self.read = True
            self.magnitude = angle - self._angle_threshhold
            return
        else:
            self.read = False
            self.magnitude = 0
            return
    
    def get_angle_threshhold(self) -> int:
        """
        Gets the angle threashold needed to be reached to allow a left walk to be recognised.

        Returns:
            int: the angle threashold needed to be reached to allow a left walk to be recognised.
        """
        return self._angle_threshhold

    def set_angle_threshhold(self, x: int) -> None:
        """
        Sets the angle threashold needed to be reached to allow a left walk to be recognised.

        Args:
            x (int): the new angle threashold needed to be reached to allow a left walk to be recognised.
        """
        self._angle_threshhold = x


class RightWalk(object):
    """
    The RightWalk Class is used to sense whether or the body in frame has its right calf rased or not.
    You need to call this class again once instanciated to update the data.

    Attributes:
        read (bool): whether or not the body has its right calf rased or not
        magnitude (int): angle over the threshold 

    Methods:
        __call__(kinect: PyKinectV2, body: PyKinectRuntime.KinectBody) -> None : updates the read according to whether or not the body is rasing its right calf or not.
        get_angle_threshhold() -> int : get the angle threashold needed to be reached to allow the motion to be recognised
        set_angle_threshhold(x: int) -> None : set the angle threashold needed to be reached to allow the motion to be recognised.
    """

    def __init__(self):
        """
        Creates the RightPunch object
        """
        self._angle_threshhold = 20
        self.read = False
        self.magnitude = 0

    def __call__(self, body: PyKinectRuntime.KinectBody, depth:ndarray, joint_points:ndarray, joint_points_depth:ndarray) -> None:
        """
        Calling RightPunch with these perameters updates the read according to whether or not the body is rasing its right calf or not.

        Args:
            body (PyKinectRuntime.KinectBody): A body being tracked in the frame.
            depth (ndarray): The array of depth points from the kinect
            joint_points (ndarray): The array of joint point poitions from the kinect
            joint_points_depth (ndarray): The array of joint depths from the kinect
        """
        joints = body.joints
        knee_point_id = PyKinectV2.JointType_KneeRight
        ankle_point_id = PyKinectV2.JointType_AnkleRight
        points = (knee_point_id, ankle_point_id)

        for i in points:
            point = joints[i].TrackingState
            # both joints are not tracked
            if point == PyKinectV2.TrackingState_NotTracked:
                return None, None, None
            # both joints are not *really* tracked
            if point == PyKinectV2.TrackingState_Inferred:
                return None, None, None

        # slope = rise/run
        rise = joint_points[ankle_point_id].y-joint_points[knee_point_id].y
        run = joint_points[ankle_point_id].x-joint_points[knee_point_id].x
        slope = (rise/run)

        angle = 90-degrees(atan(slope))
        if angle > 90:
            angle = 0

        if angle > self._angle_threshhold:
            self.read = True
            self.magnitude = angle - self._angle_threshhold
            return
        else:
            self.read = False
            self.magnitude = 0
            return

    def get_angle_threshhold(self) -> int:
        """
        Gets the angle threashold needed to be reached to allow a punch to be recognised.

        Returns:
            int: the angle threashold needed to be reached to allow a punch to be recognised.
        """
        return self._angle_threshhold

    def set_angle_threshhold(self, x: int) -> None:
        """
        Sets the angle threashold needed to be reached to allow a punch to be recognised.

        Args:
            x (int): the new angle threashold needed to be reached to allow a punch to be recognised.
        """
        self._angle_threshhold = x
