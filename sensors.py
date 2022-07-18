import serial
import json
import pdb


class Sensors():
    def __init__(self, port, speed=9600):
        self.ser = serial.Serial(port, speed)
        for i in range(10):
            self.ser.readline()
            #print(self.ser.readline())

    def update(self):
        self.ser.flushInput()
        self.rawline = self.ser.readline()
        #print(self.rawline)
        try:
            self.line = json.loads(self.rawline)
            for key, val in self.line.items():
                #print(key,val)
                setattr(self, key, val)
        except json.decoder.JSONDecodeError:
            print(self.rawline)

    def close(self):
        self.ser.close()

    def print(self):
        print(self.line)
        #print(f"distance: {self.distance}, yaw: {self.yaw}")
        



if __name__ == "__main__":

    sensors = Sensors('/dev/ttyACM0')

    while True:
        sensors.update()
        sensors.print()

    sensors.close()
