import RPi.GPIO as GPIO          
from time import sleep


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
    def __init__(self, rf, rr, lf, lr, speed):

        self.rf = Motor(*rf)
        self.rr = Motor(*rr)
        self.lf = Motor(*lf)
        self.lr = Motor(*lr)

        self.motors = [self.rf, self.rr, self.lf, self.lr]
        self.speed = speed


    def forward(self):
        for motor in self.motors:
            motor.fw()


    def reverse(self):
        [m.rw() for m in self.motors]

    def stop(self):
        [m.stop() for m in self.motors]

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




if __name__ == "__main__":

    try:
        GPIO.setmode(GPIO.BCM)

        car = Car(rf=(23,24), rr=(27,22), lf=(5,6), lr=(19,26), speed=Speed(17))

        car.speed.set(50)

        car.forward()
        sleep(1)
        car.reverse()
        sleep(1)
        car.rotate(90)
        sleep(1)
        car.stop(90)

    except:

        GPIO.cleanup()
