import RPi.GPIO as GPIO          
from time import sleep


from car import Car, Motor, Speed
from sensors import Sensors


if __name__ == "__main__":

    GPIO.setmode(GPIO.BCM)


    car = Car(rf=(23,24,12), rr=(27,22,16), lf=(5,6,20), lr=(19,26,21), sensors=Sensors('/dev/ttyACM0'))

    car.set_speed(40)


    approach = car.approach()
    print("Approach: " + str(approach["elapsed"]) + "s")

    #car.forward()
    #sleep(1)

    #car.reverse()

    #sleep(approach["elapsed"])

    car.precise_timed_reverse(approach["elapsed"])



    for i in range(4):
        car.precise_rotate(45)
        sleep(.25)

    car.precise_rotate(-90)
    sleep(.25)
    car.precise_rotate(-90)
        #car.stop()

    GPIO.cleanup()
