# Motion Fun Project
###### California State University, Northridge
###### Motion Fun Corporation ®

Welcome to Motion Fun, a senior design project for Comp 490. We have developed an incredibly cheap way to record/recreate orientation and motion data for just under $100. Visit us at www.motionfun490.com to create your Raspberry Pi Base Station and get started with our scripts today! 

#### Requirements 

- A Raspberry Pi connected to an Adafruit BNO055 Sensor.
- Python w/ Flask. 
- An SSH connection to your Raspberry Pi.
- A clone of this repository on your Raspberry Pi. 
- A webGL enabled browser. 
- Blender

#### Getting Started 

Check out our introduction video on our website for a full overview of our webGL recorder. Run the webGL.py script and press record data to begin recording orientation. Press stop when you have completed the motion you wish to recreate in Blender and a log file will be created with your orientation data. Now you can load this data into our Blender addon and track your previously recorded motion! Wow!!!!  

If you do not have a webGL enabled browser, you can use webData.py to view sensor information and calibrate your sensor, but you will not be able to record or view our 3D Environment. This file can be run directly on the Raspberry Pi. 

#### Blender Add-on


Within the directory, blender_files, contains the JSON parser which reconfigures the raw data given by the raspberry pi and feed the data into the blender model in autoload.py



