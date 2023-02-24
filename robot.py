from motor_control import MotorControl
import RPi.GPIO as GPIO  

class Robot:

    def __init__(self, enable_pin_left=25, forward_pin_left=23, reverse_pin_left=24, \
    enable_pin_right=20, forward_pin_right=16, reverse_pin_right=12, min_power=50):
        self.left_motor = MotorControl(GPIO, enable_pin_left, forward_pin_left, reverse_pin_left, min_power)
        self.right_motor = MotorControl(GPIO, enable_pin_right, forward_pin_right, reverse_pin_right, min_power)

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
        self.left_motor.test()
        self.right_motor.test()

if __name__ == '__main__':
    robot = Robot()

    print("\n")
    print("Running motor control test on default pins")
    print("s-stop f-forward r-reverse l-left r-right e-exit")
    print("\n")  

    robot.test_motors()

    while(1):

        x=input()        

        if x=='s':
            print("stop")
            robot.stop()
            x='z'

        elif x=='f':
            print("forward")
            robot.forward(75)
            x='z'

        elif x=='r':
            print("reverse")
            robot.reverse(75)
            x='z'
        
        elif x=='l':
            print("left")
            robot.rotate(direction="left", speed=100)
            x='z'
        
        elif x=='r':
            print("right")
            robot.rotate(direction="right", speed=100)
            x='z'

        elif x=='e':
            GPIO.cleanup()
            break

        else:
            print("<<<  wrong data  >>>")
            print("please enter the defined data to continue.....")