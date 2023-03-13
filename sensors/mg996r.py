import time
import RPi.GPIO as GPIO

class MG996R():

    def __init__(self, gpio, pin, low_dc, high_dc):
        gpio.setup(pin, gpio.OUT)
        self.p = gpio.PWM(pin,50)
        self.low = low_dc
        self.high = high_dc        
        self.p.start(self.get_dc_value(0))

    def get_dc_value(self, angle):        
        return ((angle + 90) / 180) * (self.high - self.low) + self.low

    def update_angle(self, angle):
        self.p.ChangeDutyCycle(self.get_dc_value(angle))

if __name__ == '__main__':
    pin = 3
    low = 5
    high = 10
    GPIO.setmode(GPIO.BOARD)
    print("Executing SG90 test on pin: " + str(pin))
    print("Low Duty Cycle threshold set to : " + str(low))
    print("High Duty Cycle threshold set to : " + str(high))
    sg90 = MG996R(GPIO, pin, low, high)

    print("setting 0%...")
    sg90.update_angle(-185.75)
    time.sleep(1)
    print("setting 90%...")
    sg90.update_angle(-5.75)
    time.sleep(1)
    print("setting 180%...")
    sg90.update_angle(170)
    time.sleep(1)
    print("Test complete...")
    GPIO.cleanup()