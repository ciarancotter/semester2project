from numpy import ndarray
from pykinect2 import PyKinectV2
from pykinect2 import PyKinectRuntime


class LeftPunch(object):
    """The LeftPunch Class is used to sense whether or the body in frame is punching to the left or not.
    You need to call this class again once instanciated to update the data.

    Attributes:
      read (bool):
        whether or not the body is punching or not
      magnitude (int):
        speed over the threshold

    Methods:
      __call__(kinect: PyKinectV2, body: PyKinectRuntime.KinectBody) -> None:
        updates the read according to whether or not the body is punching or not.
      get_speed_threshhold() -> int:
        get the speed threashold needed to be reached to allow a punch to be recognised
      set_speed_threshhold(x: int) -> None:
        set the speed threashold needed to be reached to allow a punch to be recognised.
    """

    def __init__(self):
        """Creates the LeftPunch object
        """
        self._olddelt = 0
        self._speed_threshhold = 40
        self.read = False
        self.magnitude = 0

    def __call__(self, body: PyKinectRuntime.KinectBody, depth: ndarray,
                 joint_points: ndarray) -> None:
        """Calling LeftPunch with these perameters updates the read according to whether or not the body is punching or not.

        Args:
          body (PyKinectRuntime.KinectBody):
            A body being tracked in the frame.
          depth (ndarray):
            The array of depth points from the kinect
          joint_points (ndarray):
            The array of joint point poitions from the kinect
        """

        joints = body.joints
        point_id = PyKinectV2.JointType_HandLeft
        point = joints[point_id].TrackingState

        # both joints are not tracked
        if point == PyKinectV2.TrackingState_NotTracked:
            return
        # both joints are not *really* tracked
        if point == PyKinectV2.TrackingState_Inferred:
            return

        posx = joint_points[point_id].x

        # a=0.9 == fast react      a=0.1 == slow react
        max_change_per_itteration = 0.4  # change per itteration
        delt = max_change_per_itteration * posx + (
            1 - max_change_per_itteration) * self._olddelt

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
        """Gets the speed threashold needed to be reached to allow a punch to be recognised.

        Returns:
          int:
            the speed threashold needed to be reached to allow a punch to be recognised.
        """
        return self._speed_threshhold

    def set_speed_threshhold(self, x: int) -> None:
        """Sets the speed threashold needed to be reached to allow a punch to be recognised.

        Args:
          x (int):
            the new speed threashold needed to be reached to allow a punch to be recognised.
        """
        self._speed_threshhold = x


class RightPunch(object):
    """The RightPunch Class is used to sense whether or the body in frame is punching to the right or not.
    You need to call this class again once instanciated to update the data.

    Attributes:
      read (bool):
        whether or not the body is punching or not
      magnitude (int):
        speed over the threshold

    Methods:
      __call__(kinect: PyKinectV2, body: PyKinectRuntime.KinectBody) -> None:
        updates the read according to whether or not the body is punching or not.
      get_speed_threshhold() -> int:
        get the speed threashold needed to be reached to allow a punch to be recognised.
      set_speed_threshhold(x: int) -> None:
        set the speed threashold needed to be reached to allow a punch to be recognised.
    """

    def __init__(self):
        """Creates the RightPunch object
        """
        self._olddelt = 0
        self._speed_threshhold = 40
        self.read = False
        self.magnitude = 0

    def __call__(self, body: PyKinectRuntime.KinectBody, depth: ndarray,
                 joint_points: ndarray) -> None:
        """Calling RightPunch with these perameters updates the read according to whether or not the body is punching or not.

        Args:
          body (PyKinectRuntime.KinectBody):
            A body being tracked in the frame.
          depth (ndarray):
            The array of depth points from the kinect
          joint_points (ndarray):
            The array of joint point poitions from the kinect
        """
        joints = body.joints
        point_id = PyKinectV2.JointType_HandRight
        point = joints[point_id].TrackingState

        # both joints are not tracked
        if point == PyKinectV2.TrackingState_NotTracked:
            return
        # both joints are not *really* tracked
        if point == PyKinectV2.TrackingState_Inferred:
            return

        posx = joint_points[point_id].x

        # a=0.9 == fast react      a=0.1 == slow react
        max_change_per_itteration = 0.4  # change per itteration

        delt = max_change_per_itteration * posx + (
            1 - max_change_per_itteration) * self._olddelt

        move = round(delt - self._olddelt, 3)
        self._olddelt = delt

        if move > self._speed_threshhold:
            self.read = True
            self.magnitude = move - self._speed_threshhold
            return
        else:
            self.read = False
            self.magnitude = 0
            return

    def get_speed_threshhold(self) -> int:
        """Gets the speed threashold needed to be reached to allow a punch to be recognised.

        Returns:
          int:
            the speed threashold needed to be reached to allow a punch to be recognised.
        """
        return self._speed_threshhold

    def set_speed_threshhold(self, x: int) -> None:
        """Sets the speed threashold needed to be reached to allow a punch to be recognised.

        Args:
          x (int):
            the new speed threashold needed to be reached to allow a punch to be recognised.
        """
        self._speed_threshhold = x
