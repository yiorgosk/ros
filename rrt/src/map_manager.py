#!/usr/bin/env python2
import cv2 as cv
from math import floor
import sys
import numpy as np


class Map_manager:
    def __init__(self):
        self.cfree = []
        self.image = []

    def map_manager(self):
        self.image = cv.imread("/home/lascm/catkin_ws/src/rrt/maps/point_map.png",
                               cv.IMREAD_GRAYSCALE)
        if not self.image.data:
            rospy.loginfo("No data provided from map location. Please check the file path \n")
            sys.exit(0)

        for i in range(384):
            for j in range(394):
               if self.get_state(i, j)>150:
                    point = []
                    point.append(i)
                    point.append(j)
                    self.cfree.append(point)

    
    def map_manager(self, map_location):
        print("Map Location: ", map_location, "\n")
        self.image = cv.imread(map_location, cv.IMREAD_GRAYSCALE)

        if not self.image.any():
            print("No data \n")

        for i in range(384):
            for j in range(384):
                if self.get_state(i, j)>150:
                    point = []
                    point.append(i)
                    point.append(j)
                    self.cfree.append(point)

    def get_cfree(self):
        return self.cfree

    def get_state(self, x, y):
        for i in range(len(self.image)):
	    for j in range(len(self.image)):
                 if i==x and j==y:
                     return (self.image[384-j,i]

    def check_obstacle(self, grid):
        if self.get_state(grid[0], grid[1]) == 0:
            return True
        else:
            return False

    def grid_coordinate(self, pose):
        grid = []
        grid.append(floor((pose[0] + 10) * 20))
        grid.append(floor((pose[1] + 10) * 20))
        return grid

    def distance_coordinate(self, pose):
        distance = []
        distance.append((pose[0] * 0.05) - 10)
        distance.append((pose[1] * 0.05) - 10)
        return distance

    def show_image(self):
        cv.namedWindow("Display Window", cv.WINDOW_AUTOSIZE)
        cv.imshow("display Window", self.image)
        cv.waitKey(60000)


