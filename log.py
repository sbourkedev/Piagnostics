#!/usr/bin/python
import csv, os
from config import *


class logger():

    # Debug function to read from log file for GUI testing.
    def openLog(logFile):
        with open(logFile, 'r') as f:
            csvReader = csv.reader(f)
            logList = list(csvReader)
            return logList

    # Function to close the log and rename it to include end time.
    def closeLog():
        endTime = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        os.rename('logs/' + startTime + '.csv',
                  'logs/' + startTime + "_" + endTime + '.csv')

    # Function to append to the current log file.
    def updateLog(data):
        with open('logs/' + startTime + '.csv', 'a') as f:
            w = csv.writer(f)
            w.writerow(data)

    # Function to create a csv with the specified header.
    def createLog(header):
        # Write the header of the csv file.
        with open('logs/' + startTime + '.csv', 'w') as f:
            w = csv.writer(f)
            w.writerow(header)
 
    # Debug function that reads from log file and assigns to global values.
    def getLogValues(logFile):
        global logIteration
        global vehicleRPM
        global vehicleSpeed
        global vehicleCoolantTemp
        global vehicleIntakeTemp
        global vehicleMAF
        global vehicleThrottlePos
        global vehicleEngineLoad
        vehicleRPM = int(logFile[logIteration][1])
        vehicleSpeed = int(logFile[logIteration][2])
        vehicleCoolantTemp = logFile[logIteration][3]
        vehicleIntakeTemp = logFile[logIteration][4]
        vehicleMAF = logFile[logIteration][5]
        vehicleThrottlePos = logFile[logIteration][6]
        vehicleEngineLoad = logFile[logIteration][7]
