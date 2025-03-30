import pandas as pd

path = pd.read_csv('pathFile.csv')

# Initialize the list to hold the moves
moves = []

# Iterate through the dataframe to determine the moves
for i in range(1, len(path)):
    y, x = path.iloc[i]
    moves.append((x,y))
    #print(f"({x},{y})")


print(moves)

def calc_lines(moves):
    lines = 0
    x = moves[0][0]
    y = moves[0][1]
    counter_x = 1
    counter_y = 1
    for i in range(1,len(moves)):
        if(moves[i][0] == x):
            counter_x = counter_x + 1
        else:
            if counter_x >= 30:
                lines = lines + 1
            counter_x = 0
            x = moves[i][0]

        if(moves[i][1] == y):
            counter_y = counter_y + 1
        else:
            if counter_y >= 30:
                lines = lines + 1
            counter_y = 0
            y = moves[i][1]
        
    return lines

def current_move(moves, index):
    prev_y, prev_x = moves[index - 1]
    curr_y, curr_x = moves[index]

    move = ""
   
    # Determine the move based on the change in coordinates
    if curr_y == prev_y + 1 and curr_x == prev_x:
        move = "forward"
    elif curr_y == prev_y - 1 and curr_x == prev_x:
        move = "backward"
    elif curr_y == prev_y and curr_x == prev_x + 1:
        move = "right"
    #elif curr_y == prev_y and curr_x == prev_x - 1:
    else:
        move = "left"


    return move

def calc_turnings(moves):
    turnings = 0

    move = current_move(moves,1)

    for i in range(2,len(moves)):

        c_move = current_move(moves,i)

        if(move != c_move):
            turnings = turnings + 1
            move = c_move

    return turnings




# print(f"Number of lines: {calc_lines(moves)}")
# print(f"Number of turnings: {calc_turnings(moves)}")




        


        


#def turn_straight(moves)