"""
Fundamental point object in cartesian coordinate system
"""
from typing import Union

import numpy as np

from embox.geomesh.vector import Vector


class Point(np.ndarray):
    dim = 0

    @property
    def x(self):
        return self[0]

    @x.setter
    def x(self, x):
        self[0] = x

    @property
    def y(self):
        return self[1]

    @y.setter
    def y(self, y):
        self[1] = y

    @property
    def z(self):
        return self[2]

    @z.setter
    def z(self, z):
        self[2] = z

    def to_spherical(self) -> np.ndarray:
        """
        Convert self to spherical coordinate
        :return:
        Point in Spherical coordinate
        """
        r = np.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
        theta = np.arctan2(np.sqrt(self.x ** 2 + self.y ** 2), self.z)
        phi = np.arctan2(self.y, self.x)
        return np.array([r, theta, phi])

    def to_cylindrical(self) -> np.ndarray:
        """
        Convert self to cylindrical coordinate
        :return:
        Point in Cylindrical coordinate
        """
        rho = np.sqrt(self.x ** 2 + self.y ** 2)
        phi = np.arctan2(self.y, self.x)
        return np.array([rho, phi, self.z])

    @property
    def location(self) -> Vector:
        return Vector([self.x, self.y, self.z])

    def __str__(self):
        return f"[EMBOX] Point ({self.x}, {self.y}, {self.z})"

    def __new__(cls, data: Union[list, tuple, np.ndarray], dtype=float):
        self = np.ndarray.__new__(cls, shape=(3,), dtype=dtype)
        self[0] = data[0]
        self[1] = data[1]
        self[2] = data[2]
        return self
