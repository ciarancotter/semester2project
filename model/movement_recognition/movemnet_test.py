from pykinect2 import PyKinectV2
from pykinect2 import PyKinectRuntime

import pygame
import ctypes

from punch import LeftPunch, RightPunch
'''
Worked on from the PyKinectBodyGame example packed with the pykinect2 libary
'''


class TestMovement(object):

    def __init__(self):
        pygame.init()

        # Used to manage how fast the screen updates
        self._clock = pygame.time.Clock()

        # Set the width and height of the screen [width, height]
        self._infoobject = pygame.display.Info()
        self._screen = pygame.display.set_mode(
            (self._infoObject.current_w >> 1, self._infoObject.current_h >> 1),
            pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE, 32)

        pygame.display.set_caption("Kinect for Windows v2 Body Game")

        # Loop until the user clicks the close button.
        self._done = False

        # Used to manage how fast the screen updates
        self._clock = pygame.time.Clock()

        # Kinect runtime object, we want only color and body frames
        self._kinect = PyKinectRuntime.PyKinectRuntime(
            PyKinectV2.FrameSourceTypes_Color |
            PyKinectV2.FrameSourceTypes_Body)
        #self._kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_BodyIndex)

        # back buffer surface for getting Kinect color frames, 32bit color, width and height equal to the Kinect color frame size
        self._frame_surface = pygame.Surface(
            (self._kinect.color_frame_desc.Width,
             self._kinect.color_frame_desc.Height), 0, 32)

        # here we will store skeleton data
        self._bodies = None

        self.leftpunch = LeftPunch()
        self.rightpunch = RightPunch()

    def draw_color_frame(self, frame, target_surface):
        target_surface.lock()
        address = self._kinect.surface_as_array(target_surface.get_buffer())
        ctypes.memmove(address, frame.ctypes.data, frame.size)
        del address
        target_surface.unlock()

    def draw_body_bone(self, joints, jointpoints, color, joint0, joint1):
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

    def run(self):
        # -------- Main Program Loop -----------
        while not self._done:
            # --- Main event loop
            for event in pygame.event.get():  # User did something
                if event.type == pygame.QUIT:  # If user clicked close
                    self._done = True  # Flag that we are done so we exit this loop

                elif event.type == pygame.VIDEORESIZE:  # window resized
                    self._screen = pygame.display.set_mode(
                        event.dict["size"],
                        pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE,
                        32)

            # --- Game logic should go here

            # --- Getting frames and drawing
            # --- Woohoo! We've got a color frame! Let's fill out back buffer surface with frame's data
            if self._kinect.has_new_color_frame():
                #print("colour drawn")
                frame = self._kinect.get_last_color_frame()
                self.draw_color_frame(frame, self._frame_surface)
                frame = None

            # --- Cool! We have a body frame, so can get skeletons
            if self._kinect.has_new_body_frame():
                self._bodies = self._kinect.get_last_body_frame()

            # --- draw skeletons to _frame_surface
            if self._bodies is not None:
                #print("body is there")
                for i in range(0, self._kinect.max_body_count):
                    body = self._bodies.bodies[i]
                    if not body.is_tracked:
                        continue

                    rightcol = "yellow"
                    self.rightpunch(self._kinect, body)
                    if self.rightpunch.read:
                        rightcol = "blue"

                    leftcol = "red"
                    self.leftpunch(self._kinect, body)
                    if self.leftpunch.read:
                        leftcol = "blue"

                    joints = body.joints
                    # convert joint coordinates to color space
                    joint_points = self._kinect.body_joints_to_color_space(
                        joints)

                    self.draw_body_bone(joints, joint_points, rightcol,
                                        PyKinectV2.JointType_ShoulderRight,
                                        PyKinectV2.JointType_ElbowRight)
                    self.draw_body_bone(joints, joint_points, rightcol,
                                        PyKinectV2.JointType_ElbowRight,
                                        PyKinectV2.JointType_WristRight)
                    pygame.draw.circle(
                        self._frame_surface, rightcol,
                        (joint_points[PyKinectV2.JointType_HandRight].x,
                         joint_points[PyKinectV2.JointType_HandRight].y), 15)
                    rectangle = pygame.Rect(55, 0, 50, 50)
                    pygame.draw.rect(self._frame_surface, rightcol, rectangle)

                    self.draw_body_bone(joints, joint_points, leftcol,
                                        PyKinectV2.JointType_ShoulderLeft,
                                        PyKinectV2.JointType_ElbowLeft)
                    self.draw_body_bone(joints, joint_points, leftcol,
                                        PyKinectV2.JointType_ElbowLeft,
                                        PyKinectV2.JointType_WristLeft)
                    pygame.draw.circle(
                        self._frame_surface, leftcol,
                        (joint_points[PyKinectV2.JointType_HandLeft].x,
                         joint_points[PyKinectV2.JointType_HandLeft].y), 15)
                    rectangle = pygame.Rect(0, 0, 50, 50)
                    pygame.draw.rect(self._frame_surface, leftcol, rectangle)

            # --- copy back buffer surface pixels to the screen, resize it if needed and keep aspect ratio
            # --- (screen size may be different from Kinect's color frame size)
            h_to_w = float(self._frame_surface.get_height()
                          ) / self._frame_surface.get_width()
            target_height = int(h_to_w * self._screen.get_width())
            surface_to_draw = pygame.transform.scale(
                self._frame_surface, (self._screen.get_width(), target_height))
            self._screen.blit(surface_to_draw, (0, 0))
            surface_to_draw = None
            pygame.display.update()

            # --- Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

            # --- Limit to 60 frames per second
            self._clock.tick(60)

        # Close our Kinect sensor, close the window and quit.
        self._kinect.close()
        pygame.quit()


if __name__ == "__main__":
    test = TestMovement()
    test.run()
