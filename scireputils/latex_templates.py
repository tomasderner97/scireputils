import os

import jinja2


def render_template(template_path: str, output_path: str, **variables):
    template_dir, template_name = os.path.split(template_path)

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
    rendered = template.render(section1='Long Form', section2='Short Form')

    with open(output_path, "w+", encoding="utf-8") as out:
        out.write(rendered)
