import RPi.GPIO as GPIO          
from time import sleep
from copy import copy

class Speed():
    def __init__(self, pin):
        GPIO.setup(pin,GPIO.OUT)
        self.pin = GPIO.PWM(pin,100)
       
    def set(self, speed):
        self.pin.start(speed)


class Motor():
    def __init__(self, a, b):
        self.a = a 
        self.b = b
        GPIO.setup(a, GPIO.OUT)
        GPIO.setup(b, GPIO.OUT)

    def fw(self):
        GPIO.output(self.a, GPIO.HIGH)
        GPIO.output(self.b, GPIO.LOW)

    def rw(self):
        GPIO.output(self.a, GPIO.LOW)
        GPIO.output(self.b, GPIO.HIGH)

    def stop(self):
        GPIO.output(self.a, GPIO.LOW)
        GPIO.output(self.b, GPIO.LOW)


class Car():
    def __init__(self, rf, rr, lf, lr, speed, sensors):

        self.motors = []
        self.speed = speed
        self.sensors = sensors 

        for direction in ['rf', 'rr', 'lf', 'lr']:
            pins = locals()[direction]
            motor = Motor(*pins)
            setattr(self, direction, motor)
            self.motors.append(motor)

    def cleanup(self):
        self.sensors.close()


    def forward(self):
        [m.fw() for m in self.motors]

    def reverse(self):
        [m.rw() for m in self.motors]

    def stop(self):
        [m.stop() for m in self.motors]

    def precise_rotate(self,deg):
        self.sensors.update()
        while not hasattr(self.sensors, 'yaw'):
            self.sensors.update()
            sleep(0.1)
        target = copy(self.sensors.yaw) + deg
        if target > self.sensors.yaw:
            while (target > self.sensors.yaw):
                self.sensors.update()
                self.rotate(deg)
        elif target < self.sensors.yaw:
            while (target < self.sensors.yaw):
                self.sensors.update()
                self.rotate(deg)
        self.stop()







    def rotate(self,deg):
        if deg < 0:
            self.rf.fw()
            self.rr.fw()
            self.lf.rw()
            self.lr.rw()
        elif deg > 0:
            self.rf.rw()
            self.rr.rw()
            self.lf.fw()
            self.lr.fw()
