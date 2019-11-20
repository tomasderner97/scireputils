import os

import jinja2


def render_template(template_path: str, output_path: str, **variables):
    """
    Renders a latex template into a compilable latex file.

    Parameters
    ----------
    template_path : str
        Path to the template
    output_path : str
        Destination of the rendered latex file, if only a directory is given, the name will be the same
        as the template
    variables : dict
        Variables for the template
    """
    template_dir, template_name = os.path.split(template_path)

    if os.path.isdir(output_path):
        output_path = os.path.join(output_path, template_name)

    latex_jinja_env = jinja2.Environment(
        block_start_string=r'\BLOCK{',
        block_end_string='}',
        variable_start_string=r'\VAR{',
        variable_end_string='}',
        comment_start_string=r'\#{',
        comment_end_string='}',
        line_statement_prefix='%%',
        line_comment_prefix='%#',
        trim_blocks=True,
        autoescape=False,
        loader=jinja2.FileSystemLoader(os.path.abspath(template_dir))
    )

    template = latex_jinja_env.get_template(template_name)
    rendered = template.render(section1='Long Form', section2='Short Form', **variables)

    with open(output_path, "w+", encoding="utf-8") as out:
        out.write(rendered)


def make_figure_float(figure_path, caption, label, position="h", caption_vspace=0):
    """
    Creates a latex code string which includes a figure into the document.
    Result should be used as an argument of the render_template function.

    Parameters
    ----------
    figure_path : str
        Path to the figure file, relative to the graphicspath of the graphicx package
    caption : str
        Figure caption
    label : str
        Figure label without fig:, that is added automatically
    position : str
        The float position argument, such as 'h', 'b'...
    caption_vspace : int
        Adjusts the spacing between the figure and the caption, in pts

    Returns
    -------
    Generated latex code

    """
    return f"""
\\begin{{figure}}[{position}]
    \\centering
    \\includegraphics{{{figure_path}}}
    \\vspace{{{caption_vspace}pt}}
    \\caption{{{caption}}}
    \\label{{fig:{label}}}
\\end{{figure}}
"""


def make_table_float(table_code_path, caption, label, position="h", tabcolsep=15, caption_vspace=0):
    """
    Creates a latex code string which includes a figure into the document.
    Result should be used as an argument of the render_template function.

    Parameters
    ----------
    table_code_path : str
        Path to the table tex file, relative to the latex document
        Used for
    caption : str
        Table caption
    label : str
        Table label without tab:, that is added automatically
    position : str
        The float position argument, such as 'h', 'b'...
    tabcolsep : int
        Separation distance between columns
    caption_vspace : int
        Adjusts the spacing between the figure and the caption, in pts

    Returns
    -------
    Generated latex code

    """
    return f"""
\\begin{{table}}[{position}]
    \\centering
    \\setlength{{\\tabcolsep}}{{{tabcolsep}pt}}
    \\input{{{table_code_path}}}
    \\vspace{{{caption_vspace}pt}}
    \\caption{{{caption}}}
    \\label{{tab:{label}}}
\\end{{table}}
"""


class Table:

    def __init__(self):
        pass
