import click
import os
from markup.commands import _read, _compile, _output
from pathlib import Path


@click.command()
@click.argument('files', nargs=-1, required=True)
@click.option('--fileout/--stdout', help='The person to greet.', default=True)
@click.option('-v', '--verbose', count=True)
@click.option('-V', '--full-verbose', is_flag=True, default=False)
@click.option('--append-yaml', '-y', multiple=True)
@click.option('--output', '-o')
def compile(files, fileout, verbose, full_verbose, append_yaml, output):
    """Compiles docments using RMarkdown."""
    if full_verbose:
        verbose = 1000
    for file in files:
        if verbose >= 1:
            print(f"+ processing {file}")
        text = _read(file)
        os.chdir(Path(file).parent)
        append_yaml = "\n"+"\n".join(append_yaml)
        if append_yaml != "\n\n":
            append_yaml = ""
        text, yaml = _compile(text, verbose, append_yaml)
        if text != "":
            if fileout:
                _output(text, file, yaml)
            else:
                print(text)

def start():
    compile(obj={})


if __name__ == "__main__":
    start()
