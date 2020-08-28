import os

from .meta import load_metadata_from_folder

from jinja2 import Environment, PackageLoader, select_autoescape
html_env = Environment(
    loader=PackageLoader('eurec4a', os.path.join('templates', 'html')),
    autoescape=select_autoescape(['html', 'xml'])
)

tex_env = Environment(
    block_start_string='\BLOCK{',
    block_end_string='}',
    variable_start_string='\VAR{',
    variable_end_string='}',
    comment_start_string='\#{',
    comment_end_string='}',
    line_statement_prefix='%%',
    line_comment_prefix='%#',
    trim_blocks=True,
    autoescape=False,
    loader=PackageLoader('eurec4a', os.path.join('templates', 'tex')),
)

def render_instruments(metadata, output_folder):
    instruments = [e for e in metadata.values() if e["type"] == "instrument"]
    print(instruments)
    tpl = html_env.get_template("instruments.html")
    with open(os.path.join(output_folder, "instruments.html"), "w") as outfile:
        outfile.write(tpl.render(objects=metadata,
                                 instruments=instruments))

def render_tex_instruments(metadata, output_folder):
    instruments = [e for e in metadata.values() if e["type"] == "instrument"]
    print(instruments)
    tpl = tex_env.get_template("instruments.tex")
    with open(os.path.join(output_folder, "instruments.tex"), "w") as outfile:
        outfile.write(tpl.render(objects=metadata,
                                 instruments=instruments))

def _main():
    import argparse

    default_metadata_folder = os.path.join(os.path.dirname(__file__), "..", "..", "metadata")

    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output_folder", type=str, default=".")
    parser.add_argument("-m", "--metadata_folder", type=str, default=default_metadata_folder)
    args = parser.parse_args()

    metadata = load_metadata_from_folder(args.metadata_folder)

    render_instruments(metadata, args.output_folder)
    render_tex_instruments(metadata, args.output_folder)
    

if __name__ == "__main__":
    _main()