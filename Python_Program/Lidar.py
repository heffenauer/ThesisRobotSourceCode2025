import time
from listen_to_lidar import listen_to_lidar
import functions as f
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from grid import Grid
from astar import a_star
from calculate_time import calculate_time
import serial
import movingParts as mp

lidar_data, stop = listen_to_lidar()
time.sleep(1)

stop()

cartesian_dots =  np.array(f.process_lidar_data(lidar_data['distances']))

grid, cor = f.create_grid(cartesian_dots)

grid, cor = f.shrink_grid(grid, cor[1], cor[0])

rows = len(grid)
cols = len(grid[0])

obsticles = []

for i in range(0,rows):
    for j in range(0,cols):
        if grid[i][j] == 0:
            obsticles.append((i,j))

g = Grid(cols,rows, obstacles=obsticles)

src = (cor[0],cor[1])

g.grid[cor[0]][cor[1]] = 0.75

small_grid = f.shrink_grid(g.grid,cor[1],cor[0])

print(f'Coordinates of robot are ({cor[1]},{cor[0]})')

# Print the created grid
plt.imshow(g.grid, cmap='magma', origin='lower')
plt.gca().invert_yaxis()
plt.colorbar(label='Occupancy')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Grid Map with Different Colors for 0 and 1')
plt.grid(True, which='both',  linestyle='', linewidth=0.5)
plt.show()


valid_dest = False

g.grid[cor[0]][cor[1]]= 1

while valid_dest==False:
    destX = int(input('Enter x value of destination: '))
    destY = int(input('Enter y value of destination: '))
    if(g.grid[destY][destX] == 0 or destX > cols or destX < 0 or destY > rows or destY < 0):
        print("Destination is blocked!")
    else:
        valid_dest = True

path = a_star(g, src, (destY,destX))

for node in path:
    if(g.grid[node[0]][node[1]]!=0):
        g.grid[node[0]][node[1]] = 0.5

g.grid[cor[0]][cor[1]]= 0.75

plt.imshow(g.grid, cmap='magma', origin='lower')
plt.gca().invert_yaxis()
plt.colorbar(label='Occupancy')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Grid Map with Different Colors for 0 and 1')
plt.grid(True, which='both',  linestyle='', linewidth=0.5)
plt.show()

for node in path: # clearing firs path
    if(g.grid[node[0]][node[1]]!=0):
        g.grid[node[0]][node[1]] = 1


far_x, close_y = f.end_points(path)

new_path, forward_distance, right_distance = f.adapt_path(path,far_x,close_y)

for node in new_path: # drawing adapted path
    if(g.grid[node[0]][node[1]]!=0):
        g.grid[node[0]][node[1]] = 0.5

print("Now adpated path")

plt.imshow(g.grid, cmap='magma', origin='lower')
plt.gca().invert_yaxis()
plt.colorbar(label='Occupancy')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Grid Map with Different Colors for 0 and 1')
plt.grid(True, which='both',  linestyle='', linewidth=0.5)
plt.show()


forward_time = float( calculate_time(forward_distance))
right_time = float(calculate_time(right_distance))

print(f"Time for forward is {forward_time}  and for right is {right_time}")


serialInst = serial.Serial()
serialInst.baudrate = 115200
serialInst.port = 'COM7'
serialInst.open()

serialInst.write(('start').encode('utf-8'))  # Encode the move as bytes
time.sleep(1)

mp.f(serialInst)
time.sleep(forward_time)

mp.s(serialInst)
time.sleep(2)

mp.fl(serialInst)
time.sleep(2.67)

mp.s(serialInst)
time.sleep(2)


mp.f(serialInst)
time.sleep(right_time)


mp.s(serialInst)

# Close the serial connection
serialInst.close()


df = pd.DataFrame(path, columns=['Y', 'X'])

# Specify the filename
filename = 'raw_path_better.csv'

# Write DataFrame to CSV
#df.to_csv(filename, index=False)