# Motion Fun Project
#
# www.github.com/MotionFunProject/MotionFunProject
# www.motionfun490.com
#
# Run this code using terminal command 'sudo python webGL.py'

import threading
import time
import json
import logging

from flask import *
from Adafruit_BNO055 import BNO055

# Raspberry Pi configuration with serial UART and RST connected to GPIO 18:
bno = BNO055.BNO055(serial_port='/dev/ttyAMA0', rst=18)

write = open("datalog2.txt", "w")

# BNO sensor axes remap values:  DO NOT CHANGE THESE VALUES!! 
BNO_AXIS_REMAP = { 'x': BNO055.AXIS_REMAP_X,
                   'y': BNO055.AXIS_REMAP_Z,
                   'z': BNO055.AXIS_REMAP_Y,
                   'x_sign': BNO055.AXIS_REMAP_POSITIVE,
                   'y_sign': BNO055.AXIS_REMAP_POSITIVE,
                   'z_sign': BNO055.AXIS_REMAP_NEGATIVE }


app = Flask(__name__)

sensor_data = {}
thread_changed = threading.Condition() 
thread = None

# Function to read the sensor and update the sensor_data dictionary with the
# latest data. Must run in its own thread because it will never return.
def read_data():
    while True:
        temp = bno.read_temp()
        heading, roll, pitch = bno.read_euler()
        magx, magy, magz = bno.read_magnetometer()
        gyrox, gyroy, gyroz = bno.read_gyroscope()
        accx, accy, accz = bno.read_accelerometer()
        quatx, quaty, quatz, quatw = bno.read_quaternion()
        linx, liny, linz = bno.read_linear_acceleration()
        gravx, gravy, gravz = bno.read_gravity()
        syscal, gyrocal, accelcal, magcal = bno.get_calibration_status()
        status, self_test, error = bno.get_system_status(run_self_test=False)
        if error != 0:
            print 'Error! Value: {0}'.format(error)

        with thread_changed:
            sensor_data['temp'] = (temp)
            sensor_data['euler'] = (heading, roll, pitch)
            sensor_data['mag'] = (magx, magy, magz)
            sensor_data['gyro'] = (gyrox, gyroy, gyroz)
            sensor_data['accel'] = (accx, accy, accz)
            sensor_data['quaternion'] = (quatx, quaty, quatz, quatw)
            sensor_data['linaccel'] = (linx, liny, linz)
            sensor_data['gravity'] = (gravx, gravy, gravz)
            sensor_data['calibration'] = (syscal, gyrocal, accelcal, magcal)

            # Notify any waiting threads that the BNO state has been updated.
            thread_changed.notifyAll()
        # Sleep until the next reading.
        time.sleep(.1)


#Function to handle sending sensor data to the client web browser
#using HTML5 server sent events.
def sse():
    while True:
        with thread_changed:
            thread_changed.wait()
            temp = sensor_data['temp']
            heading, roll, pitch = sensor_data['euler']
            magx, magy, magz = sensor_data['mag']
            gyrox, gyroy, gyroz = sensor_data['gyro']
            accx, accy, accz = sensor_data['accel']
            quatx, quaty, quatz, quatw = sensor_data['quaternion']
            linx, liny, linz = sensor_data['linaccel']
            gravx, gravy, gravz = sensor_data['gravity']
            syscal, gyrocal, accelcal, magcal = sensor_data['calibration']
            
        # Send the data to the connected client in HTML5 server sent event format.
        data = {'heading': heading, 'roll': roll, 'pitch': pitch,
                'quatx': quatx, 'quaty': quaty, 'quatz': quatz, 'quatw': quatw}
        toSend = 'data: {0}\n\n'.format(json.dumps(data))
        write.write(toSend)
        yield toSend


@app.before_first_request
def start_thread():
    global thread
    if not bno.begin():
        raise RuntimeError('The sensor is not detected. Make sure the sensor is connected to your Pi')
    bno.set_axis_remap(**BNO_AXIS_REMAP)
    # Start reading data in a thread
    thread = threading.Thread(target=read_data)
    thread.daemon = True 
    thread.start()

@app.route('/bno') #We route this to the Event Source we created in our html file. 
def path():
    return Response(sse(), mimetype='text/event-stream')


@app.route('/')
def root():
    return render_template('webGL.html')


# Keep threading enabled 
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
