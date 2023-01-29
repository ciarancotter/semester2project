from pykinect2 import PyKinectV2
from pykinect2 import PyKinectRuntime


class Infront(object):
    """
    The Infront Class is used to sense whether or the body in frame has its hand up infront or not.
    You need to call this class again once instanciated to update the data.

    Attributes:
        read (bool): whether or not the hand is up infront or not.

    Methods:
        __call__(kinect: PyKinectV2, body: PyKinectRuntime.KinectBody) -> None : updates the read according to whether or not the hand is up infront or not.
        get_distance_threshhold() -> int : get the distance threashold needed to be reached to allow a jump to be recognised
        set_distance_threshhold(x: int) -> None : set the distance threashold needed to be reached to allow a jump to be recognised.
    """

    def __init__(self):
        """
        Creates the Jump object
        """
        self._distance_threshhold = 2000
        self.read = False

    def __call__(self,body: PyKinectRuntime.KinectBody, depth, joint_points, joint_points_depth) -> None:
        """
        Calling Jump with these perameters updates the read according to whether or not the body is jumping or not.

        Args:
            kinect (PyKinectV2): A reference to a PyKinectRuntime object.
            body (PyKinectRuntime.KinectBody): A body being tracked in the frame.
        """

        joints = body.joints
        point_id = PyKinectV2.JointType_HandRight
        point = joints[point_id].TrackingState
        joint_points_depth = kinect.body_joints_to_depth_space(joints)
        point_id = (PyKinectV2.JointType_HandRight, PyKinectV2.JointType_SpineShoulder)

        for i in point_id:
            point = joints[i].TrackingState

            # both joints are not tracked
            if point == PyKinectV2.TrackingState_NotTracked:
                return
            # both joints are not *really* tracked
            if point == PyKinectV2.TrackingState_Inferred:
                return

        #print(int(joint_points_depth[point_id].x), int(joint_points_depth[point_id].y))
        depths = (depth[int(joint_points_depth[PyKinectV2.JointType_HandRight].x), int(joint_points_depth[PyKinectV2.JointType_HandRight].y)], depth[int(joint_points_depth[PyKinectV2.JointType_SpineShoulder].x), int(joint_points_depth[PyKinectV2.JointType_SpineShoulder].y)])


        distance = depths[1]-depths[0]

        if distance > 60000:
            return

        if distance == 0:
            return

        #print(distance)
        if distance > self._distance_threshhold:
            self.read = True
            return
        else:
            self.read = False
            return

    def get_distance_threshhold(self) -> int:
        """
        Gets the distance threashold needed to be reached to allow a jump to be recognised.

        Returns:
            int: the distance threashold needed to be reached to allow a jump to be recognised.
        """
        return self._distance_threshhold

    def set_distance_threshhold(self, x: int) -> None:
        """
        Sets the distance threashold needed to be reached to allow a jump to be recognised.

        Args:
            x (int): the new distance threashold needed to be reached to allow a jump to be recognised.
        """
        self._distance_threshhold = x