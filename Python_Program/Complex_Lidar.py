import time
from listen_to_lidar import listen_to_lidar
import functions as f
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from grid import Grid
from astar import a_star
import functions_adapting as fa


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

for node in path:
    if(g.grid[node[0]][node[1]]!=0):
        g.grid[node[0]][node[1]] = 1

x, y, l, d = fa.end_points(path)

new_path = fa.complex_path(path, y,l ,d)

for node in new_path:
    if(g.grid[node[0]][node[1]]!=0):
        g.grid[node[0]][node[1]] = 0

plt.imshow(g.grid , cmap='magma', origin='lower')
plt.gca().invert_yaxis()
plt.colorbar(label='Occupancy')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Grid Map with Different Colors for 0 and 1')
plt.show()


df = pd.DataFrame(path, columns=['Y', 'X'])

filename = 'complex_path_better.csv'

# Write DataFrame to CSV
# df.to_csv(filename, index=False)