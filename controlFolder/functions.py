import numpy as np
import math

def degrees_to_radians(degrees):
    return degrees * (math.pi / 180)

def process_lidar_data(lidar_data):
    data = lidar_data
    points=[]
    for angle_str, distance in data.items():
        angle = float(angle_str)
        angle = degrees_to_radians(angle)
        x = distance * math.cos(angle)
        y = distance * math.sin(angle)
        points.append([x, y])
    return points


def create_grid_map(points):
    # Find minimum and maximum x and y coordinates
    min_x = min(point[0] for point in points)
    min_y = min(point[1] for point in points)
    max_x = max(point[0] for point in points)
    max_y = max(point[1] for point in points)

    grid_width = int(max_x - min_x) + 1
    grid_height = int(max_y - min_y) + 1
    
    # Create grid
    grid = np.ones((grid_height, grid_width))
    
    for (x, y) in points:
        grid_x = int(x)
        grid_y = int(y)
        grid[grid_y, grid_x] = 0  # Mark the cell as occupied
    
    return grid.tolist()

def create_grid(points, path=None):
    # Find minimum and maximum x and y coordinates
    min_x = int(min(point[0] for point in points))
    min_y = int(min(point[1] for point in points))
    max_x = int(max(point[0] for point in points))
    max_y = int(max(point[1] for point in points))
    
    # Determine new grid dimensions after translation
    grid_width = max_x - min_x + 1
    grid_height = max_y - min_y + 1

    lidar_cor = (0 - min_y, 0 - min_x)
    
    # Create grid
    grid = np.ones((grid_height, grid_width))
    
    for (x, y) in points:
        # grid_x = int(x)
        # grid_y = int(y)
        grid_x = int(x - min_x)
        grid_y = int(y - min_y)
        grid[grid_y, grid_x] = 0  # Mark the cell as occupied
    
    return grid.tolist(), lidar_cor


def shrink_grid(grid, lidar_x, lidar_y):
    grid_height = len(grid)
    grid_width = len(grid[0])

    # Define the size of the smaller grid
    shrink_size = 500
    half_shrink = shrink_size // 2

    # Calculate boundaries for the smaller grid
    min_x = max(0, lidar_x - half_shrink)
    max_x = min(grid_width, lidar_x + half_shrink)

    min_y = max(0, lidar_y - half_shrink)
    max_y = min(grid_height, lidar_y + half_shrink)

    # Ensure the grid size remains 500x500
    if max_x - min_x < shrink_size:
        if min_x == 0:
            max_x = min_x + shrink_size
        elif max_x == grid_width:
            min_x = max_x - shrink_size

    if max_y - min_y < shrink_size:
        if min_y == 0:
            max_y = min_y + shrink_size
        elif max_y == grid_height:
            min_y = max_y - shrink_size

    new_lidar_x = lidar_x - min_x
    new_lidar_y = lidar_y - min_y

    # Extract the smaller grid by slicing each row individually
    small_grid = [row[min_x:max_x] for row in grid[min_y:max_y]]

    return small_grid, (new_lidar_y, new_lidar_x)

def adapt_path(path, x, y):
    first_y, first_x = path[0]

    forward = first_y - y
    right = x - first_x

    first_y_index = first_y
    first_x_index = first_x

    new_path = path

    for i in range(0, forward):
        new_path[i] = (first_y_index , first_x)
        first_y_index = first_y_index - 1

    for i in range(forward, forward + right):
        new_path[i] = (first_y_index, first_x_index)
        first_x_index = first_x_index + 1

    return new_path, forward, right

def end_points(points):

    far_x = max(p[1] for p in points)
    min_y = min(p[0] for p in points)

    return far_x, min_y


