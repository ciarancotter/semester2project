from pykinect2 import PyKinectV2, PyKinectRuntime
from pykinect2.PyKinectV2 import *

import numpy
import pygame
import ctypes

from punch import LeftPunch, RightPunch
from jump import Jump
from infront import HandInfront
from raiselegs import LeftWalk, RightWalk
from turnhips import TurnHips
from mouse import handpos
"""
Worked on from the PyKinectBodyGame example packed with the pykinect2 libary
"""

class TestMovement(object):
    """
    The TestMovment Class is used to test the movement sensing functions within this directory
    It creates a pygame instance to show what the kinect sees, and what we use to controll the game
    Methods:
    - draw_color_frame(frame: ndarray, target_surface: ndarray) -> None : Draws the current frame to the screen
    - draw_body_bone(joints: numpy.ndarray, jointpoints: numpy.ndarray, color: str, joint0: int, joint1: int) -> None : Draws the lines between the joints
    - run() -> None : runs the pygame instance loop 
    """

    def __init__(self):
        """
        Creates the TestMovement object
        """
        #draw switch
        self.draw = True
        
        pygame.init()

        # Used to manage how fast the screen updates
        self._clock = pygame.time.Clock()

        if self.draw:
            # Set the width and height of the screen [width, height]
            self._infoobject = pygame.display.Info()
            self._screen = pygame.display.set_mode(
                (self._infoobject.current_w >> 1, self._infoobject.current_h >> 1),
                pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE, 32)

            pygame.display.set_caption("Kinect for Windows v2 Body Game")

        # Loop until the user clicks the close button.
        self._done = False

        # Used to manage how fast the screen updates
        self._clock = pygame.time.Clock()

        # Kinect runtime object, we want only color and body frames
        self._kinect = PyKinectRuntime.PyKinectRuntime( PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Body | PyKinectV2.FrameSourceTypes_Depth)
        
        if self.draw:
            # back buffer surface for getting Kinect color frames, 32bit color, width and height equal to the Kinect color frame size
            self._frame_surface = pygame.Surface(
                (self._kinect.color_frame_desc.Width,
                self._kinect.color_frame_desc.Height), 0, 32)

        # here we will store skeleton data
        self._bodies = None
        self._bodyid = -1
        self._depth = None

        self._leftpunch = LeftPunch()
        self._rightpunch = RightPunch()
        self._jump = Jump()
        self._select = HandInfront()
        self._leftwalk = LeftWalk()
        self._rightwalk = RightWalk()
        self._turntest = TurnHips()
        self._mouse = handpos(100, 100)

    def draw_color_frame(self, frame: numpy.ndarray,
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

    def draw_body_bone(self, joints: numpy.ndarray, jointpoints: numpy.ndarray,
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

    def run(self) -> None:
        """
        Runs the pygame loop
        """
        # -------- Main Program Loop -----------
        while not self._done:
        # --- Main event loop
            for event in pygame.event.get():  # User did something
                if event.type == pygame.QUIT:  # If user clicked close
                    self._done = True  # Flag that we are done so we exit this loop

                elif self.draw:
                    if event.type == pygame.VIDEORESIZE:  # window resized
                        self._screen = pygame.display.set_mode(
                            event.dict["size"],
                            pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE,
                            32)

            # --- Game logic should go here

            # --- Getting frames and drawing
            # --- Woohoo! We've got a color frame! Let's fill out back buffer surface with frame's data
            if self.draw:
                if self._kinect.has_new_color_frame():
                    colorframe = self._kinect.get_last_color_frame()        # colorframe is linear array of uint8 as 1920*1080 samples of R,G,B,D = 8294400 bytes
                    self.draw_color_frame(colorframe, self._frame_surface)
                    colorframe = None

            # --- Cool! We have a body frame, so can get skeletons
            if self._kinect.has_new_body_frame():
                self._bodies = self._kinect.get_last_body_frame()

            if self._kinect.has_new_depth_frame():
                depthframe = self._kinect.get_last_depth_frame()        # depthframe is linear array of uint16 as 512*424 samples of D = 217088 bytes
                depthframe = depthframe.reshape(self._kinect.depth_frame_desc.Height, self._kinect.depth_frame_desc.Width)
                self._depth = self._kinect.depth_frame_to_color_space(depthframe)
                
                '''
                # Transform the depth frame values to pixel brightness
                self._depth = 255 * (self._depth / 5)  # self._depth values are in metres, so full white = 5 metres here
                self._depth = numpy.reshape(self._depth.clip(0, 255), self._depth.shape + (1,)).astype(numpy.uint8)
                self._depth = numpy.repeat(self._depth, 4, axis=2)    # RGBx
                # Display the frame
                #self.draw_color_frame(self._depth, self._frame_surface)
                depthframe = None
                self._depth = None'''

            # --- draw skeletons to _frame_surface
            if self._bodies is not None:
                for i in range(0, self._kinect.max_body_count):
                    body = self._bodies.bodies[i]
                    
                    if not body.is_tracked:
                        self._bodyid = -1
                        continue
                    
                    if self._bodyid == -1:
                        self._bodyid = body.tracking_id
                    '''
                    if self._bodyid not in self._bodies.bodies:
                        self._bodyid = -1
                    '''
                    if self._bodyid == body.tracking_id:

                        joints = body.joints
                        joint_points = self._kinect.body_joints_to_color_space(joints)

                        
                        rightpunchcol = "yellow"
                        self._rightpunch(body, self._depth, joint_points)
                        if self._rightpunch.read:
                            rightpunchcol = "blue"

                        leftpunchcol = "red"
                        self._leftpunch(body, self._depth, joint_points)
                        if self._leftpunch.read:
                            leftpunchcol = "blue"

                        jumpcol = "green"
                        self._jump(body, self._depth, joint_points)
                        if self._jump.read:
                            jumpcol = "blue"
                        

                        selectcol = "white"
                        self._select(body, self._depth, joint_points)
                        if self._select.read:
                            selectcol = "blue"
                        
                        rightwalkcol = "orange"
                        self._rightwalk(body, self._depth, joint_points)
                        if self._rightwalk.read:
                            rightwalkcol = "blue"

                        leftwalkcol = "pink"
                        self._leftwalk(body, self._depth, joint_points)
                        if self._leftwalk.read:
                            leftwalkcol = "blue"

                        turncol = "grey"
                        self._turntest(body, self._depth, joint_points)
                        if self._turntest.readleft:
                            turncol = "red"
                        if self._turntest.readright:
                            turncol = "blue"

                        '''
                        mousecol = "green"
                        self._mouse(body, self._depth, joint_points)'''

                        
                        if self.draw:
                            # Draw right punch
                            self.draw_body_bone(joints, joint_points, rightpunchcol,
                                                PyKinectV2.JointType_ShoulderRight,
                                                PyKinectV2.JointType_ElbowRight)
                            self.draw_body_bone(joints, joint_points, rightpunchcol,
                                                PyKinectV2.JointType_ElbowRight,
                                                PyKinectV2.JointType_WristRight)
                            pygame.draw.circle(
                                self._frame_surface, rightpunchcol,
                                (joint_points[PyKinectV2.JointType_HandRight].x,
                                joint_points[PyKinectV2.JointType_HandRight].y), 15)
                            rectangle = pygame.Rect(110, 55, 50, 50)
                            pygame.draw.rect(self._frame_surface, rightpunchcol, rectangle)

                            # Draw left punch
                            self.draw_body_bone(joints, joint_points, leftpunchcol,
                                                PyKinectV2.JointType_ShoulderLeft,
                                                PyKinectV2.JointType_ElbowLeft)
                            self.draw_body_bone(joints, joint_points, leftpunchcol,
                                                PyKinectV2.JointType_ElbowLeft,
                                                PyKinectV2.JointType_WristLeft)
                            pygame.draw.circle(
                                self._frame_surface, leftpunchcol,
                                (joint_points[PyKinectV2.JointType_HandLeft].x,
                                joint_points[PyKinectV2.JointType_HandLeft].y), 15)
                            rectangle = pygame.Rect(0, 55, 50, 50)
                            pygame.draw.rect(self._frame_surface, leftpunchcol, rectangle)

                            # Draw jump
                            pygame.draw.circle(
                                self._frame_surface, jumpcol,
                                (joint_points[PyKinectV2.JointType_SpineShoulder].x,
                                joint_points[PyKinectV2.JointType_SpineShoulder].y), 15)
                            rectangle = pygame.Rect(55, 55, 50, 50)
                            pygame.draw.rect(self._frame_surface, jumpcol, rectangle)

                            # Draw select
                            pygame.draw.circle(
                                self._frame_surface, selectcol,
                                (joint_points[PyKinectV2.JointType_HandRight].x,
                                joint_points[PyKinectV2.JointType_HandRight].y-30), 15)
                            rectangle = pygame.Rect(110, 0, 50, 50)
                            pygame.draw.rect(self._frame_surface, selectcol, rectangle)

                            # Draw right walk
                            self.draw_body_bone(joints, joint_points, rightwalkcol,
                                                PyKinectV2.JointType_HipRight,
                                                PyKinectV2.JointType_KneeRight)
                            self.draw_body_bone(joints, joint_points, rightwalkcol,
                                                PyKinectV2.JointType_KneeRight,
                                                PyKinectV2.JointType_AnkleRight)
                            pygame.draw.circle(
                                self._frame_surface, rightwalkcol,
                                (joint_points[PyKinectV2.JointType_AnkleRight].x,
                                joint_points[PyKinectV2.JointType_AnkleRight].y), 15)
                            rectangle = pygame.Rect(110, 110, 50, 50)
                            pygame.draw.rect(self._frame_surface, rightwalkcol, rectangle)

                            # Draw left walk
                            self.draw_body_bone(joints, joint_points, leftwalkcol,
                                                PyKinectV2.JointType_HipLeft,
                                                PyKinectV2.JointType_KneeLeft)
                            self.draw_body_bone(joints, joint_points, leftwalkcol,
                                                PyKinectV2.JointType_KneeLeft,
                                                PyKinectV2.JointType_AnkleLeft)
                            pygame.draw.circle(
                                self._frame_surface, leftwalkcol,
                                (joint_points[PyKinectV2.JointType_AnkleLeft].x,
                                joint_points[PyKinectV2.JointType_AnkleLeft].y), 15)
                            rectangle = pygame.Rect(0, 110, 50, 50)
                            pygame.draw.rect(self._frame_surface, leftwalkcol, rectangle)

                            # Draw turn
                            self.draw_body_bone(joints, joint_points, turncol,
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
                            
                            '''
                            # Draw mouse
                            pygame.draw.circle(
                                self._frame_surface, mousecol,
                                (joint_points[PyKinectV2.JointType_HandRight].x,
                                joint_points[PyKinectV2.JointType_HandRight].y), 15)
                            '''

            if self.draw:
                # --- copy back buffer surface pixels to the screen, resize it if needed and keep aspect ratio
                # --- (screen size may be different from Kinect's color frame size)
                h_to_w = float(self._frame_surface.get_height()
                            ) / self._frame_surface.get_width()
                target_height = int(h_to_w * self._screen.get_width())
                surface_to_draw = pygame.transform.scale(
                    self._frame_surface, (self._screen.get_width(), target_height))
                self._screen.blit(surface_to_draw, (0, 0))
                surface_to_draw = None

                # --- Go ahead and update the screen with what we've drawn.
                pygame.display.flip()

            #print(self._clock.get_fps())
            # --- Limit to 60 frames per second
            self._clock.tick(60)

        # Close our Kinect sensor, close the window and quit.
        self._kinect.close()
        pygame.quit()


if __name__ == "__main__":
    test = TestMovement()
    test.run()
