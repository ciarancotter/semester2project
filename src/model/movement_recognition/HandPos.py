from numpy import ndarray, interp
from pykinect2 import PyKinectV2
from pykinect2 import PyKinectRuntime


class HandPos(object):
    """The handpos Class is used to where the right hand is in frame.
    You need to call this class again once instanciated to update the data.

    Attributes:
      x (int):
        the x coordinate in range width
      y (int):
        the y coordinate in range height

    Methods:
      __call__(kinect: PyKinectV2, body: PyKinectRuntime.KinectBody) -> None:
        updates the read according to where the right hand is in frame.
    """

    def __init__(self, height: int, width: int):
        """Creates the handpos object
        
        Args:
          height (int):
            the range to scale the y between 0 and height.
          width (int):
            the range to scale the x between 0 and width.
        """
        self.x = 0
        self.y = 0
        self._height = height
        self._width = width

    def __call__(self, body: PyKinectRuntime.KinectBody, depth:ndarray, joint_points:ndarray) -> None:
        """Calling handpos with these perameters updates the read according to where the right hand is in frame.

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
        posy = joint_points[point_id].y

        self.x = interp(posx, [300, 1780], [0, self._width])
        self.y = interp(posy, [20, 1080], [0, self._height])