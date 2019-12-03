import glob
import os
import shutil

_FILE_DIR = os.path.split(__file__)[0]
_PROJECT_TEMPLATE_PATH = os.path.join(_FILE_DIR, "report_template")

_TEMPLATE_STRUCTURE = {
    "auxiliary": [],
    "classfiles": glob.glob(os.path.join(_PROJECT_TEMPLATE_PATH, "*.cls")),
    "data": [],
    "figures": [],
    "latex": [],
    "output": [],
    "plots": [],
    "raw_data": [],
    "scripts": glob.glob(os.path.join(_PROJECT_TEMPLATE_PATH, "*.py")),
    "templates": glob.glob(os.path.join(_PROJECT_TEMPLATE_PATH, "*.tex")),
}


def ensure_directory_exists(path):
    """
    Checks whether a directory exists and creates it if it doesn't

    Parameters
    ----------
    path : str
        Path of the directory

    """
    if not os.path.isdir(path):
        os.mkdir(path)


def init_report_directory(path=""):
    """
    Builds a report project directory structure and creates some useful files including the makefile.

    Parameters
    ----------
    path : str
        Path of the project

    """
    if not path:
        path = os.getcwd()

    for directory, files in _TEMPLATE_STRUCTURE.items():
        dir_path = os.path.join(path, directory)
        ensure_directory_exists(dir_path)

        for file in files:
            shutil.copy(os.path.join(_PROJECT_TEMPLATE_PATH, file), dir_path)
