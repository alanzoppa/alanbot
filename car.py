import RPi.GPIO as GPIO          
from time import sleep, time
from copy import copy

class Speed():
    def __init__(self, pin):
        GPIO.setup(pin,GPIO.OUT)
        self.pin = GPIO.PWM(pin,100)
       
    def set(self, sp):
        self.vel = sp
        self.pin.start(sp)

    def accelerate(self, inc):
        if not 0 < self.vel+inc < 100:
            return
        self.set(self.vel+inc)

    def decelerate(self, inc):
        self.accelerate(inc * -1)


class Motor():
    def __init__(self, a, b, speed, label):
        self.label = label
        self.a = a 
        self.b = b
        self.speed = Speed(speed)
        GPIO.setup(a, GPIO.OUT)
        GPIO.setup(b, GPIO.OUT)

    def set_speed(self, sp):
        self.speed.set(sp)

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
    def __init__(self, rf, rr, lf, lr, sensors):

        self.motors = []
        self.sensors = sensors 

        for direction in ['rf', 'rr', 'lf', 'lr']:
            pins = locals()[direction]
            motor = Motor(*pins, direction)
            setattr(self, direction, motor)
            self.motors.append(motor)

        self.r = [self.rf, self.rr]
        self.l = [self.lf, self.lr]

    @classmethod
    def is_drifting(cls, prev, nxt):
        if abs(prev-nxt) < .01:
            return 0
        elif prev < nxt:
            return 1
        elif prev > nxt:
            return -1

    def compensate_drift(self, direction, forward=True):
        if direction == 0:
            return
        if not forward:
            direction = direction * -1
        [m.speed.accelerate(-1 * direction) for m in self.l]
        [m.speed.accelerate(direction) for m in self.r]

    def set_speed(self, sp):
        self.master_speed = sp
        [m.set_speed(sp) for m in self.motors]

    def cleanup(self):
        self.sensors.close()

    def approach(self, distance=20):
        self.wait_for_sensors()
        start_yaw = self.sensors.yaw
        start = time()
        prev_yaw, nxt_yaw = start_yaw, start_yaw
        while 0 < self.sensors.distance > distance:
            self.forward()
            self.sensors.update()
            prev_yaw, nxt_yaw = nxt_yaw, self.sensors.yaw
            drift_direction = Car.is_drifting(prev_yaw, nxt_yaw)
            self.compensate_drift(drift_direction)

            log = "{:.2f} cm, {:.2f}deg drift, {}".format(self.sensors.distance, (self.sensors.yaw - start_yaw), drift_direction)
            print(log)

        self.stop()
        end = time()
        return {"elapsed": end-start}

    def precise_timed_reverse(self, seconds):
        self.wait_for_sensors()
        start_yaw = self.sensors.yaw
        start = time()
        prev_yaw, nxt_yaw = start_yaw, start_yaw

        while time() < (start+seconds):
            self.reverse()
            self.sensors.update()
            prev_yaw, nxt_yaw = nxt_yaw, self.sensors.yaw

            drift_direction = Car.is_drifting(prev_yaw, nxt_yaw)
            self.compensate_drift(drift_direction, False)

            log = "{:.2f} cm, {:.2f}deg drift, {}".format(self.sensors.distance, (self.sensors.yaw - start_yaw), drift_direction)
            print(log)

        self.stop()


    def wait_for_sensors(self):
        self.sensors.update()
        while not hasattr(self.sensors, 'yaw'):
            self.sensors.update()
            sleep(0.1)


    def forward(self):
        [m.fw() for m in self.motors]

    def reverse(self):
        [m.rw() for m in self.motors]

    def stop(self, hard=False):
        if not hard:
            while any( [m.speed.vel > 5 for m in self.motors] ):
                [m.speed.decelerate(5) for m in self.motors]
                sleep(0.01)
        [m.stop() for m in self.motors]
        self.set_speed(self.master_speed)

    def precise_rotate(self,deg):
        self.wait_for_sensors()
        target = self.sensors.yaw + deg
        if target > self.sensors.yaw:
            while (target-2 > self.sensors.yaw):
                self.sensors.update()
                self.rotate(deg)
        elif target < self.sensors.yaw:
            while (target+2 < self.sensors.yaw):
                self.sensors.update()
                self.rotate(deg)
        self.stop(hard=True)







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
