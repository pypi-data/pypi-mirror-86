"""
Coulomb's Law states that the force F between two point charges Q1 and Q2 is:

(1) Along the line joining them
(2) Directly proportional to the product Q1Q2 of the charges
(3) Inversely proportional to the square of the distance R between them
"""
from typing import Union

import numpy as np

from .basecharge import Charge
from .pointcharge import PointCharge
from ..geomesh.line import Line
from ..geomesh.point import Point
from embox.geomesh.vector import Vector


class LineCharge(Charge, Line):
    def __init__(self, rho: Union[int, float], start: Point, end: Point):
        """
        A Straight line charge with uniform charge density rho extending from start point to end point
        :param rho: the uniform charge density
        :param start: start point of the line
        :param end: end point of the line
        """
        Charge.__init__(self, rho)
        Line.__init__(self, start, end)

    @property
    def unit_vec(self):
        return (self.end_point.location - self.start_point.location).unit

    def force_on(self, point_charge: PointCharge, **kwargs):
        """
        Calculate the force on a point charge by self

        :param point_charge: the point charge
        :param kwargs: dx is required for numerical integral
        :return: the total force on point charge
        """
        if "dx" not in kwargs.keys():
            raise ValueError("LineCharge E-field intensity calculation needs dx for numerical integral")
        else:
            dx = kwargs["dx"]

        increment = dx * self.unit_vec

        N = int(np.floor((self.end_point.location - self.start_point.location).length / dx))

        total_force = Vector([0, 0, 0])
        loc = self.start_point.location
        for _ in range(N):
            q = PointCharge(self.rho * dx, loc)
            field = q.force_on(point_charge)
            loc += increment
            total_force += field
        return total_force

    def e_field_intensity(self, r: Union[Vector, np.ndarray], **kwargs) -> Vector:
        """
        Calculate the E-field intensity at given location by self

        :param r: the specified location
        :param kwargs: dx is required for numerical integral
        :return: the total E-field intensity at given location
        """
        if "dx" not in kwargs.keys():
            raise ValueError("LineCharge E-field intensity calculation needs dx for numerical integral")
        else:
            dx = kwargs["dx"]

        increment = dx * self.unit_vec

        N = int(np.floor((self.end_point.location - self.start_point.location).length / dx))
        total_field = Vector([0, 0, 0])
        loc = self.start_point.location
        for _ in range(N):
            q = PointCharge(self.rho * dx, loc)
            field = q.e_field_intensity(r)
            loc += increment
            total_field += field
        return total_field
