import markup.markup_parse as markup_parse
import markup.markup_tokenize as markup_tokenize
from markup.doc import *
import os
import re
from pathlib import Path


def _compile(file, j=0):
    os.chdir(Path(file).parent)
    print(f"{'  '*j}+ compiling {file}")
    tokens, info = markup_tokenize.tokenize(file)
    parsed = markup_parse.parse_markdown(tokens)
    if not 'file_type' in info:
        info['file_type'] = "terminal"
    if not 'output_module' in info:
        info['output_module'] = "markup.output"
    add_to_doc(file, parsed, info['output'],
               info['file_type'], info['output_module'])
    if "use" in info:
        for pattern in info['use'].split("; "):
            for f in os.listdir():
                if re.search(pattern, f):
                    try:
                        _compile(f, j+1)
                    except:
                        pass
