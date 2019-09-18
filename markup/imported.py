import os
from markup.commands import _read, _compile, _output
from pathlib import Path

def compile(files, fileout, verbose, fullverbose, appendprop, output, tree):
    """Compiles docments using Markup."""
    if fullverbose:
        verbose = 1000
    for file in files:
        if verbose >= 1:
            print(f"+ processing {file}")
        text = _read(file)
        os.chdir(Path(file).parent)
        appendprop = "\n"+"\n".join(appendprop)
        if appendprop != "\n\n":
            appendprop = ""
        text, prop = _compile(text, verbose, appendprop, tree=tree)
        if not tree:
            if text != "":
                if fileout:
                    _output(text, file, prop)
                else:
                    print(text)
