#!/usr/bin/env python2
import rospy
from math import fabs, floor, sqrt
import time
from random import randint
from geometry_msgs.msg import Pose, PoseStamped
from map_manager import Map_manager
import numpy as np
from operator import attrgetter
import sys

debug = True


class Planner:
    def __init__(self, map_manager, step_size):
        self.cfree = map_manager.get_cfree()
        self.branch_length = step_size
        self.region_radius = step_size * 3 / 2
        self.map = map_manager
        self.tree = []

    class Tree:
        def __init__(self):
            self.node = []
            self.costTocome = 0
            self.branches = []

    def get_random_point(self):
        random_point = []
        rng = np.random.RandomState()
        x = rng.uniform(0, 384)
        y = rng.uniform(0, 384)
        random_point.append(x)
        random_point.append(y)

        return random_point

    def has_obstacle(self, xnear, xnew):
        result = False

        diff1 = xnew[0] - xnear[0]
        diff2 = xnew[1] - xnear[1]

        decimated_index = 0
        diff = 0

        if fabs(diff1) > fabs(diff2):
            diff = diff1
            decimated_index = 1
        else:
            diff = diff2
            decimated_index = 0

        points_to_check = []
        points_to_check.append(xnear)

        for i in range(int(fabs(floor(diff)))):
            point = []
            point.append(xnear[0] + i * diff1 / fabs(diff))
            point.append(xnear[1] + i * diff2 / fabs(diff))

            point[decimated_index] = floor(point[decimated_index])
            points_to_check.append(point)

            if floor(point[decimated_index]) != point[decimated_index]:
                point[decimated_index] += 1
                points_to_check.append(point)

        for j in range(len(points_to_check)):
            point = []
            point.append(floor(points_to_check[j][0]))
            point.append(floor(points_to_check[j][1]))
            if self.map.check_obstacle(point):
                result = True

        return result

    def find_nearest(self, xrand):
        xnear = []
        min_distance = 1000
        distance = 0

        for i in self.tree:
            print(i.node)
            distance = self.calculate_distance(xrand, i.node)
            if distance < min_distance:
                min_distance = distance
                xnear = i.node
        return xnear

    def new_node(self, xnear, xrand):
        xnew = []
        slope = (xrand[1] - xnear[1]) / (xrand[0] - xnear[0])
        adjuster = self.branch_length * sqrt(1 / (1 + pow(slope, 2)))

        point1, point2 = [], []
        point1.append(xnear[0] + adjuster)
        point1.append(xnear[1] + slope * adjuster)
        point2.append(xnear[0] - adjuster)
        point2.append(xnear[1] - slope * adjuster)

        distance1 = self.calculate_distance(xrand, point1)
        distance2 = self.calculate_distance(xrand, point2)

        if distance1 < distance2:
            xnew = point1
        else:
            xnew = point2

        return xnew

    def get_neighbor(self, xnew):
        neighbor = []
        for i in self.tree:
            if self.calculate_distance(i.node, xnew) < self.region_radius:
                neighbor.append(i)
        return neighbor

    def get_parent(self, neighbor):
        index = self.tree.index(neighbor[0]) if neighbor[0] in self.tree else -1
        print('index', index)
        min = 1000
        xnear = self.tree[index].node
        position = neighbor[0]

        for i in range(len(neighbor)):
            index = self.tree.index(neighbor[i]) if neighbor[i] in self.tree else -1
            print('index', index)
            if min > self.tree[index].costTocome:
                min = self.tree[index].costTocome
                xnear = self.tree[index].node
                position = index
                print('position', position)
        xnear.append(position)
        return xnear

    def find_parent(self, position_of_child):
        for i in range(len(self.tree)):
            for j in range(len(self.tree[i].branches)):
                if self.tree[i].branches[j] == position_of_child:
                    return i

    def randnum(self, min, max):
        return randint(0, max + min)

    def calculate_distance(self, first_point, second_point):
        return sqrt(pow(first_point[0] - second_point[0], 2) + pow(first_point[1] - second_point[1], 2))

    def make_plan(self, root, target):
        plan = []
        twig = Planner.Tree()
        twig.node = root
        self.tree.append(twig)

        target_list = []
        target_list.append(floor(target[0]))
        target_list.append(floor(target[1]))

        if self.map.check_obstacle(target_list):
            print("target in obstacle")
            return plan

        distance_to_target = self.branch_length + 20
        count = 0
        neihbor = []
        xnew = []
        xnear = []
        xnearest = []
        xrand = []
        parent = []
        position = 0
        xnew = root
        print("Starting Search\n")
        while distance_to_target > self.branch_length or self.has_obstacle(target, xnew) or count<10:
            count += 1

            if debug:
                print("Current count: ", count, " distance to target: ", distance_to_target, "has obstacle:",
                      self.has_obstacle(target, xnew))

            xrand = self.get_random_point()
            print(xrand)
            xnearest = self.find_nearest(xrand)
	    print(xnearest)
            if xnearest[0] == xrand[0] or xnearest[1] == xrand[1]:
                continue
            xnew = self.new_node(xnearest, xrand)
            neighbor = self.get_neighbor(xnew)
            parent = self.get_parent(neighbor)
            del xnear[:]
            xnear.append(parent[0])
            xnear.append(parent[1])
            position = parent[2]
            print(parent)
            print(position)
            point1 = []
            point2 = []

            point1.append(floor(xnear[0]))
            point1.append(floor(xnear[1]))
            point2.append(floor(xnew[0]))
            point2.append(floor(xnew[1]))

            if not self.has_obstacle(point1, point2):
                current_no_of_nodes = len(self.tree)

                
                print("Printing nodes\n")
                for i in self.tree:
                    print("[", i.node[0], ", ", i.node[1], "]\n")
                print("Press any key to continue..\n")
                str = sys.stdin.read(1)
                if str == ' ':
                    print('a')

                temp = Planner.Tree()
                temp.node = xnew
              
                temp.costTocome = self.tree[position].costTocome + self.calculate_distance(xnear, xnew)
		print('temp',temp.costTocome)
                self.tree.append(temp)

                self.tree[position].branches.append(current_no_of_nodes)

                distance_to_target = self.calculate_distance(xnew, target)
                print(distance_to_target, current_no_of_nodes)
                for i in range(len(neihbor)):
                    index = self.tree.index(neighbor[i]) if neighbor[i] in self.tree else -1
                    if self.tree[current_no_of_nodes].costTocome + self.calculate_distance(self.tree[index].node, xnew) < self.tree[index].costTocome:
                        location = self.find_parent(index)
                        self.tree[location].branches.remove(index)
                        self.tree[current_no_of_nodes].branches.append(index)

        current_no_of_nodes = len(self.tree)

        temp = Planner.Tree()
        temp.node = target
        temp.costTocome = self.tree[current_no_of_nodes - 1].costTocome + self.calculate_distance(target, xnew)
        self.tree.append(temp)

        self.tree[current_no_of_nodes - 1].branches.append(current_no_of_nodes)

        print("Search Optimal Path")

        node_number = current_no_of_nodes
        current_node = target
        print(node_number)
        print(current_node)
        print(root)

        while root[0] != current_node[0] or root[1] != current_node[1]:
            pos = PoseStamped()
            pos.pose.position.x = ((current_node[0] * 0.05) - 10)
            pos.pose.position.y = ((current_node[1] * 0.05) - 10)
            plan.append(pos)
            print(pos.pose.position.x, pos.pose.position.y)
            node_number = self.find_parent(node_number)
            current_node = self.tree[node_number].node
        print(plan)
        return plan








