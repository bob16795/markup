import os
import re
from pathlib import Path

import click

from markup.commands import _compile, _output, _read
from markup.threading import multi_tasker
from markup.terminal import terminal, log, error


@click.command()
@click.argument('files', nargs=-1, required=True)
@click.option('--fileout/--stdout', help='Where to put the document.', default=True)
@click.option('--verbose', '-v', help='Incerases the annoyingness of the compiler.', count=True, default=2)
@click.option('--quiet', '-q', help='sets verbosity to zero.', default=False, is_flag=True)
@click.option('--fullverbose', '-V', help='sets verbose to 1000.', is_flag=True, default=False)
@click.option('--appendprop', '-p', help='append property to document.', multiple=True)
@click.option('--output', '-o', help='forces output to a file.')
@click.option('--tree', '-t', help='prints a parser tree for the document.', is_flag=True)
def compile(files, fileout, verbose, quiet, fullverbose, appendprop, output, tree):
    """Compiles docments using Markup."""
    if quiet or tree:
        verbose = 0
    if fullverbose:
        verbose = 1000
    output = terminal(verbose)
    multitasker = multi_tasker()
    for pattern in files:
        path = "./"
        if "/" in pattern:
            path = "/".join(pattern.strip(" ").split("/")[:-1])
            pattern = pattern.split("/")[-1]
        found = False
        for file in sorted(os.listdir(path)):
            if pattern.strip(" ") == file:
                output.add(log, f"adding {file} to queue")
                multitasker.add_to_queue(
                    (output, path + "/" + file, tree))
                found = True
        if not found:
            output.add(error, f"file not found {pattern}")
    output.add(log, f"processing queue")
    multitasker.finish(output)


def start():
    compile(obj={})


if __name__ == "__main__":
    start()
