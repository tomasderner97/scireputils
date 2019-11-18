import os

import matplotlib
import matplotlib.pyplot as plt

_MATPLOTLIB_LATEX_STYLE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "latex_style.mplstyle")


def matplotlib_use_latex_style():
    plt.style.use(_MATPLOTLIB_LATEX_STYLE_PATH)


def matplotlib_restore_default_style():
    matplotlib.rcParams.update(matplotlib.rcParamsDefault)
