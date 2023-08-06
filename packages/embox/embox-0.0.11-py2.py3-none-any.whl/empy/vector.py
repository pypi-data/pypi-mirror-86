"""
This module defines the vector in Cartesian coordinate system.
"""
from __future__ import annotations

from typing import Union

import numpy as np

_Scalar = Union[int, float]


class Vector(object):
    def __init__(self, x: _Scalar = 0, y: _Scalar = 0, z: _Scalar = 0) -> None:
        self._x = x
        self._y = y
        self._z = z

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def z(self):
        return self._z

    @property
    def norm2(self):
        return np.sqrt(self._x ** 2 + self._y ** 2 + self._z ** 2)

    @property
    def mag(self):
        return self.norm2

    @property
    def unit(self):
        return Vector(self._x / self.mag, self._y / self.mag, self._z / self.mag)

    def dot(self, other: "Vector") -> _Scalar:
        """Dot product of self and other"""
        return self._x * other.x + self._y * other.y + self._z * other.z

    def perpendicular_to(self, other: "Vector") -> bool:
        """Check if self is perpendicular to other"""
        return np.allclose(self.dot(other), 0)

    def parallel_to(self, other: "Vector") -> bool:
        """Check if self is parallel to other"""
        return np.allclose(self.dot(other), self.mag * other.mag)

    def projection(self, other: "Vector") -> float:
        """Calculate the projection of self onto other"""
        return self.dot(other) / other.mag

    def cross(self, other: "Vector") -> "Vector":
        """Cross product of self and other"""
        x_component = self._y * other.z - self.z * other.y
        y_component = self.z * other.x - self.x * other.z
        z_component = self.x * other.y - self.y * other.x
        return Vector(x_component, y_component, z_component)

    def __add__(self, other: "Vector") -> "Vector":
        """Calculate the addition of self and other"""
        return Vector(self._x + other.x, self._y + other.y, self._z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other: Union[int, float, "Vector"]) -> Union[float, "Vector"]:
        if isinstance(other, int) or isinstance(other, float):
            return Vector(self.x * other, self.y * other, self.z * other)
        else:
            return self.dot(other)

    def __rmul__(self, other: Union[int, float, "Vector"]) -> Union[float, "Vector"]:
        return self.__mul__(other)

    def __eq__(self, other):
        """Check if self is equal to other"""
        return True if self._x == other.x and self._y == other.y and self._z == other.z else False

    def __neg__(self):
        """the negative of self"""
        return Vector(-self.x, -self.y, -self.z)

    def __str__(self):
        return f"Vector({self.x}, {self.y}, {self.z})"
