import os
import subprocess
from collections import namedtuple

import jinja2
import numpy as np

from scireputils._dataframe_to_booktabs_table import _make_column_strings_equal_length
from scireputils._dataframe_to_booktabs_table import _make_formater_from_s_col_format_string
from scireputils._dataframe_to_booktabs_table import _parse_column_property

_LATEX_COMMAND = [
    "pdflatex",
    "-file-line-error",
    "-interaction=nonstopmode",
    "-synctex=1",
    "-output-format=pdf",
    "-output-directory=../output",
    "-aux-directory=../auxiliary",
    "-include-directory=../classfiles",
    "-include-directory=../latex",  # TODO think about keeping paths in project_wide.py
]

_OPEN_PDF_COMMAND = [
    "sumatrapdf",
]


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


def compile_latex_to_pdf(latex_path, pdf_path):
    """
    Compiles given latex file to pdf using pdflatex. Then opens the final pdf.
    Parameters
    ----------
    latex_path : str
        path to the latex .tex file
    pdf_path : str
        path to the resulting .pdf file or output directory (the name will be the same as the .tex file)

    """
    latex_dir, latex_name = os.path.split(latex_path)

    if os.path.isdir(pdf_path):
        latex_name_wo_ext = os.path.splitext(latex_name)[0]
        pdf_path = os.path.join(pdf_path, latex_name_wo_ext + ".pdf")

    subprocess.run(_LATEX_COMMAND + [latex_path])
    subprocess.run(_OPEN_PDF_COMMAND + [pdf_path])


def make_figure_float(figure_path, label, caption, position="h", caption_vspace=0):
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


def make_table_float(tabular_code,
                     label,
                     caption,
                     position="h",
                     tabcolsep=15,
                     caption_vspace=0,
                     external_table=False):
    """
    Creates a latex code string which includes a figure into the document.
    Result should be used as an argument of the render_template function.

    Parameters
    ----------
    tabular_code : str
        Code of the table of path to the table tex file, relative to the latex document, depending on external_table
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
    external_table : bool
        Is the table_code a link to external table?

    Returns
    -------
    Generated latex code

    """
    if external_table:
        return f"""
\\begin{{table}}[{position}]
    \\centering
    \\setlength{{\\tabcolsep}}{{{tabcolsep}pt}}
    \\input{{{tabular_code}}}
    \\vspace{{{caption_vspace}pt}}
    \\caption{{{caption}}}
    \\label{{tab:{label}}}
\\end{{table}}
"""
    else:
        return f"""
\\begin{{table}}[{position}]
    \\centering
    \\setlength{{\\tabcolsep}}{{{tabcolsep}pt}}
    {tabular_code}
    \\vspace{{{caption_vspace}pt}}
    \\caption{{{caption}}}
    \\label{{tab:{label}}}
\\end{{table}}
"""


def dataframe_to_booktabs_table(df, column_properties, file=None):
    """
    Parameters
    ----------
    df : pd.DataFrame
    column_properties : sequence of sequences of size 3 or 4
        description of columns. The inner sequences should be
        [
            name_of_col_in_df,
            optional_name_of_quantity,
            optional_unit,
            optional_S_col_fmt_str
        ]
        S column formater examples: 1.2, 4.3e1
    file : str
        path to file to save this in. Default is None - no saving

    Returns
    -------
    formated table with booktabs in latex code
    """

    columns = []
    col_types = []

    for cp in column_properties:

        col_name, quantity_name, unit, s_col_format = _parse_column_property(cp)

        if col_name == "index":
            from pandas import Series
            series = Series(df.index.values)
        else:
            series = df[col_name]
        s_column = series.dtype.name != "object"

        if s_column:
            col_type = f"S[table-format={s_col_format}]"
            col_types.append(col_type)
        else:
            col_types.append("l")

        float_format = _make_formater_from_s_col_format_string(
            s_col_format
        ) if s_col_format else None

        col_of_strings = series.to_string(
            index=False,
            float_format=float_format
        ).split("\n")

        if s_column:
            quantity_name = f"{{{quantity_name}}}"
            unit = f"{{{unit}}}"

        finished_column_list = _make_column_strings_equal_length(quantity_name, unit, col_of_strings)

        columns.append(finished_column_list)

    rows = zip(*columns)
    concatenated_rows = [" & ".join(r) + r" \\" for r in rows]

    concatenated_rows[1] += r" \midrule"
    concatenated_rows[-1] += r" \bottomrule"

    header = [r"\begin{tabular}[t]{"]
    for ct in col_types:
        header.append(f"  {ct}")
    header.append(r"} \toprule")

    footer = [r"\end{tabular}"]

    finished = "\n".join(header + concatenated_rows + footer)

    if file:
        with open(file, "w+", encoding="utf-8") as f:
            f.write(finished)

    return finished


_Column = namedtuple("Column", "values title unit format_str")
_SEPARATOR = "-"


class BooktabsTable:
    TABULAR_TEMPLATE = r"""
\begin{{tabular}}[t]{{
{column_definitions}
}}
\toprule
{head}
\midrule
{body}
\bottomrule
\end{tabular}
"""

    def __init__(self,
                 label,
                 caption,
                 position="h",
                 tabcolsep=15,
                 caption_vspace=0,):
                 # toprule_pos=None,
                 # midrule_pos=None,
                 # bottomrule_pos=None):
        """
        Represents a latex booktabs table.

        Parameters
        ----------
        label : str
            Table label without tab:, that is added automatically
        caption : str
            Table caption
        position : str
            The float position argument, such as 'h', 'b'...
        tabcolsep : int
            Separation distance between columns
        caption_vspace : int
            Adjusts the spacing between the figure and the caption, in pts
        toprule_pos : list, default [0,]
            Indices of rows over which toprule should be drawn
        midrule_pos : list, default [2,]
            Indices of rows over which midrule should be drawn
        bottomrule_pos : list, default [inf,]
            Indices of rows over which bottomrule should be drawn (inf means under last row)

        """
        self.columns = []
        self.label = label
        self.caption = caption
        self.position = position
        self.tabcolsep = tabcolsep
        self.caption_vspace = caption_vspace
        # self.toprule_pos = toprule_pos or [0, ]
        # self.midrule_pos = midrule_pos or [2, ]
        # self.bottomrule_pos = bottomrule_pos or [np.inf, ]

    def add_column(self, values, title="", unit="", format_str="1.1"):
        self.columns.append(_Column(values, title, unit, format_str))

    # def add_separator(self):
    #     self.columns.append(_SEPARATOR)

    def render(self):
        """
        Compiles the columns into a formatted tabular environment code and wraps it in a table environment.

        Returns
        -------
        Latex code for the table ready to be included in compilable .tex file
        """
        tabular = self._render_tabular()
        return f"""
        \\begin{{table}}[{self.position}]
            \\centering
            \\setlength{{\\tabcolsep}}{{{self.tabcolsep}pt}}
            {tabular}
            \\vspace{{{self.caption_vspace}pt}}
            \\caption{{{self.caption}}}
            \\label{{tab:{self.label}}}
        \\end{{table}}
        """

    def render_standalone(self, file_path, input_path):
        """
        Compiles the columns into a formatted tabular environment code and saves the code into a file.
        Then inputs the file into a table environment.

        Parameters
        ----------
        file_path : str
            Path to the tabular file relative to the python script
        input_path : str
            Path to the tabular file relative to the compilable latex file (the one that is compiled into .pdf)

        Returns
        -------
        Latex code of table environment wrapping input of external table file

        """
        tabular = self._render_tabular()
        with open(file_path, "w")as f:
            f.write(tabular)

        return f"""
        \\begin{{table}}[{self.position}]
            \\centering
            \\setlength{{\\tabcolsep}}{{{self.tabcolsep}pt}}
            \\input{{{input_path}}}
            \\vspace{{{self.caption_vspace}pt}}
            \\caption{{{self.caption}}}
            \\label{{tab:{self.label}}}
        \\end{{table}}
        """

    def _render_tabular(self):
        """
        This is a terrible hack using the function I had before to do the heavy lifting of actual table generation.
        I need to rewrite this.
        """
        column_dict = {}
        column_properties = []

        for i, col in enumerate(self.columns):
            column_dict[str(i)] = col.values
            column_properties = (str(i), col.title, col.unit, col.format_str)

        return dataframe_to_booktabs_table(column_dict, column_properties)


