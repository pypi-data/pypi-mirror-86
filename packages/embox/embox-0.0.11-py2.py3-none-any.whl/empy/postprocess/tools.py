import os
from typing import Optional

import numpy as np

from .plot import plot_curve


def load_txt(file_path: str, delimiter: str = ",", skip_rows: Optional[int] = None) -> np.ndarray:
    """
    Load file
    :param file_path: path to the data file
    :param delimiter: delimiter between two columns
    :param skip_rows: the number of rows to skip
    :return:
    """
    return np.loadtxt(file_path, delimiter=delimiter, skiprows=skip_rows)


def post_files(root: str, file_names: list, fig_titles: list, fig_names: list, **kwargs):
    """
    Process the data files within root
    :param root: path of folder containing the data files
    :param file_names: the names of the data files
    :param fig_titles: the figure titles for the data files
    :param fig_names: the figure names for the data files
    :return:


    Example
    ________
    root = "./"
    file_names = ["1.txt", "2.txt", "3.txt"]
    fig_titles = ["1-1", "1-2", "1-3"]
    fig_names = ["1", "2", "3"]
    post_files(root, file_names, fig_titles, fig_names,
               x_scale=1E9, x_label="time [ns]", y_label="Voltage [V]", dpi=600)
    """
    if not os.path.isdir(root):
        raise ValueError("Given folder not exists")
    for f, title, name in zip(file_names, fig_titles, fig_names):
        file_path = os.path.join(root, f)
        data = load_txt(file_path, delimiter="\t", skip_rows=1)
        plot_curve(data, fig_title=title, fig_name=os.path.join(root, name + ".png"), **kwargs)
