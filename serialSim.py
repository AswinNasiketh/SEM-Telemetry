import queue
import random
import threading
import time

CELL_MAX_VOLTAGE = 4.2 #Volts
CELL_MIN_VOLATGE = 3.0
NUM_CELLS = 26
NUM_TEMP_PROBES = 3

BATT_TMP_MAX = 60
BATT_TMP_MIN = 10

MAX_RPM = 2000

MAX_SPEED = 20

serialBuf = queue.Queue()

def generateSerialData():  
    while True:
        #Battery Cell Voltages

        for i in range(NUM_CELLS):
            randomNum = random.random()
            v = (randomNum * (CELL_MAX_VOLTAGE - CELL_MIN_VOLATGE)) + CELL_MIN_VOLATGE

            serialStr = "Cell " + str(i) + " Voltage: " + str(v)
            serialBuf.put(serialStr)

        #motor rpm

        randomNum = random.random()

        rpm = int(randomNum * MAX_RPM)

        serialStr = "RPM: " + str(rpm)
        serialBuf.put(serialStr)
        #motor speed

        randomNum = random.random()

        speed = int(randomNum * MAX_SPEED)

        serialStr = "Speed: " + str(speed)
        serialBuf.put(serialStr)

        #battery temperatures

        for i in range(NUM_TEMP_PROBES):
            randomNum = random.random()
            t = (randomNum * (BATT_TMP_MAX - BATT_TMP_MIN)) + BATT_TMP_MIN
            serialStr = "Temperature " + str(i) + " : " + str(t)
            serialBuf.put(serialStr)
        #State of Charge

        randomNum = random.random()

        soc = int(randomNum * 100)

        serialStr = "SOC: " + str(soc)
        serialBuf.put(serialStr)

        time.sleep(1)

def generateRandomRPM():
    randomNum = random.random()
    return int(randomNum * MAX_RPM)

def generateRandomCellVoltage():
    randomNum = random.random()
    return (randomNum * (CELL_MAX_VOLTAGE - CELL_MIN_VOLATGE)) + CELL_MIN_VOLATGE


def generateRandomTemperature():
    randomNum = random.random()
    return (randomNum * (BATT_TMP_MAX - BATT_TMP_MIN)) + BATT_TMP_MIN

def generateRandomCellVoltages():
    return [generateRandomCellVoltage() for i in range(13)]

def generateRandomTemps():
    return [generateRandomTemperature() for i in range(8)]






def startDataGen():
    t = threading.Thread(target=generateSerialData, daemon=True)
    t.start()

# for dashboard team





