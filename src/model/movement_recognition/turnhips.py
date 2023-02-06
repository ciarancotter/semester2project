from numpy import ndarray
from pykinect2 import PyKinectV2
from pykinect2 import PyKinectRuntime

class TurnHips(object):
    """The TurnHips Class is used to sense whether or the body in frame is has its hips turned or not.
    You need to call this class again once instanciated to update the data.

    Attributes:
      read (bool): 
        whether or not the body is punching or not
      magnitude (int):
        speed over the threshold 

    Methods:
      __call__(kinect: PyKinectV2, body: PyKinectRuntime.KinectBody) -> None:
        updates the read according to whether or not the body has its hips turned or not.
      get_speed_threshhold() -> int:
        get the speed threashold needed to be reached to allow a hip turn to be recognised
      set_speed_threshhold(x: int) -> None:
        set the speed threashold needed to be reached to allow a hip turn to be recognised.
    """

    def __init__(self):
        """Creates the TurnHips object
        """
        self._dist_threshhold = 80
        self.read = False
        self.magnitude = 0

    def __call__(self, body: PyKinectRuntime.KinectBody, depth:ndarray, joint_points:ndarray) -> None:
        """Calling LeftPunch with these perameters updates the read according to whether or not the body has its hips turned or not.

        Args:
          body (PyKinectRuntime.KinectBody):
            A body being tracked in the frame.
          depth (ndarray):
            The array of depth points from the kinect
          joint_points (ndarray):
            The array of joint point poitions from the kinect
        """

        joints = body.joints
        hipleft_point_id = PyKinectV2.JointType_HipLeft
        hipright_point_id = PyKinectV2.JointType_HipRight
        points = (hipleft_point_id, hipright_point_id)

        for i in points:
            point = joints[i].TrackingState
            # both joints are not tracked
            if point == PyKinectV2.TrackingState_NotTracked:
                return None, None, None
            # both joints are not *really* tracked
            if point == PyKinectV2.TrackingState_Inferred:
                return None, None, None
        
        dist = joint_points[hipright_point_id].x-joint_points[hipleft_point_id].x

        if dist < self._dist_threshhold:
            self.read = True
            self.magnitude = self._dist_threshhold - dist
            return
        else:
            self.read = False
            self.magnitude = 0
            return
    
    def get_dist_threshhold(self) -> int:
        """Gets the distance threashold needed to be reached to allow a hip turn to be recognised.

        Returns:
          int: 
            the distance threashold needed to be reached to allow a hip turn to be recognised.
        """
        return self._dist_threshhold

    def set_dist_threshhold(self, x: int) -> None:
        """Sets the distance threashold needed to be reached to allow a hip turn to be recognised.

        Args:
          x (int):
            the new distance threashold needed to be reached to allow a hip turn to be recognised.
        """
        self._dist_threshhold = x