# astar.py
from math import inf, sqrt

def heuristic_cost(src, dest):
    return sqrt((dest[0]-src[0])**2 + (dest[1]-src[1])**2)

def reconstruct_path(prev, current):
    path = [current]
    while current in prev:
        current = prev[current]
        path.append(current)
    return list(reversed(path))

def a_star(grid, src, dest):
    nodes = set(grid.get_nodes())
    if src not in nodes or dest not in nodes:
        raise ValueError(f"Invalid src or dest: {src}, {dest}")

    open_set = {src}
    prev      = {}
    g_score   = {n: inf for n in nodes}
    f_score   = {n: inf for n in nodes}
    g_score[src] = 0
    f_score[src] = heuristic_cost(src, dest)

    while open_set:
        current = min(open_set, key=lambda n: f_score[n])
        if current == dest:
            return reconstruct_path(prev, current)
        open_set.remove(current)

        for nbr in grid.get_adjacent(current):
            tentative = g_score[current] + 1
            if tentative < g_score.get(nbr, inf):
                prev[nbr]    = current
                g_score[nbr] = tentative
                f_score[nbr] = tentative + heuristic_cost(nbr, dest)
                open_set.add(nbr)

    raise ValueError(f"No path found from {src} to {dest}")
