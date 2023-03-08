import ctypes
from pykinect2 import PyKinectV2, PyKinectRuntime
from pykinect2.PyKinectV2 import *

import sys
import os
sys.path.append(os.path.abspath("./src"))

import pygame
import numpy
from shared_memory_dict import SharedMemoryDict

from model.movement_recognition.HandInfront import HandInfront
from model.movement_recognition.HandPos import HandPos
from model.movement_recognition.jump import Jump
from model.movement_recognition.punch import LeftPunch, RightPunch
from model.movement_recognition.raiselegs import RaiseLeftLeg, RaiseRightLeg
from model.movement_recognition.turnhips import TurnHips


class MovementHandler(object):

    def __init__(self, screenhight:int, screenwidth:int):
        """
        Creates the MovementHandler object
        """
        # Kinect runtime object, we want only color and body frames
        self._kinect = PyKinectRuntime.PyKinectRuntime( PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Body | PyKinectV2.FrameSourceTypes_Depth)

        # back buffer surface for getting Kinect color frames, 32bit color, width and height equal to the Kinect color frame size
        self._frame_surface = pygame.Surface(
            (self._kinect.color_frame_desc.Width,
            self._kinect.color_frame_desc.Height), 0, 32)

        # here we will store skeleton data
        self._bodies = None
        self._bodyid = -1
        self._depth = None

        self.select = HandInfront()
        self.mouse = HandPos(screenhight, screenwidth)
        self.jump = Jump()
        self.leftpunch = LeftPunch()
        self.rightpunch = RightPunch()
        #self.leftwalk = RaiseRightLeg()
        #self.rightwalk = RaiseLeftLeg()
        self.turntest = TurnHips()

        self.movementPoolRead = SharedMemoryDict(name='movementPoolRead', size=1024)
        self.movementPoolMisc = SharedMemoryDict(name='movementPoolMisc', size=1024)
        self.video = SharedMemoryDict(name='movementVideo', size=500000)

        self.movementPoolRead["select"] = self.select.read
        self.movementPoolRead["jump"] = self.jump.read
        self.movementPoolRead["leftpunch"] = self.leftpunch.read
        self.movementPoolRead["rightpunch"] = self.rightpunch.read
        #self.movementPoolRead["leftwalk"] = self.leftwalk.read
        #self.movementPoolRead["rightwalk"] = self.rightwalk.read

        self.movementPoolMisc["mousex"] = self.mouse.x
        self.movementPoolMisc["mousey"] = self.mouse.y
        self.movementPoolMisc["turnleft"] = self.turntest.readleft
        self.movementPoolMisc["turnright"] = self.turntest.readright
        self.movementPoolMisc["jumpmagnitude"] = self.jump.magnitude
        self.movementPoolMisc["leftpunchmagnitude"] = self.leftpunch.magnitude
        self.movementPoolMisc["rightpunchmagnitude"] = self.rightpunch.magnitude

    def _draw_color_frame(self, frame: numpy.ndarray,
                            target_surface: pygame.Surface) -> None:
            """
            Draws the current frame to the screen
            Parameters:
            - frame (numpy.ndarray): The frame to draw.
            - target_surface (pygame.Surface): the surface to draw to.
            """

            target_surface.lock()
            address = self._kinect.surface_as_array(target_surface.get_buffer())
            ctypes.memmove(address, frame.ctypes.data, frame.size)
            del address
            target_surface.unlock()

    def _draw_body_bone(self, joints: numpy.ndarray, jointpoints: numpy.ndarray,
                       color: str, joint0: int, joint1: int) -> None:
        """
        Draws the lines between the joints
        Parameters:
        - joints (ndarray): the array of joinnts on the body
        - jointpoints (ndarray): the array of position of thoes points
        - color (str): the colour to draw the line
        - joint0 (int): first joint
        - joint1 (int): second joint
        """

        jointzerostate = joints[joint0].TrackingState
        jointonestate = joints[joint1].TrackingState
        # both joints are not tracked
        if (jointzerostate == PyKinectV2.TrackingState_NotTracked) or (
                jointonestate == PyKinectV2.TrackingState_NotTracked):
            return

        # both joints are not *really* tracked
        if (jointzerostate == PyKinectV2.TrackingState_Inferred) and (
                jointonestate == PyKinectV2.TrackingState_Inferred):
            return

        # ok, at least one is good
        start = (jointpoints[joint0].x, jointpoints[joint0].y)
        end = (jointpoints[joint1].x, jointpoints[joint1].y)

        # get vector of the line to 3dp
        #print(round(end[0], 3)-round(start[0], 3), round(end[1], 3)-round(start[1], 0))

        try:
            pygame.draw.line(self._frame_surface, color, start, end, 8)
        except:  # need to catch it due to possible invalid positions (with inf)
            pass


    def update(self):
        if self._kinect.has_new_color_frame():
            colorframe = self._kinect.get_last_color_frame()        # colorframe is linear array of uint8 as 1920*1080 samples of R,G,B,D = 8294400 bytes
            self._draw_color_frame(colorframe, self._frame_surface)
            colorframe = None

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
                    #self.rightwalk(body, self._depth, joint_points)
                    #self.leftwalk(body, self._depth, joint_points)
                    self.turntest(body, self._depth, joint_points)

                    selectcol = "white"
                    if self.select.read:
                        selectcol = "blue"
                    
                    mousecol = "green"

                    jumpcol = "green"
                    if self.jump.read:
                        jumpcol = "blue"

                    leftpunchcol = "red"
                    if self.leftpunch.read:
                        leftpunchcol = "blue"

                    rightpunchcol = "yellow"
                    if self.rightpunch.read:
                        rightpunchcol = "blue"

                    '''leftwalkcol = "pink"
                    if self.leftwalk.read:
                        leftwalkcol = "blue"                        

                    rightwalkcol = "orange"
                    if self.rightwalk.read:
                        rightwalkcol = "blue"'''

                    turncol = "grey"
                    if self.turntest.readleft:
                        turncol = "red"
                    if self.turntest.readright:
                        turncol = "blue"

                    # Draw select
                    pygame.draw.circle(
                        self._frame_surface, selectcol,
                        (joint_points[PyKinectV2.JointType_HandRight].x,
                        joint_points[PyKinectV2.JointType_HandRight].y-30), 15)
                    rectangle = pygame.Rect(110, 0, 50, 50)
                    pygame.draw.rect(self._frame_surface, selectcol, rectangle)

                    
                    # Draw mouse
                    pygame.draw.circle(
                        self._frame_surface, mousecol,
                        (joint_points[PyKinectV2.JointType_HandRight].x,
                        joint_points[PyKinectV2.JointType_HandRight].y), 15)
                    

                    # Draw jump
                    pygame.draw.circle(
                        self._frame_surface, jumpcol,
                        (joint_points[PyKinectV2.JointType_SpineShoulder].x,
                        joint_points[PyKinectV2.JointType_SpineShoulder].y), 15)
                    rectangle = pygame.Rect(55, 55, 50, 50)
                    pygame.draw.rect(self._frame_surface, jumpcol, rectangle)

                    # Draw left punch
                    self._draw_body_bone(joints, joint_points, leftpunchcol,
                                        PyKinectV2.JointType_ShoulderLeft,
                                        PyKinectV2.JointType_ElbowLeft)
                    self._draw_body_bone(joints, joint_points, leftpunchcol,
                                        PyKinectV2.JointType_ElbowLeft,
                                        PyKinectV2.JointType_WristLeft)
                    pygame.draw.circle(
                        self._frame_surface, leftpunchcol,
                        (joint_points[PyKinectV2.JointType_HandLeft].x,
                        joint_points[PyKinectV2.JointType_HandLeft].y), 15)
                    rectangle = pygame.Rect(0, 55, 50, 50)
                    pygame.draw.rect(self._frame_surface, leftpunchcol, rectangle)

                    # Draw right punch
                    self._draw_body_bone(joints, joint_points, rightpunchcol,
                                        PyKinectV2.JointType_ShoulderRight,
                                        PyKinectV2.JointType_ElbowRight)
                    self._draw_body_bone(joints, joint_points, rightpunchcol,
                                        PyKinectV2.JointType_ElbowRight,
                                        PyKinectV2.JointType_WristRight)
                    pygame.draw.circle(
                        self._frame_surface, rightpunchcol,
                        (joint_points[PyKinectV2.JointType_HandRight].x,
                        joint_points[PyKinectV2.JointType_HandRight].y), 15)
                    rectangle = pygame.Rect(110, 55, 50, 50)
                    pygame.draw.rect(self._frame_surface, rightpunchcol, rectangle)

                    '''# Draw left raise
                    self._draw_body_bone(joints, joint_points, leftwalkcol,
                                        PyKinectV2.JointType_HipLeft,
                                        PyKinectV2.JointType_KneeLeft)
                    self._draw_body_bone(joints, joint_points, leftwalkcol,
                                        PyKinectV2.JointType_KneeLeft,
                                        PyKinectV2.JointType_AnkleLeft)
                    pygame.draw.circle(
                        self._frame_surface, leftwalkcol,
                        (joint_points[PyKinectV2.JointType_AnkleLeft].x,
                        joint_points[PyKinectV2.JointType_AnkleLeft].y), 15)
                    rectangle = pygame.Rect(0, 110, 50, 50)
                    pygame.draw.rect(self._frame_surface, leftwalkcol, rectangle)

                    # Draw right raise
                    self._draw_body_bone(joints, joint_points, rightwalkcol,
                                        PyKinectV2.JointType_HipRight,
                                        PyKinectV2.JointType_KneeRight)
                    self._draw_body_bone(joints, joint_points, rightwalkcol,
                                        PyKinectV2.JointType_KneeRight,
                                        PyKinectV2.JointType_AnkleRight)
                    pygame.draw.circle(
                        self._frame_surface, rightwalkcol,
                        (joint_points[PyKinectV2.JointType_AnkleRight].x,
                        joint_points[PyKinectV2.JointType_AnkleRight].y), 15)
                    rectangle = pygame.Rect(110, 110, 50, 50)
                    pygame.draw.rect(self._frame_surface, rightwalkcol, rectangle)'''

                    # Draw turn
                    self._draw_body_bone(joints, joint_points, turncol,
                                        PyKinectV2.JointType_HipLeft,
                                        PyKinectV2.JointType_HipRight)
                    pygame.draw.circle(
                        self._frame_surface, turncol,
                        (joint_points[PyKinectV2.JointType_HipLeft].x,
                        joint_points[PyKinectV2.JointType_HipLeft].y), 15)
                    pygame.draw.circle(
                        self._frame_surface, turncol,
                        (joint_points[PyKinectV2.JointType_HipRight].x,
                        joint_points[PyKinectV2.JointType_HipRight].y), 15)
                    rectangle = pygame.Rect(55, 110, 50, 50)
                    pygame.draw.rect(self._frame_surface, turncol, rectangle)

        self.movementPoolRead["select"] = self.select.read
        self.movementPoolRead["jump"] = self.jump.read
        self.movementPoolRead["leftpunch"] = self.leftpunch.read
        self.movementPoolRead["rightpunch"] = self.rightpunch.read
        '''self.movementPoolRead["leftwalk"] = self.leftwalk.read
        self.movementPoolRead["rightwalk"] = self.rightwalk.read'''

        self.movementPoolMisc["mousex"] = self.mouse.x
        self.movementPoolMisc["mousey"] = self.mouse.y
        self.movementPoolMisc["turnleft"] = self.turntest.readleft
        self.movementPoolMisc["turnright"] = self.turntest.readright
        self.movementPoolMisc["jumpmagnitude"] = self.jump.magnitude
        self.movementPoolMisc["leftpunchmagnitude"] = self.leftpunch.magnitude
        self.movementPoolMisc["rightpunchmagnitude"] = self.rightpunch.magnitude

        #print(self.movementPoolMisc)

        surface_to_draw = pygame.transform.scale(self._frame_surface, (496, 279))
        vid = pygame.surfarray.array3d(surface_to_draw)
        self.video["src"] = vid
       

if __name__ == '__main__':
    mv = MovementHandler(1280, 784)
    while True:
        mv.update()