"""
This module contains some plot helper functions
"""

from itertools import product, combinations
from typing import Union

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d

from .__config__ import formatter
from embox.geomesh.vector import Vector


class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0, 0), (0, 0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        FancyArrowPatch.draw(self, renderer)


def cube(bottom_left_corner: Vector, length: Union[int, float], **kwargs) -> [plt.figure, plt.Axes]:
    fig = plt.figure()
    ax = fig.gca(projection="3d")
    xs = [bottom_left_corner.x, bottom_left_corner.x + length]
    ys = [bottom_left_corner.y, bottom_left_corner.y + length]
    zs = [bottom_left_corner.z, bottom_left_corner.z + length]

    for s, e in combinations(np.array(list(product(xs, ys, zs))), 2):
        if np.sqrt(np.sum((s - e) ** 2, axis=-1)) == length:
            ax.plot3D(*zip(s, e), **kwargs)
    ax.xaxis.set_major_formatter(formatter)
    ax.yaxis.set_major_formatter(formatter)
    ax.zaxis.set_major_formatter(formatter)
    return fig, ax


def sphere(origin: Vector, radius: Union[int, float], **kwargs):
    pass
