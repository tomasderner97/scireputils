import os
from distutils.dir_util import copy_tree

_TEMPLATE_PATH = os.path.join(os.path.split(__file__)[0], "report_template")


def ensure_directory_exists(path):
    if not os.path.isdir(path):
        os.mkdir(path)


def init_report_directory(path=""):
    if not path:
        path = os.getcwd()

    ensure_directory_exists(path)

    copy_tree(_TEMPLATE_PATH, path)
