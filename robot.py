from datetime import datetime
from motion_control import MotionControl
from velocity_motion_model import VelocityMotionModel
import numpy as np
import time

class Robot():
    #VELOCITY MAGNITUDES MUST BE IN UNIT/SECOND

    rotation_magnitude = 0
    translation_magnitude = 0
    model_timestamp = None
    

    def __init__(self, track_spacing, initial_pose=np.array([[0,0,0]])):
        self.pose = initial_pose
        self.motion_controller = MotionControl(enable_pin_left=14, forward_pin_left=15, reverse_pin_left=18, enable_pin_right=17, forward_pin_right=27, reverse_pin_right=22)
        self.track_spacing = track_spacing
        #TODO set correct alphas
        alphas = np.array([0.001, 0.001, 0.001, 0.001, 0.001, 0.001])
        self.vmm = VelocityMotionModel(alphas, self.pose, sample_size=10)

    def move_to_target(self, target_pose):
        x_t, y_t, theta_t = target_pose
        #TODO
        print('move_to_target is not implemented.')
        return True

    def rotate(self, magnitude):
        self.update_model()
        self.rotation_magnitude = magnitude
        if self.rotation_magnitude != 0:
            self.motion_controller.rotate('right', self.rotation_magnitude)
        elif self.rotation_magnitude > 0:
            self.motion_controller.rotate('left', self.rotation_magnitude)
        else:
        #if self.rotation_magnitude == 0:
            self.rotation_magnitude = 0
        return True
    
    def traverse(self, magnitude):
        self.update_model()        
        self.translation_magnitude = magnitude
        if self.translation_magnitude > 0:
            self.motion_controller.forward(self.translation_magnitude)
        elif self.translation_magnitude < 0:
            self.motion_controller.reverse(-self.translation_magnitude)
        else:           
        #if not self.translation_magnitude > 0:
            self.translation_magnitude = 0
        return True

    def stop(self):
        self.update_model()
        self.motion_controller.stop()
        self.rotation_magnitude, self.translation_magnitude = 0, 0


    def update_model(self):
        if(self.translation_magnitude != 0 or self.rotation_magnitude != 0):
            displacement = [self.translation_magnitude, (self.track_spacing / 2) * self.rotation_magnitude]
            self.vmm.update(displacement, (datetime.now() - self.model_timestamp).total_seconds())
        self.model_timestamp = datetime.now()

    def graph_motion(self):
        self.vmm.graph()

if __name__ == '__main__':

    robot = Robot(1)

    robot.traverse(10)
    time.sleep(1)
    #robot.update_model()
    #time.sleep(0.5)
    robot.stop()
    time.sleep(0.1)
    robot.rotate(1)
    time.sleep(1)
    robot.stop()
    time.sleep(0.1)
    robot.traverse(10)
    time.sleep(1)
    robot.stop()
    robot.graph_motion()