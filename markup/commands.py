import markup.parse as parse
import markup.tokenize as tokenize
from markup.doc import add_to_doc
import os
import re

def _read(file, inside=False):
    with open(file, encoding='utf-8') as filew:
        file_cached = ""
        for line in filew:
            if line[:5] == "Inc: ":
                cwd = os.getcwd()
                for pattern in line[5:-1].split(";"):
                    if "/" in pattern:
                        os.chdir("/".join(pattern.split("/")[:-1]))
                        pattern = pattern.split("/")[-1]
                    for f in sorted(os.listdir()):
                        if re.search(pattern.strip(" "), f):
                            if inside:
                                file_cached = f"{file_cached}{_read(f, True)}\n"
                            else:
                                file_cached = f"{file_cached}\n---\nslave: True\n---\n{_read(f, True)}\n---\nslave: False\n---\n"
                    os.chdir(cwd)
                file_cached = file_cached[:-1]
            else:
                file_cached = f"{file_cached}{line}"
    while "\n\n\n" in file_cached:
        file_cached = file_cached.replace("\n\n\n", "\n\n")
    return file_cached
 

def _compile(file_cached, verbose, yaml, j=1, tree=False):
    if verbose >= 3:
        print(f"{'  '*j}- tokenizing")
    tokens, info = tokenize.tokenize(file_cached, yaml)
    parsed = parse.parse_markdown(tokens)
    if tree:
        print(parsed)
        file_new = str(parsed)
    else:
        if not 'file_type' in info:
            info['file_type'] = "terminal"
        if not 'output_module' in info:
            info['output_module'] = "markup.output"
        if not "ignore" in info:
            if verbose >= 3:
                print(f"{'  '*j}- creating text")
            file_new = add_to_doc(parsed, info['file_type'], info['output_module'], info)
        else:
            file_new = ""
    if "use" in info:
        cwd = os.getcwd()
        for pattern in info['use'].split(";"):
            if "/" in pattern:
                os.chdir("/".join(pattern.split("/")[:-1]))
                pattern = pattern.split("/")[-1]
            for file in sorted(os.listdir()):
                if re.search(pattern.strip(" "), file):
                    if verbose >= 2:
                        print(f"{'  '*j}+ processing {file}")
                    text = _read(file)
                    text, yaml = _compile(text, verbose, "", j+1, tree)
                    if not tree:
                        if text != "":
                            _output(text, file, yaml)
            os.chdir(cwd)
    return file_new, info

def _output(file_cached, file, yaml):
    to = file.replace(file.split(".")[-1], yaml["file_type"])
    if "output" in yaml:
        to = yaml["output"]
    with open(to , "wb") as f:
        f.write(file_cached)
