import sys
import random


class Node(object):
    x = 0
    y = 0

    def __init__(self, y, x):
        self.y = y
        self.x = x

    def tweak(self, ymod, xmod):
        return Node(self.y + ymod, self.x + xmod)

    def print_node(self):
        print "[%s,%s]" % (self.y, self.x)

    def is_same(self, othernode):
        if (self.y == othernode.y) and (self.x == othernode.x):
            return True
        else:
            return False


def g_score(map, origin, destination):                  # calculates G score
    score = 0
    if map[destination.y][destination.x] is "1":
        score += 10
    if abs(origin.y - destination.y) + abs(origin.x - destination.x) == 2:
        score += 14
    else:
        score += 10
    return score


def ymax(val1, val2, val3, val4):
    if val1 >= val2:
        if val1 >= val3:
            if val1 >= val4:
                return val1, "up"
            else:
                return val4, "left"
        else:
            if val3 >= val4:
                return val3, "right"
            else:
                return val4, "left"
    else:
        if val2 >= val3:
            if val2 >= val4:
                return val2, "down"
            else:
                return val4, "left"
        else:
            if val3 >= val4:
                return val3, "right"
            else:
                return val4, "left"


def map_reward(map, state, hue, winstate):
    if hue is True:
        if (0 <= state.y < 8) and (0 <= state.x < 10):
            if map[state.y][state.x] == (, -1):         # create a reward for the current state
                return -1
            elif map[state.y][state.x] == (, -2):
                return -2
            elif map[state.y][state.x] == (, None):
                return 0
        elif map[state.y][state.x] == 4:
            reward += 1
            reward = reward * (discount ^ step)
            return reward, 0
        elif (state.y == 0) and (state.x == 9):
            reward += 50
            reward = reward * (discount ^ step)
            return reward, 2
    else:
        return 0, 1


def MDP(map, new_map, cur_state, start, step, discount, trail, score, winfail, iterkill):
    state_value = map[start.y][start.x]
    if state_value is None:
        return None
                                                        # check reward and winstate
    # reward = map_reward(map, cur_state, rewutil, winfail)
    reward = map[cur_state.y][cur_state.x][1]

    if reward is None:
        return 0

    d_down = cur_state.tweak(1, 0)
    d_right = cur_state.tweak(0, 1)
    d_up = cur_state.tweak(-1, 0)
    d_left = cur_state.tweak(0, -1)
                                                        # find the utility of each direction
    u_down = 0.8 * map[d_down.y][d_down.x][0] + 0.1 * map[d_left.y][d_left.x][0] + 0.1 * map[d_right.y][d_right.x][0]
    u_right = 0.8 * map[d_right.y][d_right.x][0] + 0.1 * map[d_down.y][d_down.x][0] + 0.1 * map[d_up.y][d_up.x][0]
    u_up = 0.8 * map[d_up.y][d_up.x][0] + 0.1 * map[d_right.y][d_right.x][0] + 0.1 * map[d_left.y][d_left.x][0]
    u_left = 0.8 * map[d_left.y][d_left.x][0] + 0.1 * map[d_up.y][d_up.x][0] + 0.1 * map[d_down.y][d_down.x][0]
                                                        # find the best direction
    y_max_value, direction = ymax(u_up, u_down, u_right, u_left)
    max_utility = reward + y_max_value                  # find the state utility

    pointer = None
    down_trail = trail
    right_trail = trail
    up_trail = trail
    left_trail = trail
    if (0 <= cur_state.y < 8) and (0 <= cur_state.x < 10):
        iterdead = iterkill + 1                         # check all possible actions
        pointer = cur_state.tweak(-1, 0)
        down = MDP(map, pointer, step + 1, goal, discount, down_trail.append(pointer), score, winfail, iterdead)
        pointer = cur_state.tweak(0, 1)
        right = MDP(map, pointer, step + 1, goal, discount, right_trail.append(pointer), score, winfail, iterdead)
        pointer = cur_state.tweak(1, 0)
        up = MDP(map, pointer, step + 1, goal, discount, up_trail.append(pointer), score, winfail, iterdead)
        pointer = cur_state.tweak(0, -1)
        left = MDP(map, pointer, step + 1, goal, discount, left_trail.append(pointer), score, winfail, iterdead)
    else:                                               # avoid going off-map
        return trail, score, 1




    pointer = center.tweak(-1, 0)                       # add all valid nodes around the center
    if (0 <= pointer.y < 8) and (0 <= pointer.x < 10):
        tosearch.append(pointer)
    pointer = center.tweak(-1, 1)
    if (0 <= pointer.y < 8) and (0 <= pointer.x < 10):
        tosearch.append(pointer)
    pointer = center.tweak(0, 1)
    if (0 <= pointer.y < 8) and (0 <= pointer.x < 10):
        tosearch.append(pointer)
    pointer = center.tweak(1, 1)
    if (0 <= pointer.y < 8) and (0 <= pointer.x < 10):
        tosearch.append(pointer)
    pointer = center.tweak(1, 0)
    if (0 <= pointer.y < 8) and (0 <= pointer.x < 10):
        tosearch.append(pointer)
    pointer = center.tweak(1, -1)
    if (0 <= pointer.y < 8) and (0 <= pointer.x < 10):
        tosearch.append(pointer)
    pointer = center.tweak(0, -1)
    if (0 <= pointer.y < 8) and (0 <= pointer.x < 10):
        tosearch.append(pointer)
    pointer = center.tweak(-1, -1)
    if (0 <= pointer.y < 8) and (0 <= pointer.x < 10):
        tosearch.append(pointer)

    iterkill += 1
    if location.is_same(goal):                          # if goal is reached, return
        return trail, score, winfail
    elif scrutiny is None:
        return trail, score, winfail
    elif iterkill > 40:                                 # emergency overflow shutdown
        return trail, score, winfail
    else:                                               # if goal is not reached, iterate
        results = MDP(map, nex_state, goal, discount, trail, score, winfail, iterkill)
        return results[0], results[1], results[2]


def main(argv):                                         # -------MAIN----------------------------
    w = sys.argv[1]
    e = sys.argv[2]
    world = []
    new_world = []
    with open(w) as f:                                  # read in and clean up world data
        for line in f:
            world_in_list = line.strip("\n")
            world_in_list = world_in_list.strip("\r")
            world_in_list = world_in_list.strip("")
            world_in_list = world_in_list.split(" ")
            world.append(world_in_list)
    world.pop()
    for y in range(0, 7):
        for x in range(0, 9):
            if world[y][x] == 1:
                world[y][x] = (-1, -1, None)
            if world[y][x] == 2:
                world[y][x] = (0, None, None)
            if world[y][x] == 3:
                world[y][x] = (-2, -2, None)
            if world[y][x] == 4:
                world[y][x] = (1, 1, None)
            if world[y][x] == 50:
                world[y][x] = (50, 50, None)

    hol = Node(7, 0)                                   # worldbuilding and execution
    start = Node(0, 9)
    path = [hol]
    steps = 0
    start_state = hol
    totalscore = []
    sucess = 0
    leash = 1

    while leash > 0.5:
        result = MDP(world, new_world, hol, start, steps, e, path, totalscore, sucess, leash)

    sum = 0
    for r in range(0, len(result[1])-1):
        sum += result[1][r]
    print "Path followed:"
    for yy in result[0]:
        yy.print_node()
    print "Total F-Score is: %s" % sum
    print "Total number of unique node checks: %s" % result[2]


if __name__ == "__main__":
    main(sys.argv)


# Cited Code
# http://stackoverflow.com/questions/10393176/is-there-a-way-to-read-a-txt-file-and-store-each-line-to-memory
# May 1, 2012
#
# Reference MDP
# http://artint.info/html/ArtInt_227.html
# Copyright David Poole and Alan Mackworth, 2010
# Licenced under Creative Commons Attribution-Noncommercial-No Derivative Works 2.5 Canada License
