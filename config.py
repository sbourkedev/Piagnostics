#!/usr/bin/python
import ecu
import datetime
import numpy as np

# RPM values for use in the lookup table
vehicleRPMArray = np.array([750, 1000, 1250, 1500,
                            1750, 2000, 2250, 2500, 2750, 3000, 3250,
                            3500, 3750, 4000, 4250, 4500, 4750, 5000,
                            5250, 5500, 5750, 6000, 6250, 6500, 6750,
                            7000])

# Global Values
elapsedTime = 0
testTime = 0
logLength = 0
dtcIteration = 0
ecuFlag = False
dtcFlag = False
printCounter = 0
screenFlag = False
debugModeFlag = True
logIteration = 1
startTime = datetime .datetime.today().strftime('%Y%m%d%H%M%S')
RESOLUTION = (700, 500)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Lookup table with speeds for each gear
vehicleSpeedArray = np.array([[4, 7, 10, 14, 17],
                              [5, 9, 14, 18, 23],
                              [7, 11, 17, 23, 2],
                              [8, 14, 21, 28, 34],
                              [9, 16, 24, 32, 40],
                              [11, 18, 27, 37, 46],
                              [12, 21, 31, 41, 51],
                              [14, 23, 34, 46, 57],
                              [15, 25, 38, 50, 63],
                              [16, 27, 41, 55, 68],
                              [18, 30, 45, 60, 74],
                              [19, 32, 48, 64, 80],
                              [20, 34, 51, 69, 85],
                              [22, 37, 55, 73, 91],
                              [23, 39, 58, 78, 97],
                              [24, 41, 62, 83, 102],
                              [26, 43, 65, 87, 108],
                              [27, 46, 69, 92, 114],
                              [28, 48, 72, 96, 120],
                              [30, 50, 75, 101, 125],
                              [31, 53, 79, 106, 131],
                              [33, 55, 82, 110, 137],
                              [34, 57, 86, 115, 142],
                              [35, 59, 89, 119, 148],
                              [37, 62, 93, 124, 154],
                              [38, 64, 96, 129, 159]])
