"""
This module contains some plot helper functions
"""
import matplotlib.pyplot as plt
import numpy as np
from empy.math.vector import Vector
from matplotlib import ticker

plt.rcParams['font.serif'] = ["JetBrains Mono", "Times New Roman"]
plt.rc('text', usetex=True)

formatter = ticker.ScalarFormatter(useMathText=True)
formatter.set_scientific(True)
formatter.set_powerlimits((-1, 1))


def plot_vector_addition(ax: plt.Axes, v1: Vector, v2: Vector, **kwargs):
    v3 = v1 + v2

    ax.quiver(0., 0., 0., v1.x, v1.y, v1.z, **kwargs)
    ax.quiver(v1.x, v1.y, v1.z, v2.x, v2.y, v2.z, **kwargs)
    ax.quiver(0., 0., 0., v3.x, v3.y, v3.z, **kwargs)

    return ax


def plot_curve(array: np.ndarray, **kwargs):
    """
    plot 2D curve, if the keyword fig_name is provided, the figure will be saved
    :param array: 2d ndarray
    :param kwargs: kwargs for plt.plot and some custom kwargs including the x_label, y_label, fig_title, fig_name
    :return:
    """
    if array.shape[1] != 2:
        raise ValueError("The input array must have and only have two columns")

    if "x_scale" in kwargs.keys():
        x_scale = kwargs["x_scale"]
        kwargs.pop("x_scale")
    else:
        x_scale = 1.0

    if "y_scale" in kwargs.keys():
        y_scale = kwargs["y_scale"]
        kwargs.pop("y_scale")
    else:
        y_scale = 1.0

    if "x_label" in kwargs.keys():
        x_label = kwargs["x_label"]
        kwargs.pop("x_label")
    else:
        x_label = ""

    if "y_label" in kwargs.keys():
        y_label = kwargs["y_label"]
        kwargs.pop("y_label")
    else:
        y_label = ""

    if "fig_title" in kwargs.keys():
        fig_title = kwargs["fig_title"]
        kwargs.pop("fig_title")
    else:
        fig_title = ""

    if "fig_name" in kwargs.keys():
        fig_name = kwargs["fig_name"]
        kwargs.pop("fig_name")
    else:
        fig_name = ""

    if "dpi" in kwargs.keys():
        dpi = kwargs["dpi"]
        kwargs.pop("dpi")
    else:
        dpi = 100
    with plt.style.context(['science', 'ieee', "grid", "retro"]):
        fig, ax = plt.subplots(1, 1, figsize=(16, 9))
        ax.plot(x_scale * array[:, 0], y_scale * array[:, 1], **kwargs)
        ax.yaxis.set_major_formatter(formatter)
        ax.set_xlabel(x_label, fontsize=20)
        ax.set_ylabel(y_label, fontsize=20)
        ax.set_title(fig_title, fontsize=20)
        ax.xaxis.set_tick_params(labelsize=16)
        ax.yaxis.set_tick_params(labelsize=16)
        plt.tight_layout()
        if fig_name == "":
            plt.show()
        else:
            plt.savefig(fig_name, dpi=dpi)
            plt.close()
