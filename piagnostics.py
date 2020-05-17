#!/usr/bin/python
import config, ecu, log, time, datetime, sys
import pygame, os
from art import *
from pygame.locals import *

print("\n\n---------------------------------------------------------------")
Art = text2art("Piagnostics")
print(Art)
print("------------------------  SHANE BOURKE  -----------------------\n\n")

# Clock object. Used for storing values to log
# every X seconds
clock = pygame.time.Clock()


# Helper function to draw the given string at coordinates, relative to center.
def displayTextInitializer(string, x, y, font):
    if font == "ecuValue":
        displayText = ecuValueFont.render(string, True, config.WHITE)
    elif font == "ecuVariable":
        displayText = ecuVariableFont.render(string, True, config.WHITE)

    displayTextRect = displayText.get_rect()
    displayTextRect.centerx = windowSurface.get_rect().centerx + x
    displayTextRect.centery = windowSurface.get_rect().centery + y
    windowSurface.blit(displayText, displayTextRect)


# If not in debug mode, open ECU thread and attempt connection
if not config.debugModeFlag:
    ecu.ecuThread()

    while not config.ecuFlag:
        time.sleep(.10)

# Load the background image for the GUI
backgroundImage = pygame.image.load("resources/ground.png")

# Load the window for the GUI
# If the screenFlag is set, load the window for external Pi display
# Else, set up the screen for the GUI window
if config.screenFlag:
    # Set the environment path for the external display
    os.putenv('SDL_ENV', 'dev/fb0')
    pygame.init()
    # Hide the mouse if using touchscreen display
    pygame.mouse.set_visible(0)
    windowSurface = pygame.display.set_mode(config.RESOLUTION)
else:
    pygame.init()
    windowSurface = pygame.display.set_mode(config.RESOLUTION, 0, 32)

# Load the OBD logo for the GUI
img = pygame.image.load("resources/obd.png")
img_button = img.get_rect(topleft=(135, 220))

# Assigning the fonts from the fonts folder
ecuValueFont = pygame.font.Font("fonts/Roboto-Light.ttf", 40)
ecuVariableFont = pygame.font.Font("fonts/Roboto-Light.ttf", 30)

# Setting the coordinates for the background image
backgroundCoordinates = (windowSurface.get_rect().centerx - 350,
                         windowSurface.get_rect().centery - 250)

# Call to createLog method using headings given
log.logger.createLog(["TIME", "RPM", "SPEED", "COOLANT_TEMP", "INTAKE_TEMP",
                      "MAF", "THROTTLE_POS", "ENGINE_LOAD"])

# If debug mode enabled, read logs from the debug log file
# instead of ECU
if config.debugModeFlag:
    # Read the debug log file
    list = log.logger.openLog('logs/debug_log.csv')
    # Get the length of the debug log file
    logLength = len(list)
    log.logger.getLogValues(list)

# If not in debug mode but no ECU connection established
# Print error and exit gracefully
elif not ecu.ecuConnection:
    print("\nNo ECU Connection Found")
    print("Check ECU or enable Debug Mode\n")
    sys.exit()

# Set the Window Caption
pygame.display.set_caption('Piagnostics - Shane Bourke')

# Display the GUI until exited
while True:
    for event in pygame.event.get():

        # When GUI is exited, do this:
        if event.type == QUIT:
            # Rename the log file to include the end time
            # and close the log file
            log.logger.closeLog()

            if ecu.ecuConnection:
                # Close ECU connection if one is open
                if ecu.ecuConnection:
                    ecu.ecuConnection.close()

                # Exit program from ECU mode
                pygame.quit()
                print("-----Exiting ECU Mode-----")
                sys.exit()

            # Exit program from ECU mode
            pygame.quit()
            print("-----Exiting Debug Mode-----")
            sys.exit()

        # If the screen is clicked do this:
        if event.type == MOUSEBUTTONDOWN:
            # Toggle the dtc flag
            config.dtcFlag = not config.dtcFlag

    if not config.debugModeFlag:
        # Method call to calculate current gear using
        # vehicle speed and rpm
        ecu.calculateCurrentGear(int(float(ecu.vehicleRPM)),
                                 int(ecu.vehicleSpeed))

    # If in debug mode, set current mode to 'log'
    if config.debugModeFlag:
        mode = log

    # If in ECU mode, set mode to 'ecu'
    else:
        mode = ecu

    # Clears the GUI
    windowSurface.fill(config.BLACK)

    # Initialize the window width and height
    WINDOWWIDTH = 700
    WINDOWHEIGHT = 500

    # Load the OBD logo
    windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)

    # If the screen has been clicked & vehicle speed is zero, do this:
    if (config.dtcFlag and ecu.vehicleSpeed == 0):
        displayTextInitializer("Diagnostic Trouble Codes", 0, -100, "ecuValue")
        # If there is a DTC:
        if ecu.dtc:
            # Display all DTCs
            for code in ecu.dtc:
                displayTextInitializer(code, 0, -80 + 50,
                                       "ecuVariable")

        # If there isn't a DTC(s)
        else:
            displayTextInitializer("No DTCs found", 0, -20, "ecuVariable")

    # If the screen hasn't been clicked:
    elif config.debugModeFlag:

        # Load the OBD image
        windowSurface.blit(backgroundImage, backgroundCoordinates)

        # Draw the currentGear ecuValue and ecuVariable.
        if ecu.ecuConnection:
            displayTextInitializer(str(ecu.currentGear), -190, -25, "ecuValue")
        else:
            displayTextInitializer("2nd", -190, -25, "ecuValue")
        displayTextInitializer("Gear", -190, 25, "ecuVariable")

        # Draw the MAF ecuValue and ecuVariable.
        displayTextInitializer(str(mode.vehicleMAF) + " g/s", -175,
                               -150, "ecuValue")
        displayTextInitializer("MAF", -190, -110, "ecuVariable")

        # Draw the RPM ecuValue and ecuVariable.
        displayTextInitializer(str(mode.vehicleRPM), 0, -25, "ecuValue")
        displayTextInitializer("RPM", 0, 25, "ecuVariable")

        # Draw the throttle position ecuValue and ecuVariable.
        displayTextInitializer(str(mode.vehicleThrottlePos) + " %", 190,
                               -145, "ecuValue")
        displayTextInitializer("Throttle", 190, -110, "ecuVariable")

        # Draw the intake temp ecuValue and ecuVariable.
        displayTextInitializer(str(mode.vehicleIntakeTemp) + "\xb0C", 190,
                               105, "ecuValue")
        displayTextInitializer("Intake", 190, 140, "ecuVariable")

        # Draw the engine load ecuValue and ecuVariable.
        displayTextInitializer(str(mode.vehicleEngineLoad) + " %", 0,
                               -145, "ecuValue")
        displayTextInitializer("Load", 0, -110, "ecuVariable")

        # Draw the coolant temp ecuValue and ecuVariable.
        displayTextInitializer(str(mode.vehicleCoolantTemp) + "\xb0C",
                               -190, 105, "ecuValue")
        displayTextInitializer("Coolant", -190, 140, "ecuVariable")

        # Draw the vehicleSpeed ecuValue and ecuVariable.
        displayTextInitializer(str(mode.vehicleSpeed) + " mph", 170,
                               -25, "ecuValue")
        displayTextInitializer("Speed", 180, 25, "ecuVariable")

        # Load the image
        windowSurface.blit(img, (windowSurface.get_rect().centerx - 25,
                                 windowSurface.get_rect().centery + 100))

        # If debug flag is set, feed fake data so I can test the GUI.
        if config.debugModeFlag:
            # Debug gui display refresh 10 times a second.
            if config.testTime > 500:
                log.logger.getLogValues(list)
                ecu.calculateCurrentGear(ecu.vehicleRPM, ecu.vehicleSpeed)
                config.testTime = 0

    # Update the clock object
    clockTick = clock.tick()
    config.elapsedTime += clockTick
    config.testTime += clockTick

    # If X milliseconds have elapsed, do this:
    if config.elapsedTime > 2500:
        # Log all of our data.
        data = [datetime.datetime.today().strftime('%Y%m%d%H%M%S'),
                mode.vehicleRPM, mode.vehicleSpeed, mode.vehicleCoolantTemp,
                mode.vehicleIntakeTemp, mode.vehicleMAF,
                mode.vehicleThrottlePos, mode.vehicleEngineLoad]

        log.logger.updateLog(data)

        # Rest time elapsed
        config.elapsedTime = 0

    # Update the GUI
    pygame.display.update()
