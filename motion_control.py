from motor_control import MotorControl
import RPi.GPIO as GPIO  

class MotionControl:

    def __init__(self, forward_pin_left=17, reverse_pin_left=27, \
    forward_pin_right=22, reverse_pin_right=23, min_power=50):
        self.left_motor = MotorControl(GPIO, forward_pin_left, reverse_pin_left, min_power)
        self.right_motor = MotorControl(GPIO, forward_pin_right, reverse_pin_right, min_power)

    def forward(self, speed):
        self.move(speed)
        return True
    
    def reverse(self, speed):
        self.move(-speed)
        return True
    
    def rotate(self, direction, speed):
        if(direction == 'left'):
            self.left_motor.set_velocity(-speed)
            self.right_motor.set_velocity(speed)
        elif(direction == 'right'):        
            self.left_motor.set_velocity(speed)
            self.right_motor.set_velocity(-speed)
        else:
            return False
        return True
    
    def stop(self):
        self.left_motor.stop()
        self.right_motor.stop()
        return True

    def move(self, speed):
        self.left_motor.set_velocity(speed)
        self.right_motor.set_velocity(speed)
        return True
    
    def test_motors(self):
        print("Runing test on left motor.")
        self.left_motor.test()
        print("Runing test on right motor.")
        self.right_motor.test()

if __name__ == '__main__':

    position_control = MotionControl()

    print("\n")
    print("Running motor control test on default pins")
    print("s-stop f-forward r-reverse l-left r-right t-test e-exit")
    print("\n") 

    while(1):

        x=input()        

        if x=='s':
            print("stop")
            position_control.stop()
            x='z'

        elif x=='f':
            print("forward")
            position_control.forward(75)
            x='z'

        elif x=='r':
            print("reverse")
            position_control.reverse(75)
            x='z'
        
        elif x=='l':
            print("left")
            position_control.rotate(direction="left", speed=100)
            x='z'
        
        elif x=='t':
            print("right")
            position_control.rotate(direction="right", speed=100)
            x='z'
        
        elif x=='t':
            print("testing")
            position_control.test_motors()
            x='z'

        elif x=='e':
            GPIO.cleanup()
            break

        else:
            print("<<<  wrong data  >>>")
            print("please enter the defined data to continue.....")