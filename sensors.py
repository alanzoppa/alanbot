import serial
import json
import pdb
from time import sleep


class Sensors():
    def __init__(self, port, speed=9600):
        self.ser = serial.Serial(port, speed)
        for i in range(10):
            self.ser.readline()

    def update(self):
        try:
            self.ser.flushInput()
            line = json.loads(self.ser.readline())
            for key, val in line.items():
                setattr(self, key, val)
        except json.decoder.JSONDecodeError:
            pass

    def goof(self):
        pdb.set_trace()

    def close(self):
        self.ser.close()

    def print(self):
        print(f"distance: {self.distance}, yaw: {self.yaw}")
        




if __name__ == "__main__":

    sensors = Sensors('/dev/ttyACM0')

    for i in range(10):
        sensors.update()
        sensors.print()
    sensors.goof()

    #ser = serial.Serial('/dev/ttyACM0', 9600)
    #for i in range(10):
        #try:
            #line = json.loads(ser.readline())
            #print(line)
        #except:
            #pass


    sensors.close()
