import os

from project_wide import TEMPLATES_PATH, LATEX_PATH, OUTPUT_PATH
from scireputils.latex_templates import render_template, compile_latex_to_pdf

template_params = {

}

TEMPLATE_PATH = os.path.join(TEMPLATES_PATH, "main.tex")
LATEX_OUT_PATH = os.path.join(LATEX_PATH, "main.tex")
PDF_PATH = os.path.join(OUTPUT_PATH, "main.pdf")

render_template(TEMPLATE_PATH,
                LATEX_OUT_PATH,
                )
compile_latex_to_pdf(LATEX_OUT_PATH,
                     PDF_PATH)
