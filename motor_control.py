import RPi.GPIO as GPIO          
import time

class MotorControl():

    def __init__(self, gpio, forward_pin, reverse_pin, min_power):
        
        self._min_power = min_power
        self._range = 100 - self._min_power
        self._forward_pin = forward_pin
        self._reverse_pin = reverse_pin
        self.gpio = gpio
        self.gpio.setmode(self.gpio.BCM)

        self.gpio.setup(self._forward_pin, self.gpio.OUT)
        self.gpio.setup(self._reverse_pin, self.gpio.OUT)
   
        self.gpio.output(self._reverse_pin, self.gpio.LOW)      
        self.gpio.output(self._forward_pin, self.gpio.LOW)
        
        self._forward = self.gpio.PWM(self._forward_pin, 1000)
        self._reverse = self.gpio.PWM(self._reverse_pin, 1000)

        self._forward.start(0)
        self._reverse.start(0)

        self.static = True

    def set_velocity(self, magnitude):
        self.static = False

        if magnitude == 0:
            self.stop()
        elif magnitude > 0:
            self._forward.ChangeDutyCycle(self._range * (magnitude/100) + self._min_power) 
            self._reverse.ChangeDutyCycle(0) 
            self.gpio.output(self._forward_pin, self.gpio.HIGH)
            self.gpio.output(self._reverse_pin, self.gpio.LOW)
        else:      
            self._reverse.ChangeDutyCycle(self._range * (magnitude/100) + self._min_power) 
            self._forward.ChangeDutyCycle(0)       
            self.gpio.output(self._forward_pin, self.gpio.LOW)
            self.gpio.output(self._reverse_pin, self.gpio.HIGH)      

    def stop(self):        
        self.gpio.output(self._forward_pin, self.gpio.LOW)
        self.gpio.output(self._reverse_pin, self.gpio.LOW)
        self._forward.ChangeDutyCycle(0) 
        self._reverse.ChangeDutyCycle(0) 
        self.static = True

    def test(self):
        print("Executing motion test.")
        print("Velocity magnitude: 0", end='\r')
        for i in range(0, 100):
            print("Velocity magnitude: ", i, end='\r')
            self.set_velocity(i)
            time.sleep(0.2)
        
        for i in range(0, 100):
            print("Velocity magnitude: ", -i, end='\r')
            self.set_velocity(-i)
            time.sleep(0.2)
        print("")
        print("Test completed.")
        self.stop()


if __name__ == '__main__':

    GPIO.setmode(GPIO.BCM)
    enable_pin = 25
    forward_pin = 23
    reverse_pin = 24
    print("\n")
    print("Running motor control test on pins e-", enable_pin, " f-", forward_pin, " r-", reverse_pin)
    print("s-stop #-for speed e-exit")
    print("\n")  

    motor_control = MotorControl(GPIO, enable_pin, forward_pin, reverse_pin, 50)
    direction = 1
    speed = 0

    while(1):

        x=input()        

        if x=='s':
            print("stop")
            motor_control.stop()
            x='z'

        elif x.isnumeric():
            motor_control.set_velocity(int(x))
            x='z'

        elif x=='e':
            GPIO.cleanup()
            break
        
        else:
            print("<<<  wrong data  >>>")
            print("please enter the defined data to continue.....")