import serial
import time
import movingParts as mp

# Initialize the serial connection
serialInst = serial.Serial()
serialInst.baudrate = 115200
serialInst.port = 'COM3'  # Make sure this is the correct port for Arduino
serialInst.open()

# Optional: start handshake
serialInst.write('start'.encode('utf-8'))
time.sleep(1)

# Move forward briefly
mp.f(serialInst)
time.sleep(1.5)  # Adjust duration as needed

# Stop movement
mp.s(serialInst)

# Close the serial connection
serialInst.close()
