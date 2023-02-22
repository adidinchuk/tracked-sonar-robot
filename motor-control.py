import RPi.GPIO as GPIO          
from time import sleep

class MotorControl():

    def __init__(self, gpio, enable_pin, forward_pin, reverse_pin, min_power):
        
        self._min_power = min_power
        self._range = 100 - self._min_power
        self._forward_pin = forward_pin
        self._reverse_pin = reverse_pin
        self._enable_pin = enable_pin
        self.gpio = gpio
        GPIO.setmode(self.gpio.BCM)

        GPIO.setup(self._forward_pin, self.gpio.OUT)
        GPIO.output(self._forward_pin, self.gpio.LOW)
        GPIO.setup(self._reverse_pin, self.gpio.OUT)
        GPIO.output(self._reverse_pin, self.gpio.LOW)      
        GPIO.setup(self._enable_pin, self.gpio.OUT)       
        
        self._enable = GPIO.PWM(self._enable_pin, 1000)
        self.static = True

    def set_velocity(self, magnitude):
        self.static = False

        if magnitude == 0:
            self.stop()
        elif magnitude > 0:
            self.gpio.output(self._forward_pin, self.gpio.HIGH)
            self.gpio.output(self._reverse_pin, self.gpio.LOW)          
        else:            
            self.gpio.output(self._forward_pin, self.gpio.LOW)
            self.gpio.output(self._reverse_pin, self.gpio.HIGH)     
        
        self._enable.ChangeDutyCycle(self._range * (magnitude/100) + self._min_power)

    def stop(self):        
        self.gpio.output(self._forward_pin, self.gpio.LOW)
        self.gpio.output(self._reverse_pin, self.gpio.LOW)
        self._enable.ChangeDutyCycle(0)
        self.static = True

if __name__ == '__main__':

    GPIO.setmode(GPIO.BCM)
    enable_pin = 25
    forward_pin = 23
    reverse_pin = 24
    print("\n")
    print("Running motor control test on pins e-", enable_pin, " f-", forward_pin, " r-", reverse_pin)
    print("s-stop #-for speed e-exit")
    print("\n")  

    motor_control = MotorControl(GPIO, enable_pin, forward_pin, reverse_pin, 20)
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