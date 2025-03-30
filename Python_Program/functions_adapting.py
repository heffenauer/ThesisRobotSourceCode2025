import numpy as np

def find_move(path, i):
    prev_y,prev_x, = path[i - 1]
    curr_y,curr_x, = path[i]
    move = ""
    
    if curr_y == prev_y + 1 and curr_x == prev_x:
        move="backward"
    elif curr_y == prev_y - 1 and curr_x == prev_x:
        move="forward"
    elif curr_y == prev_y and curr_x == prev_x + 1:
        move="right"
    elif curr_y == prev_y and curr_x == prev_x - 1:
        move="left"
    
    return move

def end_points(points):
    first_move = find_move(points,1)
    first_up = 0

    for i in range(2,len(points)):
        current_move = find_move(points,i)
        if(current_move != first_move):
            first_up = i - 1
            break
        
    far_left = min(p[1] for p in points)

    biggest_up = min(p[0] for p in points)

    return first_move, first_up, far_left, biggest_up

def complex_path(path, first_up, far_left, biggest_up):
    new_path = path

    left_range = path[first_up][1] - far_left
    left_movig = path[first_up][1]

    last_index = 0 

    for i in range(first_up + 1, first_up + left_range + 1):
        new_path[i] = (path[first_up][0], left_movig)
        left_movig = left_movig - 1
        last_index = i

    second_up_range = path[last_index][0] - biggest_up 
    second_up_index = path[last_index][0]
    up_index= last_index

    for i in range(last_index + 1, last_index + second_up_range + 1):
        new_path[i] = (second_up_index, path[up_index][1])
        second_up_index = second_up_index - 1
        last_index = i

    right_index = path[last_index][1] 

    for i in range(last_index + 1, len(path)):
        new_path[i] = (path[last_index][0], right_index)
        right_index = right_index + 1

    return new_path

def complex_path_2(path, first_up, far_left, biggest_up):

    new_path = path[0:first_up + 1]

    far_right = max(p[1] for p in path)

    left_range = path[first_up][1] - far_left

    left_movig = path[first_up][1]

    constant_y = new_path[len(new_path) - 1][0]

    while(left_range != 0):
        new_path = np.append(new_path,(constant_y, left_movig))
        left_movig = left_movig - 1
        left_range = left_range -1
       

    second_up_range = new_path[len(new_path) - 1][0] - biggest_up 

    second_up_moving = new_path[len(new_path) - 1][0]

    constant_x = new_path[len(new_path) - 1][1]

    while(second_up_range != 0):
        new_path = np.append(new_path,(second_up_moving, constant_x))
        second_up_moving = second_up_moving - 1
        second_up_range = second_up_range - 1

    constant_y = new_path[len(new_path) - 1][0]

    right_moving = new_path[len(new_path) - 1][1] 

    right_range = far_right - right_moving

    while(right_range != 0):
        new_path =  np.append(new_path,(constant_y,right_moving))
        right_moving = right_moving + 1
        right_range = right_range - 1

    return new_path