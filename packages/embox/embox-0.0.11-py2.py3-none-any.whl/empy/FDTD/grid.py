"""
FDTD calculation space with Cartesian coordinates
"""
from typing import Sequence, Iterable, Union

import numpy as np
from mpi4py import MPI


class Grid(object):
    def __init__(self, size: Union[Sequence, Iterable], resolution: Union[int, Sequence, Iterable] = 15,
                 parallel=False):
        """
        Create a FDTD calculation space.
        :param size: Sequence or Iterable, 3-element sequence consisting of non-negative numbers
        :param resolution: int, Sequence, Iterable, the number of sections in one unit. Default to 15.
        :param parallel: bool, whether space be divided into segments. Default to False.
        """

        if isinstance(resolution, int):
            self._res = np.array((resolution,) * 3, np.double)
        else:
            self._res = np.array(resolution, np.double)

        self._dr = np.array(1.0 / self._res, np.double)

        self._half_size = 0.5 * np.array(size, np.double)

        for idx, value in enumerate(self._dr):
            if self._half_size[idx] == 0:
                self._half_size[idx] = 0.5 * value

        self._whole_field_size = np.array(np.round(2.0 * self._half_size * self._res), np.int)

        self._id = 0
        self._num_procs = 1

        if parallel:
            self._id = MPI.COMM_WORLD.rank
            self._num_procs = MPI.COMM_WORLD.size
            self._cart_comm = MPI.COMM_WORLD.Create_cart(self.find_best_deploy(), (1, 1, 1))

