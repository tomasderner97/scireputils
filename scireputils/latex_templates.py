import os

import jinja2

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
    loader=jinja2.FileSystemLoader(os.path.abspath('.'))
)


def render_template(template_path: str, output_path: str, **variables):
    template = latex_jinja_env.get_template(template_path)
    rendered = template.render(section1='Long Form', section2='Short Form')

    with open(output_path, "w+") as out:
        out.write(rendered)
