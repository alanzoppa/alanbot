import RPi.GPIO as GPIO          
from time import sleep


from car import Car, Motor, Speed
from sensors import Sensors


if __name__ == "__main__":

    try:
        GPIO.setmode(GPIO.BCM)

        car = Car(rf=(23,24), rr=(27,22), lf=(5,6), lr=(19,26), speed=Speed(17), sensors=Sensors('/dev/ttyACM0'))

        car.speed.set(40)

        #car.forward()
        #sleep(1)
        #car.reverse()
        #sleep(1)

    except:
        pass

    car.precise_rotate(180)
    car.precise_rotate(-90)
    sleep(1)
    car.precise_rotate(-90)
    car.stop()

    GPIO.cleanup()
