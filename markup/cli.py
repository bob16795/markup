import click
import os
from markup.commands import _read, _compile, _output
from pathlib import Path


@click.command()
@click.argument('files', nargs=-1, required=True)
@click.option('--fileout/--stdout', help='Where to put the document.', default=True)
@click.option('--verbose', '-v', help='Incerases the annoyingness of the compiler.', count=True, default=2)
@click.option('--quiet', '-q', help='sets verbosity to zero.', default=False, is_flag=True)
@click.option('--fullverbose', '-V', help='sets verbose to 1000.', is_flag=True, default=False)
@click.option('--appendprop', '-p', help='append property to document.', multiple=True, is_flag=True)
@click.option('--output', '-o', help='forces output to a file.')
@click.option('--tree', '-t', help='prints a parser tree for the document.', is_flag=True)
def compile(files, fileout, verbose, quiet, fullverbose, appendprop, output, tree):
    """Compiles docments using Markup."""
    if quiet:
        verbose = 0
    if fullverbose:
        verbose = 1000
    for file in files:
        if verbose >= 1:
            print(f"+ processing {file}")
        try:
            text = _read(file)
        except FileNotFoundError as error:
            print(f"+ file not found {file}")
            quit()
        os.chdir(Path(file).parent)
        appendprop = "\n"+"\n".join(appendprop)
        if appendprop != "\n\n":
            appendprop = ""
        text, prop = _compile(text, verbose, appendprop, file, tree=tree)
        if not tree:
            if text != "":
                if fileout:
                    _output(text, file, prop)
                    if verbose >= 3:
                        print(f"  - writing {file}")
                else:
                    print(text)


def start():
    compile(obj={})


if __name__ == "__main__":
    start()
