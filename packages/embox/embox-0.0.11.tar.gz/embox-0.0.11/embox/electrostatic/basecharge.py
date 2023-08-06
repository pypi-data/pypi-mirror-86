"""
This module contains the Charge base class for all kinds of charges
"""
from abc import ABC, abstractmethod
from typing import Union, NoReturn

import numpy as np

from embox.geomesh.vector import Vector


class Charge(ABC):
    k = 9.0E9

    def __init__(self, density: Union[int, float]) -> NoReturn:
        self._density = float(density)

    @property
    def rho(self) -> float:
        return self._density

    @rho.setter
    def rho(self, density: Union[int, float]) -> NoReturn:
        self._density = density

    @abstractmethod
    def force_on(self, other, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def e_field_intensity(self, r: Union[Vector, list, np.ndarray], **kwargs):
        raise NotImplementedError
