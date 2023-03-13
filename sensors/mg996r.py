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

    def update_dc_value(self, value):
        self.p.ChangeDutyCycle(value)

if __name__ == '__main__':
    pin = 3
    low = 4.92
    high = 9.778
    GPIO.setmode(GPIO.BOARD)
    print("Executing SG90 test on pin: " + str(pin))
    print("Low Duty Cycle threshold set to : " + str(low))
    print("High Duty Cycle threshold set to : " + str(high))
    sg90 = MG996R(GPIO, pin, low, high)

    print("setting 0%...")
    sg90.update_angle(-180)
    time.sleep(3)
    print("setting 90%...")
    sg90.update_angle(0)
    time.sleep(3)
    print("setting 180%...")
    sg90.update_angle(180)
    time.sleep(3)

    print("Test complete...")
    GPIO.cleanup()


#low = 5
#high = 10

#sg90.update_angle(-185.75)
#time.sleep(1)
#print("setting 90%...")
#sg90.update_angle(-5.75)
#time.sleep(1)
#print("setting 180%...")
#sg90.update_angle(164)