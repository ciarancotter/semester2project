from pykinect2 import PyKinectV2, PyKinectRuntime
from pykinect2.PyKinectV2 import *

import sys
import os
sys.path.append(os.path.abspath("./src"))
print(sys.path)

from shared_memory_dict import SharedMemoryDict

from model.movement_recognition.HandInfront import HandInfront
from model.movement_recognition.HandPos import HandPos
from model.movement_recognition.Jump import Jump
from model.movement_recognition.Punch import LeftPunch, RightPunch
from model.movement_recognition.RaiseLegs import RaiseLeftLeg, RaiseRightLeg
from model.movement_recognition.TurnHips import TurnHips


class MovementHandler(object):

    def __init__(self, screenhight:int, screenwidth:int):
        """
        Creates the MovementHandler object
        """
        # Kinect runtime object, we want only color and body frames
        self._kinect = PyKinectRuntime.PyKinectRuntime( PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Body | PyKinectV2.FrameSourceTypes_Depth)

        # here we will store skeleton data
        self._bodies = None
        self._bodyid = -1
        self._depth = None

        self.select = HandInfront()
        self.mouse = HandPos(screenhight, screenwidth)
        self.jump = Jump()
        self.leftpunch = LeftPunch()
        self.rightpunch = RightPunch()
        self.leftwalk = RaiseRightLeg()
        self.rightwalk = RaiseLeftLeg()
        self.turntest = TurnHips()

        self.movementPoolRead = SharedMemoryDict(name='movementPoolRead', size=1024)
        self.movementPoolMisc = SharedMemoryDict(name='movementPoolMisc', size=1024)

        self.movementPoolRead["select"] = self.select.read
        self.movementPoolRead["jump"] = self.jump.read
        self.movementPoolRead["leftpunch"] = self.leftpunch.read
        self.movementPoolRead["rightpunch"] = self.rightpunch.read
        self.movementPoolRead["leftwalk"] = self.leftwalk.read
        self.movementPoolRead["rightwalk"] = self.rightwalk.read

        self.movementPoolMisc["mousex"] = self.mouse.x
        self.movementPoolMisc["mousey"] = self.mouse.y
        self.movementPoolMisc["turntest"] = self.turntest.readleft
        self.movementPoolMisc["turntest"] = self.turntest.readright
        self.movementPoolMisc["jumpmagnitude"] = self.jump.magnitude
        self.movementPoolMisc["leftpunchmagnitude"] = self.leftpunch.magnitude
        self.movementPoolMisc["rightpunchmagnitude"] = self.rightpunch.magnitude


    def update(self):
        if self._kinect.has_new_body_frame():
                self._bodies = self._kinect.get_last_body_frame()

        if self._kinect.has_new_depth_frame():
            depthframe = self._kinect.get_last_depth_frame()        # depthframe is linear array of uint16 as 512*424 samples of D = 217088 bytes
            depthframe = depthframe.reshape(self._kinect.depth_frame_desc.Height, self._kinect.depth_frame_desc.Width)
            self._depth = self._kinect.depth_frame_to_color_space(depthframe)
        
        if self._bodies is not None:
            for i in range(0, self._kinect.max_body_count):
                body = self._bodies.bodies[i]
                
                if not body.is_tracked:
                    self._bodyid = -1
                    continue
                
                if self._bodyid == -1:
                    self._bodyid = body.tracking_id

                if self._bodyid == body.tracking_id:
                    joints = body.joints
                    joint_points = self._kinect.body_joints_to_color_space(joints)

                    self.mouse(body, self._depth, joint_points)
                    self.select(body, self._depth, joint_points)
                    self.jump(body, self._depth, joint_points)
                    self.rightpunch(body, self._depth, joint_points)
                    self.leftpunch(body, self._depth, joint_points)
                    self.rightwalk(body, self._depth, joint_points)
                    self.leftwalk(body, self._depth, joint_points)
                    self.turntest(body, self._depth, joint_points)

        self.movementPoolRead["select"] = self.select.read
        self.movementPoolRead["jump"] = self.jump.read
        self.movementPoolRead["leftpunch"] = self.leftpunch.read
        self.movementPoolRead["rightpunch"] = self.rightpunch.read
        self.movementPoolRead["leftwalk"] = self.leftwalk.read
        self.movementPoolRead["rightwalk"] = self.rightwalk.read

        self.movementPoolMisc["mousex"] = self.mouse.x
        self.movementPoolMisc["mousey"] = self.mouse.y
        self.movementPoolMisc["turntest"] = self.turntest.readleft
        self.movementPoolMisc["turntest"] = self.turntest.readright
        self.movementPoolMisc["jumpmagnitude"] = self.jump.magnitude
        self.movementPoolMisc["leftpunchmagnitude"] = self.leftpunch.magnitude
        self.movementPoolMisc["rightpunchmagnitude"] = self.rightpunch.magnitude

        print(self.movementPoolRead)
        

if __name__ == '__main__':
    mv = MovementHandler(100, 100)
    while True:
        mv.update()