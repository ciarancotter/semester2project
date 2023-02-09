from numpy import ndarray, interp
from pykinect2 import PyKinectV2
from pykinect2 import PyKinectRuntime


class handpos(object):
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

    def __init__(self, height, width):
        """Creates the LeftPunch object
        """
        self.x = 0
        self.y = 0
        self._height = height
        self._width = width

    def __call__(self, body: PyKinectRuntime.KinectBody, depth:ndarray, joint_points:ndarray) -> None:
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

        #print(int(posx), int(posy))

        self.x = interp(posx, [300, 1780], [0, self._width])
        self.y = interp(posy, [20, 1080], [0, self._height])

        print(int(self.x), int(self.y))