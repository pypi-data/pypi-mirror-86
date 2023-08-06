"""
This module defines the vector in Cartesian coordinate system.
"""
from __future__ import annotations

from typing import Union

import numpy as np


class Vector(np.ndarray):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self[0] = args[0][0]
        self[1] = args[0][1]
        self[2] = args[0][2]

    @property
    def Ax(self) -> float:
        return self[0]

    @Ax.setter
    def Ax(self, x: Union[int, float]):
        self[0] = x

    @property
    def Ay(self) -> float:
        return self[1]

    @Ay.setter
    def Ay(self, y: Union[int, float]):
        self[1] = y

    @property
    def Az(self) -> float:
        return self[2]

    @Az.setter
    def Az(self, z: Union[int, float]):
        self[2] = z

    @property
    def norm(self):
        return np.sqrt(self.Ax ** 2 + self.Ay ** 2 + self.Az ** 2)

    @property
    def length(self):
        return self.norm

    @property
    def unit(self) -> "Vector":
        return Vector([self.Ax / self.length, self.Ay / self.length, self.Az / self.length])

    def perpendicular_to(self, other: "Vector") -> bool:
        """Check if self is perpendicular to other"""
        return np.allclose(self.dot(other), 0)

    def parallel_to(self, other: "Vector") -> bool:
        """Check if self is parallel to other"""
        return np.allclose(self.dot(other), self.length * other.length)

    def projection(self, other: "Vector") -> float:
        """Calculate the projection of self onto other"""
        return self.dot(other) / other.length

    def cross(self, other: "Vector") -> "Vector":
        """Cross product of self and other"""
        x_component = self.Ay * other.Az - self.Az * other.Ay
        y_component = self.Az * other.Ax - self.Ax * other.Az
        z_component = self.Ax * other.Ay - self.Ay * other.Ax
        return Vector([x_component, y_component, z_component])

    def __sub__(self, other: "Vector") -> "Vector":
        return Vector([self.Ax - other.Ax, self.Ay - other.Ay, self.Az - other.Az])

    def __eq__(self, other: "Vector") -> bool:
        return False if (self - other).any() else True

    def __new__(cls, *args, **kwargs):
        self = super(Vector, cls).__new__(cls, shape=(3,), **kwargs)
        self.__init__(*args, **kwargs)
        return self
