import os

import matplotlib.pyplot as plt

_MATPLOTLIB_LATEX_STYLE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "latex_style.mplstyle")


def latex_style():
    """
    Used as context.
    Usage
    -----
    with latex_style():
        plt...
    """
    return plt.style.context(_MATPLOTLIB_LATEX_STYLE_PATH)


def matplotlib_use_latex_style():
    plt.style.use(_MATPLOTLIB_LATEX_STYLE_PATH)
