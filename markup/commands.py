import markup.markup_parse as markup_parse
import markup.markup_tokenize as markup_tokenize
from markup.doc import *
import os
import re
from pathlib import Path


def _compile(file, j=0):
    os.chdir(Path(file).parent)
    tokens, info = markup_tokenize.tokenize(file)
    parsed = markup_parse.parse_markdown(tokens)
    if not 'file_type' in info:
        info['file_type'] = "terminal"
    if not 'output_module' in info:
        info['output_module'] = "markup.output"
    if not 'output' in info:
        info['output'] = file.replace(file.split(".")[-1], info["file_type"])
    if not "ignore" in info:
        print(f"{'  '*j}+ compiling {file}")
        add_to_doc(file, parsed, info['output'],
                 info['file_type'], info['output_module'], info)
    else:
        print(f"{'  '*j}+ processing {file}")
    if "use" in info:
        for pattern in info['use'].split(";"):
            for f in os.listdir():
                if re.search(pattern.strip(" "), f):
                    _compile(f, j+1)
