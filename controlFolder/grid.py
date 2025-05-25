# grid.py
from itertools import product

# how many fine‐grid cells to pad around each obstacle
CLEARANCE_RADIUS = 8

class Grid:
    def __init__(self, width, height, obstacles=None):
        self.i = width
        self.j = height
        self.grid = [[1]*width for _ in range(height)]
        self.obstacles = obstacles or []
        for (r, c) in self.obstacles:
            self.grid[r][c] = 0

    def get_adjacent(self, node):
        r, c = node
        if not (0 <= r < self.j and 0 <= c < self.i) or self.grid[r][c] != 1:
            return []
        nbrs = []
        for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < self.j and 0 <= nc < self.i and self.grid[nr][nc] == 1:
                # enforce clearance buffer
                safe = True
                for drr in range(-CLEARANCE_RADIUS, CLEARANCE_RADIUS+1):
                    for dcc in range(-CLEARANCE_RADIUS, CLEARANCE_RADIUS+1):
                        rr, cc = nr+drr, nc+dcc
                        if 0 <= rr < self.j and 0 <= cc < self.i and self.grid[rr][cc] == 0:
                            safe = False
                            break
                    if not safe:
                        break
                if safe:
                    nbrs.append((nr, nc))
        return nbrs

    def get_nodes(self):
        return [(r, c) for r, c in product(range(self.j), range(self.i))
                if self.grid[r][c] == 1]

    def plot_path(self, path):
        arr = [['_' for _ in range(self.i)] for __ in range(self.j)]
        for (r, c) in self.obstacles:
            arr[r][c] = 'X'
        for (r, c) in path:
            arr[r][c] = '.'
        return "\n".join("".join(row) for row in arr)
