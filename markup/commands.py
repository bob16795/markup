import markup.parse as parse
import markup.tokenize as tokenize
from markup.doc import add_to_doc
import os
import re


def _read(file, inside=False):
    """
    reads a document and imports Inc: * files

    file: the file to start with
    inside: should always be false unless being called by anothrer document
    """
    with open(file, encoding='utf-8') as filew:
        file_cached = ""
        for line in filew:
            if line.split(":")[0] == "Inc":
                cwd = os.getcwd()
                for pattern in line[4:-1].split(";"):
                    pattern = pattern.strip(" ")
                    if "/" in pattern:
                        os.chdir("/".join(pattern.split("/")[:-1]))
                        pattern = pattern.split("/")[-1]
                    for f in sorted(os.listdir()):
                        if re.search(pattern, f):
                            if inside:
                                file_cached = f"{file_cached}{_read(f, True)}\n"
                            else:
                                file_cached = f"{file_cached}\n---\nslave: True\n---\n{_read(f, True)}\n---\nslave: False\n---\n"
                    os.chdir(cwd)
                file_cached = file_cached[:-1]
            else:
                file_cached = f"{file_cached}{line}"
    return file_cached


def _cleanup(file_cached):
    """
    unstupifies document for tokenization

    file_cached: the document to be unstupified
    """
    while "\n\n\n" in file_cached:
        file_cached = file_cached.replace("\n\n\n", "\n\n")
    file_cached = file_cached.replace("---\n\n", "---\n")
    for l in range(3, 0, -1):
        file_cached = file_cached.replace("\n" + "  "*l, "\n" + "\t"*l)
    # TODO find a way that works
    return file_cached


def _compile(file_cached, verbose, prop, j=1, tree=False):
    """
    comples a srting using markup

    file_cached: the string to be compiled
    verbose:     verbosity of the parser
    prop:        the properties of the document
    j:           the level of the document
    tree:        will output the parser tree of the document
    """
    file_cached = _cleanup(file_cached)
    if verbose >= 3:
        print(f"{'  '*j}- tokenizing")
    tokens, prop = tokenize.tokenize(file_cached, prop)
    parsed = parse.parse_markdown(tokens)
    if tree:
        print(parsed)
        file_new = str(parsed)
    else:
        if not 'file_type' in prop:
            prop['file_type'] = "terminal"
        if not 'output_module' in prop:
            prop['output_module'] = "markup.output"
        if not "ignore" in prop:
            if verbose >= 3:
                print(f"{'  '*j}- creating text")
            file_new = add_to_doc(
                parsed, prop['file_type'], prop['output_module'], prop)
        else:
            file_new = ""
    if "use" in prop:
        cwd = os.getcwd()
        for pattern in prop['use'].split(";"):
            if "/" in pattern:
                os.chdir("/".join(pattern.split("/")[:-1]))
                pattern = pattern.split("/")[-1]
            for file in sorted(os.listdir()):
                if re.search(pattern.strip(" "), file):
                    if verbose >= 2:
                        print(f"{'  '*j}+ processing {file}")
                    text = _read(file)
                    text, prop_slave = _compile(text, verbose, "", j+1, tree)
                    if not tree:
                        if text != "":
                            _output(text, file, prop_slave)
            os.chdir(cwd)
    return file_new, prop


def _output(bytes_out, file, prop):
    """
    writes a bytes object to a document

    bytes_out: the bytes to write
    file:      the file to write them to
    prop:      properties of the document
    """
    to = file.replace(file.split(".")[-1], prop["file_type"])
    if "output" in prop:
        to = prop["output"]
    with open(to, "wb+") as f:
        f.write(bytes_out)
