import os
from markup.commands import _read, _compile, _output
from pathlib import Path

def compile(files, fileout, verbose, fullverbose, appendyaml, output, tree):
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
        text, yaml = _compile(text, verbose, appendyaml, tree=tree)
        if not tree:
            if text != "":
                if fileout:
                    _output(text, file, yaml)
                else:
                    print(text)
