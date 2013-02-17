# This script performs a scan, converts the scan to JPG and uploads it to DropBox
# it uses:
#   - GPIO pin 8:   Button to start a scan
#   - GPIO pin 10:  Output LED 1. System Ready led.   .... Now it's used for Scanning but once board is finished it should be ready LED again
#   - GPIO pin 11:  Output LED 2. Scanning led.   .... Now it's used for Conversion but once board is finished it should be Scanning LED again
#   - GPIO pin 12:  Output LED 3. Conversion Ready led.   .... once board is finished...
#   - GPIO pin 13:  Output LED 4. Uploading led.   .... once board is finished...
#   - GPIO pin 15:  Output LED 5. Completed led.   .... once board is finishedconnect...
#   - GPIO pin 16:  Output LED 6. ERROR led..... once board is finishedconnect...
#
# When button is pushed a timestamp based filename is generated.

# Import the required modules. 
import RPi.GPIO as GPIO
from time import sleep
import os
import time
import datetime

# Set the mode of numbering the pins. 
GPIO.setmode(GPIO.BOARD)

# Disable Already In Use warnings
GPIO.setwarnings(False)

# GPIO pin 8 as input. 
GPIO.setup(8, GPIO.IN) 

# GPIO pin 10, 11, 12 as output
GPIO.setup(10, GPIO.OUT) # System ready
GPIO.setup(11, GPIO.OUT) # Scanning
GPIO.setup(12, GPIO.OUT) # Converting
GPIO.setup(13, GPIO.OUT) # Uploading
GPIO.setup(15, GPIO.OUT) # Finished
GPIO.setup(16, GPIO.OUT) # Error (red led)

# Set 10 to True (LED off)
GPIO.output(10,False)
GPIO.output(11,True)
GPIO.output(12,True)
GPIO.output(13,True)
GPIO.output(15,True)
GPIO.output(16,True)

# Loop and wait for button press
while 1: 
    if GPIO.input(8):
        GPIO.output(10,True)
        ts = time.time()
        file_name = "scan_" + datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%y_%H-%M-%S')
        print file_name
        GPIO.output(11,False)
        os.system("scanimage --format=tiff --mode=Color --resolution=300 -p > " + file_name + ".tiff")
        GPIO.output(11,True)
        GPIO.output(12,False)
        os.system("convert " + file_name + ".tiff "+ file_name + ".jpg")
        GPIO.output(12,True)
        GPIO.output(13,False)
        os.system("./dropbox_uploader.sh upload " + file_name + ".jpg")
        GPIO.output(13,True)
        
        #clean up
        os.system("rm " + file_name + ".tiff");
        os.system("mv " + file_name + ".jpg finished_scans/");
        
        for x in range(0, 3):       # Flash 3 times for succes
            GPIO.output(15,False)
            sleep(0.3)
            GPIO.output(15,True)
            sleep(0.3)
            
        GPIO.output(10,False) # System ready led back on again