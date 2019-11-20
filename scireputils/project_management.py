import os
import shutil

_FILE_DIR = os.path.split(__file__)[0]
_TEMPLATE_PATH = os.path.join(_FILE_DIR, "report_template")


def ensure_directory_exists(path):
    if not os.path.isdir(path):
        os.mkdir(path)


def init_report_directory(path=""):
    if not path:
        path = os.getcwd()

    ensure_directory_exists(path)

    auxiliary_path = os.path.join(path, "auxiliary")
    classfiles_path = os.path.join(path, "classfiles")
    data_path = os.path.join(path, "data")
    figures_path = os.path.join(path, "figures")
    latex_path = os.path.join(path, "latex")
    output_path = os.path.join(path, "output")
    plots_path = os.path.join(path, "plots")
    raw_data_path = os.path.join(path, "raw_data")
    scripts_path = os.path.join(path, "scripts")
    templates_path = os.path.join(path, "templates")

    os.mkdir(auxiliary_path)
    os.mkdir(classfiles_path)
    os.mkdir(data_path)
    os.mkdir(figures_path)
    os.mkdir(latex_path)
    os.mkdir(output_path)
    os.mkdir(plots_path)
    os.mkdir(raw_data_path)
    os.mkdir(scripts_path)
    os.mkdir(templates_path)

    shutil.copy(os.path.join(_TEMPLATE_PATH, "makefile"), path)
    shutil.copy(os.path.join(_TEMPLATE_PATH, "project_wide.py"), scripts_path)
    shutil.copy(os.path.join(_TEMPLATE_PATH, "render.py"), scripts_path)
    shutil.copy(os.path.join(_TEMPLATE_PATH, "main.tex"), templates_path)
    shutil.copy(os.path.join(_TEMPLATE_PATH, "scirep.cls"), classfiles_path)
