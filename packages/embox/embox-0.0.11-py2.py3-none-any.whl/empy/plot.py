"""
This module contains some plot helper functions
"""
import matplotlib.pyplot as plt

from .vector import Vector


def plot_vector_addition(ax: plt.Axes, v1: Vector, v2: Vector, **kwargs):
    v3 = v1 + v2

    ax.quiver(0., 0., 0., v1.x, v1.y, v1.z, **kwargs)
    ax.quiver(v1.x, v1.y, v1.z, v2.x, v2.y, v2.z, **kwargs)
    ax.quiver(0., 0., 0., v3.x, v3.y, v3.z, **kwargs)

    return ax
