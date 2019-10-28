import os
import re
from pathlib import Path

import click

from markup.commands import _compile, _output, _read
from markup.threading import multi_tasker


@click.command()
@click.argument('files', nargs=-1, required=True)
@click.option('--fileout/--stdout', help='Where to put the document.', default=True)
@click.option('--verbose', '-v', help='Incerases the annoyingness of the compiler.', count=True, default=1)
@click.option('--quiet', '-q', help='sets verbosity to zero.', default=False, is_flag=True)
@click.option('--fullverbose', '-V', help='sets verbose to 1000.', is_flag=True, default=False)
@click.option('--appendprop', '-p', help='append property to document.', multiple=True, is_flag=True)
@click.option('--output', '-o', help='forces output to a file.')
@click.option('--tree', '-t', help='prints a parser tree for the document.', is_flag=True)
def compile(files, fileout, verbose, quiet, fullverbose, appendprop, output, tree):
    """Compiles docments using Markup."""
    if quiet or tree:
        verbose = 0
    if fullverbose:
        verbose = 1000
    # for file in files:
    #     if verbose >= 1:
    #         click.echo(f"started {file}")
    #     try:
    #         text = _read(file)
    #     except FileNotFoundError:
    #         click.echo(f"file not found {file}")
    #         quit()
    #     os.chdir(Path(file).parent)
    #     appendprop = "\n"+"\n".join(appendprop)
    #     if appendprop != "\n\n":
    #         appendprop = ""
    #     text, prop = _compile(text, verbose, appendprop, file, tree=tree)
    #     if not tree:
    #         if text != "":
    #             if fileout:
    #                 _output(text, file, prop, verbose)
    #             else:
    #                 click.echo(text)
    multitasker = multi_tasker()
    for pattern in files:
        path = "./"
        if "/" in pattern:
            path = "/".join(pattern.strip(" ").split("/")[:-1])
            pattern = pattern.split("/")[-1]
        for file in sorted(os.listdir(path)):
            if re.search(pattern.strip(" "), file):
                if verbose >= 2:
                    click.echo(f"adding {file} to queue")
                multitasker.add_to_queue((verbose, {}, path + "/" + file, tree))
    if verbose >= 2:
        click.echo(f"processing queue")
    multitasker.finish(verbose)

def start():
    compile(obj={})


if __name__ == "__main__":
    start()
