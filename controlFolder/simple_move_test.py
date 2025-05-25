#!/usr/bin/env python3
import time
import serial
import movingParts as mp

# ————— CONFIG —————
SERIAL_PORT = 'COM3'
BAUDRATE    = 115200
TIMEOUT     = 1

# Sequence: (command, duration_in_seconds)
MOVES = [
    ('forward', 1.0),
    ('left',    0.7),
    ('forward', 1.0),
    ('right',   0.7),
    ('forward', 2.5),
    ('right',   0.7),
    ('forward', 1.5),
]

INTER_MOVE_PAUSE = 2.0  # seconds between segments

def run_moves(moves):
    # open serial
    ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=TIMEOUT)
    time.sleep(2)               # let the port settle
    ser.write(b'start\n')       # optional handshake
    time.sleep(1)

    for direction, duration in moves:
        # pick the correct movingParts function
        if direction == 'forward':
            cmd_fn = mp.f
        elif direction == 'backward':
            cmd_fn = mp.b
        elif direction == 'right':
            cmd_fn = mp.r
        elif direction == 'left':
            cmd_fn = mp.l
        else:
            print(f"⚠️ Unknown direction: {direction}")
            continue

        print(f"→ {direction:>8} for {duration:.2f}s")
        cmd_fn(ser)            # start motion
        time.sleep(duration)   # wait
        mp.s(ser)              # stop after this segment
        time.sleep(INTER_MOVE_PAUSE)

    # ensure robot is fully stopped before closing
    mp.s(ser)
    ser.close()
    print("Done.")

if __name__ == "__main__":
    run_moves(MOVES)
