import RPi.GPIO as GPIO          
from time import sleep


from car import Car, Motor, Speed
from sensors import Sensors


if __name__ == "__main__":

    GPIO.setmode(GPIO.BCM)


    car = Car(rf=(23,24,12), rr=(27,22,16), lf=(5,6,20), lr=(19,26,21), sensors=Sensors('/dev/ttyACM0'))

    car.set_speed(50)


    approach = car.approach()
    print("Approach: " + str(approach["elapsed"]) + "s")
    car.precise_timed_reverse(approach["elapsed"])

    #car.forward()
    #sleep(2)

    #car.reverse()
    #sleep(2)

    #sleep(approach["elapsed"])




    prev_error = 0
    for i in range(4):
        rotation = car.precise_rotate(45-prev_error)
        prev_error = rotation['error']
        sleep(.25)

    for i in range(2):
        rotation = car.precise_rotate(-90-prev_error)
        prev_error = rotation['error']
        sleep(.25)

    GPIO.cleanup()
