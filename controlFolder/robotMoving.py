import serial
import pandas as pd
import time  # Import the time module
import movingParts as mp

# Initialize the serial connection
serialInst = serial.Serial()
serialInst.baudrate = 115200
serialInst.port = 'COM3'
serialInst.open()


serialInst.write(('start').encode('utf-8'))  # Encode the move as bytes
time.sleep(1)

mp.f(serialInst)
time.sleep(1.75) # prvo kratanje pravo, mijenja

mp.s(serialInst) # stop ne diraj
time.sleep(2)

mp.fl(serialInst) # okretanje ne diraj
time.sleep(2.65)

mp.s(serialInst)# stop ne diraj
time.sleep(2)


mp.f(serialInst)
time.sleep(2.5) # drugo kratanje pravo, mijenja



# mp.f(serialInst)
# time.sleep(5)

# +

# serialInst.write(('r1').encode('utf-8'))  # Encode the move as bytes
# time.sleep(5)

mp.s(serialInst)

# Close the serial connection
serialInst.close()
