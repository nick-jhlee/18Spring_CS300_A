# 이정현 a.k.a. Nick Lee 20170500
# Version 1: Assume no orange tiles, circles or crosses on the terrain

import sys

# Queues(list) for BFS Algorithm
# Hash table(dictionary) for finding ancestors
visited_vertices = []
state_sequence = []
total_vertices = []
prev = {}


# Define maps, matching each possible move with each possible state of a box
# PS is acronym for Possible States
# M is acronym for Movement
M = []
PS = ["straight", "upsidedown", "lieright", "lieleft", "lieup", "liedown"]
tmp = {0: 1, 1: 0, 2: 3, 3: 2, 4: 5, 5: 4}

t_right = {PS[0]: 2, PS[1]: 1, PS[2]: 1, PS[3]: 2, PS[4]: 1, PS[5]: 1}
b_right = {PS[x]: t_right[PS[tmp[x]]] for x in range(6)}

t_left = {PS[0]: 2, PS[1]: 1, PS[2]: 2, PS[3]: 1, PS[4]: 1, PS[5]: 1}
b_left = {PS[x]: t_left[PS[tmp[x]]] for x in range(6)}

t_up = {PS[0]: 2, PS[1]: 1, PS[2]: 1, PS[3]: 1, PS[4]: 1, PS[5]: 2}
b_up = {PS[x]: t_up[PS[tmp[x]]] for x in range(6)}

t_down = {PS[0]: 2, PS[1]: 1, PS[2]: 1, PS[3]: 1, PS[4]: 2, PS[5]: 1}
b_down = {PS[x]: t_down[PS[tmp[x]]] for x in range(6)}

# Define dics for change in state of the box for each move
rm = {PS[0]: PS[2], PS[1]: PS[3], PS[2]: PS[1], PS[3]: PS[0], PS[4]: PS[4], PS[5]: PS[5]}
lm = {PS[0]: PS[3], PS[1]: PS[2], PS[2]: PS[0], PS[3]: PS[1], PS[4]: PS[4], PS[5]: PS[5]}
um = {PS[0]: PS[4], PS[1]: PS[5], PS[2]: PS[2], PS[3]: PS[3], PS[4]: PS[1], PS[5]: PS[0]}
dm = {PS[0]: PS[5], PS[1]: PS[4], PS[2]: PS[2], PS[3]: PS[3], PS[4]: PS[0], PS[5]: PS[1]}

# Define dic that maps each change of state to one of [R, L, U, D]
right = [(0, 2), (1, 3), (2, 1), (3, 0)]
left = [(x[1], x[0]) for x in right]
up = [(0, 4), (1, 5), (4, 1), (5, 0)]
down = [(x[1], x[0]) for x in up]

steps = ["R", "L", "U", "D"]
lists = [right, left, up, down]

convert_to_step = {(PS[x[0]], PS[x[1]]): steps[i] for i in range(4) for x in lists[i]}


# Define box class with the following attributes and methods
# state, (coordinates of) top and bottom, position = (top, bottom)
# move(right, left, up, down)
class Box:
    def __init__(self, state, top, bottom):
        self.state = state
        self.top = top
        self.bottom = bottom
        self.position = (self.top, self.bottom)

    def right(self):
        self.top = (self.top[0] + t_right.get(self.state), self.top[1])
        self.bottom = (self.bottom[0] + b_right.get(self.state), self.bottom[1])
        self.state = rm.get(self.state)

    def left(self):
        self.top = (self.top[0] - t_left.get(self.state), self.top[1])
        self.bottom = (self.bottom[0] - b_left.get(self.state), self.bottom[1])
        self.state = lm.get(self.state)

    def up(self):
        self.top = (self.top[0], self.top[1] - t_up.get(self.state))
        self.bottom = (self.bottom[0], self.bottom[1] - b_up.get(self.state))
        self.state = um.get(self.state)

    def down(self):
        self.top = (self.top[0], self.top[1] + t_down.get(self.state))
        self.bottom = (self.bottom[0], self.bottom[1] + b_down.get(self.state))
        self.state = dm.get(self.state)

    def move(self, i):
        if i == 0:
            self.right()
        if i == 1:
            self.left()
        if i == 2:
            self.up()
        if i == 3:
            self.down()

# Return the possible configurations(nodes) that can result by moving from a given position
def neighbors(Tiles, box):
    neighbor = []
    for i in range(4):
        tmp = Box(box.state, box.top, box.bottom)
        tmp.move(i)
        s = tmp.state
        t = tmp.top
        b = tmp.bottom
        if t in Tiles and b in Tiles:
            neighbor.append(Box(s, t, b))
    return neighbor


# Implement the BFS algorithm that stops when the box is "straight" or "upsidedown" on the destination(D)
def BFS(Tiles, box, D):
    total_vertices.append(box.position)
    visited_vertices.append(box.position)
    state_sequence.append(box.state)
    while len(visited_vertices) != 0:
        v = visited_vertices.pop(0)
        s = state_sequence.pop(0)
        box = Box(s, v[0], v[1])
        for node in neighbors(Tiles, box):
            position = node.position
            state = node.state
            if position in total_vertices:
                continue
            prev[position] = v
            total_vertices.append(position)
            visited_vertices.append(position)
            state_sequence.append(state)
            if (D, D) == position:
                return prev
    return prev

# Construct the path from S(starting position) to D(destination)
def Path(prev, D):
    dest = (D, D)
    if dest not in prev:
        return "No solution!"
    path = [dest]
    while prev.get(dest) is not None:
        path.append(prev.get(dest))
        dest = prev.get(dest)
    path.reverse()
    return path

# Show the sequence of [R, L, U, D] needed to construct the given path, assuming that the starting state is "straight"
def ShowSteps(path):
    if isinstance(path, str):
        return path
    steps = []
    sequential_state = []
    iposition = path.pop(0)
    box = Box("straight", iposition[0], iposition[1])
    sequential_state.append(box.state)

    for position in path:
        for i in range(4):
            tmp = Box(box.state, box.top, box.bottom)
            tmp.move(i)
            s = tmp.state
            t = tmp.top
            b = tmp.bottom
            if position == (t, b):
                sequential_state.append(s)
                box = Box(s, t, b)
                continue
    path.insert(0, iposition)

    l = len(sequential_state)
    for i in range(l-1):
        s1 = sequential_state[i]
        s2 = sequential_state[i+1]
        if s1 == s2:
            p1 = path[i]
            p2 = path[i+1]
            if p1[0][0] == p1[1][0]:
                if p1[0][0] < p2[0][0]:
                    steps.append("R")
                else:
                    steps.append("L")
            else:
                if p1[0][1] < p2[0][1]:
                    steps.append("D")
                else:
                    steps.append("U")
        else:
            steps.append(convert_to_step[(s1, s2)])
    return "".join(steps)


# Import the level txt file and covert it to a list of coordinates as stated in the instruction
# Tiles store all tiles that are not '-'
leveltxtname = sys.argv[1]
leveltxt = open(leveltxtname, "r")

Tiles = []
Start = None
Destination = None

y = 1
for l in leveltxt:
    x = 1
    line = l.strip()
    for tile in line:
        # Treat circles and crosses as regular tiles
        # Break out of the loop when the line specifying the behaviors of circles and crosses is reached
        if tile == '#':
            break
        if tile != '-':
            Tiles.append((x, y))
        if tile == 'S':
            Start = (x, y)
        if tile == 'T':
            Destination = (x, y)
        x += 1
    y += 1

leveltxt.close()

# If the level does not contain starting or/and ending position, return "No such level"
# initialize the box at the starting position(Start)
# Run BFS on the given level and construct a path from S to D, if there is one
# Convert the path to set of instructions, which is always the optimal solution
# If there is no such path, return "No solution!"
if None not in {Start, Destination}:
    box = Box("straight", Start, Start)
    prev = BFS(Tiles, box, Destination)
    sol_path = Path(prev, Destination)
    print(sol_path)
    answer = ShowSteps(sol_path)
    print(answer)
    print(len(answer))
else:
    print("No such level...")
