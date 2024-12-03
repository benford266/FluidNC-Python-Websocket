# Description: This script is used to connect to the FluidNS ESP32 websocket server and read the coordinates of the CNC machine


from websocket import create_connection
import time
import re

# Connect to the websocket server FluidNC IP address
ws = create_connection("ws://192.168.4.87:81")

# Regular expression to match the coordinates of the CNC machine
pattern = re.compile(rb'<Idle\|MPos:\d+\.\d{3},\d+\.\d{3},\d+\.\d{3}\|FS:\d+,\d+\|Pn:P>\r\n')

# Function to clean up and write the coordinates of the CNC machine
def write_coordinates(result):
    parts = result.decode('utf-8').strip('<>\r\n').split('|')
    status = parts[0]
    mpos = parts[1].split(':')[1].split(',')
    fs = parts[2].split(':')[1].split(',')
    pn = parts[3].split(':')[1]
    print("Status: '%s'    ---   X: '%s'  Y: '%s' Z: '%s'" % (status, mpos[0], mpos[1], mpos[2]))

# Main loop to read the coordinates of the CNC machine
while True:
    ws.send("?")
    result = ws.recv()
    
    # Check to see if the result is a byte string and if it matches the pattern then write the coordinates
    if type(result) == bytes:
        if pattern.match(result):
            write_coordinates(result)

    # Sleep for 1 second
    time.sleep(1)