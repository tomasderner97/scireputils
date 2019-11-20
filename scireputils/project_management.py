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

    ensure_directory_exists(auxiliary_path)
    ensure_directory_exists(classfiles_path)
    ensure_directory_exists(data_path)
    ensure_directory_exists(figures_path)
    ensure_directory_exists(latex_path)
    ensure_directory_exists(output_path)
    ensure_directory_exists(plots_path)
    ensure_directory_exists(raw_data_path)
    ensure_directory_exists(scripts_path)
    ensure_directory_exists(templates_path)

    shutil.copy(os.path.join(_TEMPLATE_PATH, "makefile"), path)
    shutil.copy(os.path.join(_TEMPLATE_PATH, "project_wide.py"), scripts_path)
    shutil.copy(os.path.join(_TEMPLATE_PATH, "render.py"), scripts_path)
    shutil.copy(os.path.join(_TEMPLATE_PATH, "main.tex"), templates_path)
    shutil.copy(os.path.join(_TEMPLATE_PATH, "scirep.cls"), classfiles_path)
