"""
Fundamental straight line object in cartesian coordinate system
"""
from typing import List

from .point import Point


class BaseLine(object):
    dim = 1

    def __init__(self, points: List[Point]):
        self._points = points

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, points: List[Point]):
        self._points = points


class Line(BaseLine):
    def __init__(self, start: Point, end: Point):
        """
        Straight line form start to end
        :param start: the start point of the line
        :param end: the end point of the line
        """
        BaseLine.__init__(self, [start, end])

    @property
    def start_point(self) -> Point:
        return self.points[0]

    @start_point.setter
    def start_point(self, start: Point):
        self.points[0] = start

    @property
    def end_point(self) -> Point:
        return self.points[1]

    @end_point.setter
    def end_point(self, end: Point):
        self.points[1] = end


class Spline(BaseLine):
    def __init__(self, points: List[Point]):
        """
        create a b-spline based on given control points
        :param points: the data points defining a curve
        """
        BaseLine.__init__(self, points)
