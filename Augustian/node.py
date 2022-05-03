import math
from queue import PriorityQueue

import numpy as np


class Node:
    """
        A node class for A* Pathfinding
        g is the cost from start to current node
        h is the heuristic based estimated cost for current node to goal
        f is the total cost f=h+g
    """

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.f = 0
        self.h = 0

    def __eq__(self, other):
        return self.position == other.position


def a_star_search(board, start, goal, occupied_list):
    if start == goal:
        return 0
    # initialize visited list and start and goal node and unvisited list
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, goal)
    end_node.g = end_node.h = end_node.f = 0

    open_list = []
    close_list = []

    open_list.append(start_node)

    # as long as the unvisited list is not null, keep iterate through
    while len(open_list) > 0:
        current_node = open_list[0]
        current_index = 0

        # rearrange the list in the order of the total cost which is f
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        open_list.pop(current_index)
        close_list.append(current_node)

        # if reach the goal, return the path
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]

        # children of this node
        children = []
        neighbor = neighbours(current_node.position, board)

        # only add children that's not in the occupied_list
        for c in neighbor:
            if c not in occupied_list:
                new_node = Node(current_node, c)
                children.append(new_node)

        for child in children:
            for closed_child in close_list:
                if child == closed_child:
                    continue

            child.g = axial_distance(child.position, start_node.position)
            child.h = h_heuristic(child.position, end_node.position)
            child.f = child.g + child.h

            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue
            if child not in close_list:
                open_list.append(child)


# connect to these nodes' neighbour
def neighbours(node, all_nodes):
    dirs = [[1, -1],  # up left
            [1, 0],  # up right
            [0, -1],  # left
            [0, 1],  # right
            [-1, 0],  # down left
            [-1, 1], ]  # down right
    result = []
    for i in dirs:
        neighbor = [node[0] + i[0], node[1] + i[1]]
        if neighbor in all_nodes:
            result.append(neighbor)
    return result


def h_heuristic(current, goal):
    (c1, c2) = current
    (g1, g2) = goal
    return abs(c1 - g1) + abs(c2 - g2)


def axial_distance(current, start):
    (c1, c2) = current
    (s1, s2) = start
    return (abs(c1 - s1)
            + abs(c1 + c2 - s1 - s2)
            + abs(c2 - s2)) / 2
