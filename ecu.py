#!/usr/bin/python
import config
from threading import Thread
import obd
import numpy as np

# Global Values
vehicleThrottlePos = 0
vehicleTimingAdvance = 0
vehicleSpeed = 0
vehicleCoolantTemp = 0
vehicleIntakeTemp = 0
vehicleMAF = 0
vehicleRPM = 0
vehicleEngineLoad = 0
currentGear = 0
ecuConnection = None
dtc = ['P0430 - Catalytic Converter  Pollutant Spike']


def find_nearest(array, value):
    indexValue = (np.abs(array - value)).argmin()
    return indexValue


# Initialize connection to the ECU using Thread
class ecuThread(Thread):
    def __init__(self):
        # Initialize the thread
        Thread.__init__(self)
        self.daemon = True
        self.start()

    # Setters for ECU values
    def setVehicleTimingAdvance(self, r):
        vehicleTimingAdvance = int(round(r.value.magnitude))

    def setVehicleRPM(self, r):
        vehicleRPM = int(r.value.magnitude)

    def setVehicleMAF(self, r):
        vehicleMAF = r.value.magnitude

    def setVehicleSpeed(self, r):
        vehicleSpeed = r.value.to("mph")
        vehicleSpeed = int(round(vehicleSpeed.magnitude))

    def setVehicleIntakeTemp(self, r):
        vehicleIntakeTemp = r.value.magnitude

    def setVehicleEngineLoad(self, r):
        vehicleEngineLoad = int(round(r.value.magnitude))

    def setVehicleThrottlePos(self, r):
        vehicleThrottlePos = int(round(r.value.magnitude))

    def setVehicleCoolantTemp(self, r):
        vehicleCoolantTemp = r.value.magnitude

    def new_dtc(self, r):
        dtc = r.value

    def run(self):
        ports = obd.scan_serial()
        print(ports)

        # Enable ECU debugging to show more information from ECU
        obd.logger.setLevel(obd.logging.DEBUG)

        # Connects to the ECU
        ecuConnection = obd.Async("dev/rfcomm1")

        # ECU watchers to detect new values for the setters
        ecuConnection.watch(obd.commands.ENGINE_LOAD,
                            callback=self.getVehicleEngineLoad)

        ecuConnection.watch(obd.commands.THROTTLE_POS,
                            callback=self.getVehicleThrottlePos)

        ecuConnection.watch(obd.commands.MAF, callback=self.getVehicleMAF)

        ecuConnection.watch(obd.commands.SPEED, callback=self.getVehicleSpeed)

        ecuConnection.watch(obd.commands.COOLANT_TEMP,
                            callback=self.getVehicleCoolantTemp)

        ecuConnection.watch(obd.commands.GET_DTC, callback=self.new_dtc)

        ecuConnection.watch(obd.commands.RPM, callback=self.getVehicleRPM)

        ecuConnection.watch(obd.commands.INTAKE_TEMP,
                            callback=self.getVehicleIntakeTemp)

        # Starts the connection to the ECU
        ecuConnection.start()
        # Set ECU Flag to True
        config.ecuFlag = True


# Function to calculate current gear using RPM and Speed
def calculateCurrentGear(vehicleRPM, vehicleSpeed):
    if vehicleSpeed == 0:
        currentGear = 'N'

    elif (vehicleRPM < 875) & (vehicleSpeed > 0):
        currentGear = 'N'

    else:
        closestSpeedIndx = find_nearest(config.vehicleRPMArray, vehicleRPM)
        currentGear = str(closestSpeedIndx + 1)
