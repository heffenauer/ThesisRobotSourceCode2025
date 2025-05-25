import numpy as np

def find_move(path, i):
    """Return 'forward'/'backward'/'left'/'right' between path[i-1]→path[i]."""
    py, px = path[i-1]
    cy, cx = path[i]
    if   cy == py-1 and cx == px: return "forward"
    elif cy == py+1 and cx == px: return "backward"
    elif cx == px+1 and cy == py: return "right"
    elif cx == px-1 and cy == py: return "left"
    return None

def end_points(path):
    """
    From the raw A* path:
      - first_move: 'forward' or 'backward'
      - first_up:   index where that move changes
      - far_left:   minimal x across entire path
      - biggest_up: minimal y across entire path
    """
    first_move = find_move(path, 1)
    # find where that first_move stops
    first_up = 1
    for i in range(2, len(path)):
        if find_move(path, i) != first_move:
            first_up = i-1
            break
    far_left   = min(p[1] for p in path)
    biggest_up = min(p[0] for p in path)
    return first_move, first_up, far_left, biggest_up

def complex_path(path, first_up, far_left, biggest_up):
    """
    Build a new path that:
      1) goes straight to path[first_up]
      2) then moves in x from that x down to far_left
      3) then moves in y from that y down to biggest_up
      4) then moves in x from that x up to final x of original
    """
    # start with everything up to first_up
    newp = path[: first_up+1 ]
    y0, x0 = newp[-1]

    # phase 2: slide left from x0 down to far_left
    for x in range(x0-1, far_left-1, -1):
        newp.append((y0, x))

    # phase 3: slide up from y0 down to biggest_up
    for y in range(y0-1, biggest_up-1, -1):
        newp.append((y, far_left))

    # phase 4: slide right from far_left up to path[-1][1]
    final_x = path[-1][1]
    final_y = path[-1][0]
    y1 = newp[-1][0]
    for x in range(far_left+1, final_x+1):
        newp.append((y1, x))

    return newp

def path_to_moves(path):
    """
    Collapse a grid‐cell path into (direction, steps) runs.
    """
    if len(path) < 2:
        return []
    dir_map = {(-1,0):'forward',(1,0):'backward',(0,1):'right',(0,-1):'left'}
    moves = []
    # start with first delta
    dy = path[1][0]-path[0][0]
    dx = path[1][1]-path[0][1]
    curr = dir_map[(dy,dx)]
    cnt = 1
    for (y0,x0),(y1,x1) in zip(path[1:], path[2:]):
        d = (y1-y0, x1-x0)
        dname = dir_map.get(d)
        if dname == curr:
            cnt += 1
        else:
            moves.append((curr, cnt))
            curr, cnt = dname, 1
    moves.append((curr, cnt))
    return moves

def adapt_path(path, grid=None):
    """
    1) Identify first straight run -> first_up  
    2) Build detour via complex_path  
    3) Collapse into (dir,steps)
    """
    _, first_up, far_left, biggest_up = end_points(path)
    newp = complex_path(path, first_up, far_left, biggest_up)
    moves = path_to_moves(newp)
    return newp, moves
