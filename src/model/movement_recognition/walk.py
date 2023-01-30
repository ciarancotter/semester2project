from pykinect2 import PyKinectV2
from pykinect2 import PyKinectRuntime
from math import degrees, atan


class LeftWalk(object):
    """
    The LeftPunch Class is used to sense whether or the body in frame is punching to the left or not.
    You need to call this class again once instanciated to update the data.

    Attributes:
        read (bool): whether or not the body is punching or not
        magnitude (int): speed over the threshold 

    Methods:
        __call__(kinect: PyKinectV2, body: PyKinectRuntime.KinectBody) -> None : updates the read according to whether or not the body is punching or not.
        get_speed_threshhold() -> int : get the speed threashold needed to be reached to allow a punch to be recognised
        set_speed_threshhold(x: int) -> None : set the speed threashold needed to be reached to allow a punch to be recognised.
    """

    def __init__(self):
        """
        Creates the LeftWalk object
        """
        self._angle_threshhold = 20
        self.read = False
        self.magnitude = 0

    def __call__(self, body: PyKinectRuntime.KinectBody, depth, joint_points, joint_points_depth) -> None:
        """
        Calling LeftPunch with these perameters updates the read according to whether or not the body is punching or not.

        Args:
            kinect (PyKinectV2): A reference to a PyKinectRuntime object.
            body (PyKinectRuntime.KinectBody): A body being tracked in the frame.
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
        Gets the speed threashold needed to be reached to allow a punch to be recognised.

        Returns:
            int: the speed threashold needed to be reached to allow a punch to be recognised.
        """
        return self._angle_threshhold

    def set_angle_threshhold(self, x: int) -> None:
        """
        Sets the speed threashold needed to be reached to allow a punch to be recognised.

        Args:
            x (int): the new speed threashold needed to be reached to allow a punch to be recognised.
        """
        self._angle_threshhold = x


class RightWalk(object):
    """
    The RightPunch Class is used to sense whether or the body in frame is punching to the right or not.
    You need to call this class again once instanciated to update the data.

    Attributes:
        read (bool): whether or not the body is punching or not
        magnitude (int): speed over the threshold 

    Methods:
        __call__(kinect: PyKinectV2, body: PyKinectRuntime.KinectBody) -> None: updates the read according to whether or not the body is punching or not.
        get_speed_threshhold() -> int: get the speed threashold needed to be reached to allow a punch to be recognised.
        set_speed_threshhold(x: int) -> None: set the speed threashold needed to be reached to allow a punch to be recognised.
    """

    def __init__(self):
        """
        Creates the RightPunch object
        """
        self._angle_threshhold = 20
        self.read = False
        self.magnitude = 0

    def __call__(self, body: PyKinectRuntime.KinectBody, depth, joint_points, joint_points_depth) -> bool:
        """
        Calling RightPunch with these perameters updates the read according to whether or not the body is punching or not.

        Args:
            kinect (PyKinectV2): 
                A reference to a PyKinectRuntime object.
            body (PyKinectRuntime.KinectBody): 
                A body being tracked in the frame.
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
        Gets the speed threashold needed to be reached to allow a punch to be recognised.

        Returns:
            int: the speed threashold needed to be reached to allow a punch to be recognised.
        """
        return self._angle_threshhold

    def set_angle_threshhold(self, x: int) -> None:
        """
        Sets the speed threashold needed to be reached to allow a punch to be recognised.

        Args:
            x (int): the new speed threashold needed to be reached to allow a punch to be recognised.
        """
        self._angle_threshhold = x
