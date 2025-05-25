#!/usr/bin/env python
import time, sys, numpy as np, matplotlib.pyplot as plt, serial
from listen_to_lidar   import listen_to_lidar
import functions        as f
from grid              import Grid
from astar             import a_star
from calculate_time    import calculate_time
import movingParts      as mp
from functions_adapting import adapt_path

# ————— PARAMETERS —————
CLEARANCE_CELLS  = 2
CALIBRATION_CM   = 100.0
CALIBRATION_STEP = 350
CELL_SIZE_CM     = CALIBRATION_CM / CALIBRATION_STEP

PIVOT_RIGHT = 0.75
PIVOT_LEFT  = 0.75

SETTLE_FWD  = 0.0
POST_PAUSE  = 3.0

SERIAL_PORT = 'COM3'
BAUDRATE    = 115200
TIMEOUT     = 1

def inflate_grid(grid, r):
    R, C = len(grid), len(grid[0])
    out = [row[:] for row in grid]
    for y in range(R):
        for x in range(C):
            if grid[y][x] == 0:
                for dy in range(-r, r+1):
                    for dx in range(-r, r+1):
                        yy, xx = y+dy, x+dx
                        if 0 <= yy < R and 0 <= xx < C:
                            out[yy][xx] = 0
    return out

# 1. Acquire & stop LiDAR
data, stop = listen_to_lidar(); time.sleep(1); stop()

# 2. Build occupancy grid
pts = f.process_lidar_data(data['distances'])
if not pts:
    print("❌ No LiDAR data!"); sys.exit(1)
raw, cor  = f.create_grid(np.array(pts))
grid, cor = f.shrink_grid(raw, cor[1], cor[0])
grid      = inflate_grid(grid, CLEARANCE_CELLS)

# 3. Prepare A* graph
R, C  = len(grid), len(grid[0])
obs   = [(y, x) for y in range(R) for x in range(C) if grid[y][x] == 0]
src   = (cor[0], cor[1])
if src in obs: obs.remove(src)
g     = Grid(C, R, obstacles=obs)

# 4. Show map & robot start
print(f"Robot start coordinates: (X={src[1]}, Y={src[0]})")
vis = [row[:] for row in grid]
y0, x0 = src
if 0 <= y0 < R and 0 <= x0 < C:
    vis[y0][x0] = 0.75
plt.imshow(vis, cmap='magma', origin='upper'); plt.title('Padded Occupancy'); plt.show()
g.grid[y0][x0] = 1

# 5. Prompt for destination
while True:
    try:
        gx = int(input(f"X dest [0–{C-1}]: "))
        gy = int(input(f"Y dest [0–{R-1}]: "))
    except ValueError:
        print("⚠️ Integers only. Try again."); continue
    except (KeyboardInterrupt, EOFError):
        print("\n❌ Input cancelled."); sys.exit(1)
    if 0 <= gx < C and 0 <= gy < R and grid[gy][gx] == 1:
        dest = (gy, gx)
        break
    print("⚠️ Blocked or out of bounds; try again.")

# 6. Compute A*
try:
    raw_path = a_star(g, src, dest)
except Exception as e:
    print(f"❌ A* error: {e}"); sys.exit(1)

# 7. Visualize raw path
vis2 = [row[:] for row in grid]
for y, x in raw_path:
    if vis2[y][x] != 0:
        vis2[y][x] = 0.5
vis2[y0][x0] = 0.75
plt.imshow(vis2, cmap='magma', origin='upper'); plt.title('Raw A* Path'); plt.show()

# 8. Smooth & segment
waypoints, moves = adapt_path(raw_path, grid)
print("Segments (cells):", moves)

# 9. Convert to timed plan
timed = []
for d, steps in moves:
    if d == 'forward':
        t = float(calculate_time(steps * CELL_SIZE_CM))
    elif d == 'backward':
        t = float(calculate_time(steps * CELL_SIZE_CM))
    elif d == 'right':
        t = PIVOT_RIGHT
    else:  # 'left'
        t = PIVOT_LEFT
    timed.append((d, t))

# 10. Show & manual‐override
print("\n→ EXECUTION PLAN ←")
for d, t in timed:
    print(f"{d:>9} for {t:.2f}s")
try:
    confirm = input("Run? (y/N) or 'M' to manual: ").strip().lower()
except (KeyboardInterrupt, EOFError):
    print("\n❌ Cancelled."); sys.exit(1)

if confirm == 'm':
    print("Enter manual moves: direction time (e.g. forward 2.5). Blank to finish.")
    manual = []
    while True:
        try:
            line = input("Move> ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            print("\n❌ Manual entry cancelled."); manual = []; break
        if not line:
            break
        parts = line.split()
        if len(parts) != 2 or parts[0] not in ('forward','backward','left','right'):
            print("  ❌ Invalid. Try: forward 1.5"); continue
        try:
            manual.append((parts[0], float(parts[1])))
        except ValueError:
            print("  ❌ Time must be numeric.")
    if manual:
        timed = manual
        print("Using manual plan:")
        for d, t in timed:
            print(f"  {d:>9} for {t:.2f}s")
    # *** new confirmation after manual input ***
    try:
        again = input("\nExecute these manual moves? (y/N): ").strip().lower()
    except (KeyboardInterrupt, EOFError):
        print("\n❌ Cancelled."); sys.exit(1)
    if again != 'y':
        print("Cancelled."); sys.exit(0)

elif confirm != 'y':
    print("Cancelled."); sys.exit(0)

# 11. Execute with in-place spins
ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=TIMEOUT)
ser.write(b'start\n'); time.sleep(1)
for d, t in timed:
    if   d == 'forward':
        mp.f(ser)
    elif d == 'backward':
        mp.b(ser)
    elif d == 'right':
        mp.r(ser)     # in-place 90° right spin
    else:  # 'left'
        mp.l(ser)     # in-place 90° left spin

    time.sleep(t)
    mp.s(ser)

    # settle-forward after pivot
    if d in ('right','left'):
        mp.f(ser); time.sleep(SETTLE_FWD); mp.s(ser)

    time.sleep(POST_PAUSE)
ser.close()
