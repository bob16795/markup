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
    while "\n\n\n" in file_cached:
        file_cached = file_cached.replace("\n\n\n", "\n\n")
    file_cached = file_cached.replace("---\n\n", "---\n")
    # TODO find a better way
    file_cached = file_cached.split("\n")
    curtabs_num = 0
    cur_tabs = 0
    tab_sizes = []
    for i, line in enumerate(file_cached):
        line_tabs = len(line) - len(line.strip(" "))
        if line_tabs > cur_tabs:
            tab_sizes.append(line_tabs)
            curtabs_num += 1
        if line_tabs < cur_tabs:
            curtabs_num = 0
            for i, size in enumerate(tab_sizes):
                if size == line_tabs:
                    curtabs_num = i
            tab_sizes = tab_sizes[:curtabs_num]
        if curtabs_num != 0:
            file_cached[i] = ("\t"*curtabs_num) + line.strip(" ")
        cur_tabs = line_tabs
    return "\n".join(file_cached)


def _compile(file_cached, verbose, prop, j=1, tree=False):
    """
    comples a srting using markup

    file_cached: the string to be compiled
    verbose:     verbosity of the parser
    prop:        the properties of the document
    j:           the level of the document
    tree:        will output the parser tree of the document
    """
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
