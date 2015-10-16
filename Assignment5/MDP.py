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


def print_map(land):
    for y in range(0, 8):
        for x in range(0, 10):
            location = land[y][x]
            print "[%s,%s,%s]" % (location[0], location[1], location[2]),
        print "\n"


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

def map_direction(map, state):
    if (0 <= state.y < 8) and (0 <= state.x < 10):
        # return the reward
        reward = map[state.y][state.x][1]
        if reward is None:
            # wall condition
            return 0
        else:
            return map[state.y][state.x][2]
    else:
        return 0


def map_reward(map, state):
    if (0 <= state.y < 8) and (0 <= state.x < 10):
        # return the reward
        reward = map[state.y][state.x][1]
        if reward is None:
            return 0
        else:
            return reward
    else:
        return 0


def map_utility(map, state):
    if (0 <= state.y < 8) and (0 <= state.x < 10):
        # return the reward
        reward = map[state.y][state.x][1]
        if reward is None:
            return 0
        else:
            return map[state.y][state.x][0]
    else:
        return 0


def MDP(map, new_map, cur_state, start, step, discount):
    state_value = map[start.y][start.x]
    if state_value is None:
        return None

        # check reward
    reward = map_reward(map, cur_state)

        # avoid walls
    if reward is None:
        return 0

        # check the neighboring directions
    d_down = cur_state.tweak(1, 0)
    d_right = cur_state.tweak(0, 1)
    d_up = cur_state.tweak(-1, 0)
    d_left = cur_state.tweak(0, -1)
        # find the utility of each direction, (probability * (future value + reward))
    u_down = (0.8 * (map_utility(map, d_down) + map_reward(map, d_down))) + (0.1 * (map_utility(map, d_left) + map_reward(map, d_left))) + (0.1 * (map_utility(map, d_right) + map_reward(d_right)))
    u_right = (0.8 * (map_utility(map, d_right) + map_reward(map, d_right))) + (0.1 * (map_utility(map, d_down.y) + map_reward(map, d_down))) + (0.1 * (map_utility(map, d_up) + map_reward(map, d_up)))
    u_up = (0.8 * (map_utility(map, d_up) + map_reward(map, d_up))) + (0.1 * (map_utility(map, d_right) + map_reward(map, d_right))) + (0.1 * (map_utility(map, d_left) + map_reward(map, d_left)))
    u_left = (0.8 * (map_utility(map, d_left) + map_reward(map, d_left))) + (0.1 * (map_utility(map, d_up) + map_reward(map, d_up))) + (0.1 * (map_utility(map, d_down) + map_reward(map, d_down)))

        # find the best direction
    y_max_value, direction = ymax(u_up, u_down, u_right, u_left)
        # find the state utility
    max_utility = reward + y_max_value
        # read into new map
    new_map[cur_state.y][cur_state.x] = [max_utility, reward, direction]
        # find the change
    delta_utility = abs(map_utility(new_map, cur_state) - map_utility(map, cur_state))

    return new_map, delta_utility


def main(argv):                                         # -------MAIN----------------------------
    w = sys.argv[1]
    e = sys.argv[2]
    world = []
    with open(w) as f:                                  # read in and clean up world data
        for line in f:
            world_in_list = line.strip("\n")
            world_in_list = world_in_list.strip("\r")
            world_in_list = world_in_list.strip("")
            world_in_list = world_in_list.split(" ")
            world.append(world_in_list)
    world.pop()

    '''
    print world
    '''

    # world[y][x] = (utility, reward, direction)
    for y in range(0, 8):
        for x in range(0, 10):
            if world[y][x] == '0':
                # open space
                world[y][x] = [0, 0, None]
            if world[y][x] == '1':
                # mountains
                world[y][x] = [0, -1, None]
            if world[y][x] == '2':
                # walls
                world[y][x] = [0, None, None]
            if world[y][x] == '3':
                # snakes
                world[y][x] = [0, -2, None]
            if world[y][x] == '4':
                # barns
                world[y][x] = [0, 1, None]
            if world[y][x] == '50':
                # apples
                world[y][x] = [0, 50, None]

    hol = Node(7, 0)                                   # worldbuilding and execution
    start = Node(0, 9)
    new_world = world
    old_world = world
    entropy = 0.9
    path = [hol]
    steps = 0
    start_state = hol
    scorecard = []
    totalscore = 0
    success = False
    leash = 1
    safety = True

        # iterate maps until utility change falls below threshold
    while leash > e:
        net = 0
        for h in range(0, 8):
            for g in range(0, 10):
                new_world, delta = MDP(old_world, new_world, Node(h, g), start, steps, entropy)
                print "hi-sign"
                if delta > net:
                    net = delta
        leash = delta
        old_world = new_world

        # Move the Horse through the map
    leash = 40
    w = 0
    while safety is True:
        w += 1
        if map_reward(new_world, hol) is None:
            # wall contingent
            safety = False
        elif map_reward(new_world, hol) == 50:
            # win condition
            safety = False
            success = True
        elif map_direction(new_world, hol) is "left":
            hol = hol.tweak(0, -1)
            path.append(hol)
            steps += 1
        elif map_direction(new_world, hol) is "up":
            hol = hol.tweak(-1, 0)
            path.append(hol)
            steps += 1
        elif map_direction(new_world, hol) is "right":
            hol = hol.tweak(0, 1)
            path.append(hol)
            steps += 1
        elif map_direction(new_world, hol) is "down":
            hol = hol.tweak(1, 0)
            path.append(hol)
            steps += 1
        elif map_direction(new_world, hol) == 0:
            print "Something dumb happened."
            safety = False
        if w == leash:
            # prevent infinte loops
            safety = False

        # total the score
    for q in range(0, len(scorecard)):
        totalscore += scorecard[q]

        # give a report printout
    if success is False:
        print "Path Failure, horse is lost, mismatch."
        print "%s steps taken." % steps
        print "Scorecard: %s" % scorecard
        print "Total Score: %s" % totalscore
        print "\n"
        print_map(new_world)
    else:
        print "Path Success, horse has found apples!"
        print "%s steps taken." % steps
        print "Scorecard: %s" % scorecard
        print "Total Score: %s" % totalscore
        print "\n"
        print_map(new_world)



    '''
    sum = 0
    for r in range(0, len(result[1])-1):
        sum += result[1][r]
    print "Path followed:"
    for yy in result[0]:
        yy.print_node()
    print "Total F-Score is: %s" % sum
    print "Total number of unique node checks: %s" % result[2]
    '''

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
