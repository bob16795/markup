import click
import os
import sys
import re
import subprocess
import time
from markup.commands import _compile
from pathlib import Path


@click.command()
@click.argument('files', nargs=-1, required=True)
def compile(files):
    """Compiles docments using RMarkdown."""
    for file in files:
        _compile(file)


def start():
    compile(obj={})


if __name__ == "__main__":
    start()
