import glob
import os
import shutil

import report_template.paths as paths

_FILE_DIR = os.path.split(__file__)[0]
_PROJECT_TEMPLATE_PATH = os.path.join(_FILE_DIR, "report_template")

_PATHS_FILE_FROM_PROJECT_ROOT = "scripts/paths.py"

_TEMPLATE_STRUCTURE = {
    paths.AUXILIARY_PATH: [],
    paths.CLASSFILES_PATH: glob.glob(os.path.join(_PROJECT_TEMPLATE_PATH, "*.cls")),
    paths.DATA_PATH: [],
    paths.FIGURES_PATH: [],
    paths.LATEX_PATH: [],
    paths.OUTPUT_PATH: [],
    paths.PLOTS_PATH: [],
    paths.RAW_DATA_PATH: [],
    paths.SCRIPTS_PATH: glob.glob(os.path.join(_PROJECT_TEMPLATE_PATH, "*.py")),
    paths.TEMPLATES_PATH: glob.glob(os.path.join(_PROJECT_TEMPLATE_PATH, "*.tex")),
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

    cwd = os.getcwd()
    relative_paths_dir = os.path.split(_PATHS_FILE_FROM_PROJECT_ROOT)[0]
    paths_dir_from_project_root = os.path.join(path, relative_paths_dir)
    ensure_directory_exists(paths_dir_from_project_root)
    os.chdir(paths_dir_from_project_root)

    for directory, files in _TEMPLATE_STRUCTURE.items():
        dir_path = os.path.join(path, directory)
        ensure_directory_exists(dir_path)

        for file in files:
            shutil.copy(os.path.join(_PROJECT_TEMPLATE_PATH, file), dir_path)

    os.chdir(cwd)
