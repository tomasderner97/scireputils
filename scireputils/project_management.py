import glob
import os
import shutil

_FILE_DIR = os.path.split(__file__)[0]
_TEMPLATE_PATH = os.path.join(_FILE_DIR, "report_template")

_TEMPLATE_STRUCTURE = {
    "": ["makefile"],
    "auxiliary": [],
    "classfiles": glob.glob(os.path.join(_TEMPLATE_PATH, "*.cls")),
    "data": [],
    "figures": [],
    "latex": [],
    "output": [],
    "plots": [],
    "raw_data": [],
    "scripts": glob.glob(os.path.join(_TEMPLATE_PATH, "*.py")),
    "templates": glob.glob(os.path.join(_TEMPLATE_PATH, "*.tex")),
}


def ensure_directory_exists(path):
    if not os.path.isdir(path):
        os.mkdir(path)


def init_report_directory(path=""):
    if not path:
        path = os.getcwd()

    for directory, files in _TEMPLATE_STRUCTURE.items():
        dir_path = os.path.join(path, directory)
        ensure_directory_exists(dir_path)

        for file in files:
            shutil.copy(os.path.join(_TEMPLATE_PATH, file), dir_path)
