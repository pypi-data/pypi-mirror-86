from typing import Union

import numpy as np

_Scalar = Union[int, float]


class Cartesian:
    def __init__(self, x: _Scalar = 0, y: _Scalar = 0, z: _Scalar = 0) -> None:
        self._x = x
        self._y = y
        self._z = z

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._y = y

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, z):
        self._z = z

    def to_spherical(self) -> "Spherical":
        """
        Convert self to spherical coordinate
        :return:
        Point in Spherical coordinate
        """
        r = np.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
        theta = np.arctan2(np.sqrt(self.x ** 2 + self.y ** 2), self.z)
        phi = np.arctan2(self.y, self.x)
        return Spherical(r, theta, phi)

    def to_cylindrical(self) -> "Cylindrical":
        """
        Convert self to cylindrical coordinate
        :return:
        Point in Cylindrical coordinate
        """
        rho = np.sqrt(self.x ** 2 + self.y ** 2)
        phi = np.arctan2(self.y, self.x)
        return Cylindrical(rho, phi, self.z)


class Cylindrical:
    def __init__(self, rho: _Scalar = 0, phi: _Scalar = 0, z: _Scalar = 0) -> None:
        self._rho = rho
        self._phi = phi
        self._z = z

    @property
    def rho(self):
        return self._rho

    @rho.setter
    def rho(self, rho):
        self._rho = rho

    @property
    def phi(self) -> _Scalar:
        """
        Angle to positive x-axis in radians
        :return:
        angle to x-axis in radians
        """
        return self._phi

    @phi.setter
    def phi(self, phi):
        """Angle to positive x-axis in radians"""
        self._phi = phi

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, z):
        self._z = z

    def to_cartesian(self):
        x = self._rho * np.cos(self._phi)
        y = self._rho * np.sin(self._phi)
        return Cartesian(x, y, self.z)


class Spherical:
    def __init__(self, r: _Scalar = 0, theta: _Scalar = 0, phi: _Scalar = 0) -> None:
        self._r = r
        self._theta = theta
        self._phi = phi

    @property
    def r(self):
        return self._r

    @r.setter
    def r(self, r):
        self._r = r

    @property
    def theta(self):
        """Angle to positive z-axis in radians"""
        return self._theta

    @theta.setter
    def theta(self, theta):
        """Angle to positive z-axis in radians"""
        self._theta = theta

    @property
    def phi(self):
        """Angle to positive x-axis in radians"""
        return self._phi

    @phi.setter
    def phi(self, phi):
        """Angle to positive x-axis in radians"""
        self._phi = phi

    def to_cartesian(self):
        """Convert self to cartesian coordinate"""
        x = self.r * np.sin(self._theta) * np.cos(self._phi)
        y = self.r * np.sin(self.theta) * np.sin(self.phi)
        z = self.r * np.cos(self.theta)
        return Cartesian(x, y, z)
