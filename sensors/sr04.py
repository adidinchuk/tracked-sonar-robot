#Libraries
import RPi.GPIO as GPIO
import time
import numpy as np
 
class SR04():

    sonic_speed = 34300 #sonic speed (34300 cm/s)

    def __init__(self, gpio, trigger_pin, echo_pin):
        self.gpio = gpio
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        self.gpio.setup(self.trigger_pin, gpio.OUT)
        self.gpio.setup(self.echo_pin, gpio.IN)
 
    def distance(self):
        # set Trigger to HIGH
        self.gpio.output(self.trigger_pin, True)    
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        self.gpio.output(self.trigger_pin, False)
    
        StartTime = time.time()
        StopTime = time.time()
    
        # save StartTime
        while self.gpio.input(self.echo_pin) == 0:
            StartTime = time.time()
    
        # save time of arrival
        while self.gpio.input(self.echo_pin) == 1:
            StopTime = time.time()
        
        distance = ((StopTime - StartTime) * self.sonic_speed) / 2
        
        return distance

    def measure_distance(self, number_of_reads=1, remove_outliers=False):
        values = []
        for i in range(number_of_reads):
            values.append(self.distance())

        values = np.array(values)
        
        if(number_of_reads > 2 and remove_outliers):
            values = self._strip_outliers(values)        

        return np.average(values)


    def _strip_outliers(np_array, m=2.):
        d = np.abs(np_array - np.median(np_array))
        mdev = np.median(d)
        s = d / (mdev if mdev else 1.)
        return np_array[s < m]

 
if __name__ == '__main__':

    #GPIO Mode (BOARD / BCM)
    GPIO.setmode(GPIO.BOARD)
    trigger_pin = 12
    echo_pin = 18
    sample_size = 2
    number_of_reads = 10
    sr04 = SR04(GPIO, trigger_pin, echo_pin)

    print("Executing SR04 test on trigger pin: " + str(trigger_pin) + " and control pin: " + str(echo_pin))
    print("Using sample size of: " + str(sample_size))
    print("Running " + str(number_of_reads) + " reads")
    
    for i in range(number_of_reads):
        dist = sr04.measure_distance(sample_size)
        print ("Measured Distance = %.1f cm" % dist)
        time.sleep(1)
 

    print("Testing completed")
    GPIO.cleanup()