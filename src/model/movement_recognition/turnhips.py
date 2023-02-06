from numpy import ndarray
from pykinect2 import PyKinectV2
from pykinect2 import PyKinectRuntime

class TurnHips(object):
    """The TurnHips Class is used to sense whether or the body in frame is has its hips turned or not.
    You need to call this class again once instanciated to update the data.

    Attributes:
      read (bool): 
        whether or not the body is punching or not

    Methods:
      __call__(kinect: PyKinectV2, body: PyKinectRuntime.KinectBody) -> None:
        updates the read according to whether or not the body has its hips turned or not.
      get_diff_threshhold() -> int:
        get the difference threashold needed to be reached to allow a hip turn to be recognised
      set_diff_threshhold(x: int) -> None:
        set the difference threashold needed to be reached to allow a hip turn to be recognised.
    """

    def __init__(self):
        """Creates the TurnHips object
        """
        self._diff_threshhold = 0.05
        self.readleft = False
        self.readright = False

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
        points = (PyKinectV2.JointType_HipLeft, PyKinectV2.JointType_HipRight)

        for i in points:
            point = joints[i].TrackingState
            # both joints are not tracked
            if point == PyKinectV2.TrackingState_NotTracked:
                return None, None, None
            # both joints are not *really* tracked
            if point == PyKinectV2.TrackingState_Inferred:
                return None, None, None
        
        lefty = int(joint_points[PyKinectV2.JointType_HipLeft].y)
        if lefty > 1080:
            return
        leftx = int(joint_points[PyKinectV2.JointType_HipLeft].x)
        if leftx > 1920:
            return

        righty = int(joint_points[PyKinectV2.JointType_HipRight].y)
        if righty > 1080:
            return
        rightx = int(joint_points[PyKinectV2.JointType_HipRight].x)
        if rightx > 1920:
            return
    
        lhipDepth = depth[lefty, leftx]
        rhipDepth = depth[righty, rightx]

        difference = lhipDepth - rhipDepth

        if abs(difference) > self._diff_threshhold:
            if lhipDepth > rhipDepth:
                self.readleft = True
                self.readright = False
                return
            if lhipDepth < rhipDepth:
                self.readleft = False
                self.readright = True
                return
        else:
            self.readleft = False
            self.readright = False
            return

    
    def get_diff_threshhold(self) -> int:
        """Gets the difference threashold needed to be reached to allow a hip turn to be recognised.

        Returns:
          int: 
            the difference threashold needed to be reached to allow a hip turn to be recognised.
        """
        return self._diff_threshhold

    def set_diff_threshhold(self, x: int) -> None:
        """Sets the difference threashold needed to be reached to allow a hip turn to be recognised.

        Args:
          x (int):
            the new difference threashold needed to be reached to allow a hip turn to be recognised.
        """
        self._diff_threshhold = x