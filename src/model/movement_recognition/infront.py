from numpy import ndarray
from pykinect2 import PyKinectV2
from pykinect2 import PyKinectRuntime


class HandInfront(object):
    """The HandInfront Class is used to sense whether or the body in frame has its hand up infront or not.
    You need to call this class again once instanciated to update the data.

    Attributes:
      read (bool): whether or not the hand is up infront or not.

    Methods:
      __call__(kinect: PyKinectV2, body: PyKinectRuntime.KinectBody) -> None:
        updates the read according to whether or not the hand is up infront or not.
      get_distance_threshhold() -> int:
        get the distance threashold needed to be reached to allow a hand in front to be recognised
      set_distance_threshhold(x: int) -> None:
        set the distance threashold needed to be reached to allow a hand in front to be recognised.
    """

    def __init__(self):
        """Creates the HandInfront object
        """
        self._distance_threshhold = 0.4
        self.read = False

    def __call__(self, body: PyKinectRuntime.KinectBody, depth: ndarray,
                 joint_points: ndarray) -> None:
        """Calling HandInfront with these perameters updates the read according to whether or not the body has a hand in front or not.

        Args:
          body (PyKinectRuntime.KinectBody):
            A body being tracked in the frame.
          depth (ndarray):
            The array of depth points from the kinect
          joint_points (ndarray):
            The array of joint point poitions from the kinect
        """

        joints = body.joints
        points = (PyKinectV2.JointType_HandRight,
                  PyKinectV2.JointType_SpineShoulder)

        for i in points:
            point = joints[i].TrackingState
            # both joints are not tracked
            if point == PyKinectV2.TrackingState_NotTracked:
                return None, None, None
            # both joints are not *really* tracked
            if point == PyKinectV2.TrackingState_Inferred:
                return None, None, None

        handy = int(joint_points[PyKinectV2.JointType_HandRight].y)
        if handy > 1079:
            return
        handx = int(joint_points[PyKinectV2.JointType_HandRight].x)
        if handx > 1919:
            return

        chesty = int(joint_points[PyKinectV2.JointType_SpineShoulder].y)
        if chesty > 1079:
            return
        chestx = int(joint_points[PyKinectV2.JointType_SpineShoulder].x)
        if chestx > 1919:
            return

        hand_depth = depth[handy, handx]
        chest_depth = depth[chesty, chestx]
        distance = chest_depth - hand_depth

        if (distance > self._distance_threshhold):
            self.read = True
            return
        else:
            self.read = False
            return

    def get_distance_threshhold(self) -> int:
        """Gets the distance threashold needed to be reached to allow a hand in front to be recognised.

        Returns:
          int:
            the distance threashold needed to be reached to allow a hand in front to be recognised.
        """
        return self._distance_threshhold

    def set_distance_threshhold(self, x: int) -> None:
        """Sets the distance threashold needed to be reached to allow a hand in front to be recognised.

        Args:
          x (int):
            the new distance threashold needed to be reached to allow a hand in front to be recognised.
        """
        self._distance_threshhold = x
