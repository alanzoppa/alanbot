import serial
import json


class Sensors():
    def __init__(self, port, speed=9600):
        self.ser = serial.Serial(port, speed)

    def update(self):
        line = json.loads(self.ser.readline())
        for key, val in line.items():
            setattr(self, key, val)
        print("Updated: " + json.dumps(line))

    def close(self):
        self.ser.close()
        




if __name__ == "__main__":

    sensors = Sensors('/dev/ttyACM0')

    for i in range(10):
        sensors.update()

    #ser = serial.Serial('/dev/ttyACM0', 9600)
    #for i in range(10):
        #try:
            #line = json.loads(ser.readline())
            #print(line)
        #except:
            #pass


    sensors.close()
