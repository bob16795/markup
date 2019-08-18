import click
import os
from markup.commands import _read, _compile, _output
from pathlib import Path


@click.command()
@click.argument('files', nargs=-1, required=True)
@click.option('--fileout/--stdout', help='The person to greet.', default=True)
@click.option('-v', '--verbose', count=True)
@click.option('-V', '--fullverbose', is_flag=True, default=False)
@click.option('--appendyaml', '-y', multiple=True)
@click.option('--output', '-o')
def compile(files, fileout, verbose, fullverbose, appendyaml, output):
    """Compiles docments using Markup."""
    if fullverbose:
        verbose = 1000
    for file in files:
        if verbose >= 1:
            print(f"+ processing {file}")
        text = _read(file)
        os.chdir(Path(file).parent)
        appendyaml = "\n"+"\n".join(appendyaml)
        if appendyaml != "\n\n":
            appendyaml = ""
        text, yaml = _compile(text, verbose, appendyaml)
        if text != "":
            if fileout:
                _output(text, file, yaml)
            else:
                print(text)

def start():
    compile(obj={})


if __name__ == "__main__":
    start()
