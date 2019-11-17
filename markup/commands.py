import markup.parser as parser
import markup.tokenize as tokenize
from markup.threading import multi_tasker
from markup.doc import add_to_doc
import os
import re
from pathlib import Path
import click
from markup.terminal import error, log, debug


def _read(file, output, inside=False):
    """
    reads a document and imports Inc: * files

    file: the file to start with
    inside: should always be false unless being called by anothrer document
    """

    output.add(debug, "commands.py: reading %s" % file)
    with open(file, encoding='utf-8') as filew:
        file_cached = ""
        for line in filew:
            if line.split(":")[0] == "Inc":
                for pattern in line[4:-1].split(";"):
                    pattern = pattern.strip(" ")
                    path = "./"
                    if "/" in file:
                        path = "/".join(file.strip(" ").split("/")[:-1])
                    if "/" in pattern:
                        path += "/".join(pattern.strip(" ").split("/")[:-1])
                        pattern = pattern.split("/")[-1]
                    for f in sorted(os.listdir(path)):
                        if re.search(pattern, f):
                            fpath = path + "/" + f
                            if inside:
                                file_cached = "%s%s\n" % (file_cached, _read(fpath, output, True))
                            else:
                                file_cached = "%s\n---\nslave: True\n---\n%s\n---\nslave: False\n---\n" % (file_cached, _read(fpath, output, True))
                file_cached = file_cached[:-1]
            elif line.split(":")[0] == "Tmp":
                cwd = os.getcwd()
                for pattern in line[4:-1].split(";"):
                    pattern = pattern.strip(" ")
                    if "/" in pattern:
                        os.chdir("/".join(pattern.split("/")[:-1]))
                        pattern = pattern.split("/")[-1]
                    for f in sorted(os.listdir()):
                        if re.search(pattern, f):
                            file_cached = "%s%s\n" % (file_cached, _read(fpath, output, True))
                    os.chdir(cwd)
                file_cached = file_cached[:-1]
            else:
                file_cached = "%s%s" % (file_cached, line)
    return file_cached


def _cleanup(file_cached, file_name, tabs=2, output=0):
    """
    unstupifies document for tokenization

    file_cached: the document to be unstupified
    """
    output.add(log, "cleaning %s" % file_name)
    while "\n\n\n" in file_cached:
        file_cached = file_cached.replace("\n\n\n", "\n\n")
    file_cached = file_cached.replace("---\n\n", "---\n")
    for l in range(3, 0, -1):
        file_cached = file_cached.replace("\n" + " "*l*tabs, "\n" + "\t"*l)
    return file_cached


def _compile(file_cached, output, prop, file_name="test", tree=False):
    """
    comples a srting using markup

    file_cached: the string to be compiled
    verbose:     verbosity of the parser
    prop:        the properties of the document
    tree:        will output the parser tree of the document
    """
    if "tab_to_spaces" in file_cached:
        file_cached = _cleanup(file_cached, file_name,
                               file_cached["tab_to_spaces"])
    else:
        file_cached = _cleanup(file_cached, file_name, output=output)
    tokens, prop = tokenize.tokenize(file_cached, file_name, prop, output)
    parsed = parser.parse_markdown(tokens)
    if tree:
        print(parsed)
        file_new = str(parsed)
    else:
        if not prop.get("ignore"):
            output.add(log, "creating text for %s" % file_name)
            file_new = add_to_doc(
                parsed,
                prop.get('file_type',     "terminal"),
                prop.get('output_module', "markup.output"),
                prop)
        else:
            file_new = ""
    if prop.get("use"):
        use = prop.get("use")
        multitasker = multi_tasker()
        for pattern in use.split(";"):
            path = "./"
            if "/" in pattern:
                path = "/".join(pattern.strip(" ").split("/")[:-1])
                pattern = pattern.split("/")[-1]
            for file in sorted(os.listdir(path)):
                if re.search(pattern.strip(" "), file):
                    output.add(log, "adding %s to queue" % file)
                    multitasker.add_to_queue(
                        (output, path + "/" + file, tree))
        output.add(log, "processing queue")
        multitasker.finish(output)
    return file_new, prop


def _output(bytes_out, file, prop, output):
    """
    writes a bytes object to a document

    bytes_out: the bytes to write
    file:      the file to write them to
    prop:      properties of the document
    """
    to = prop.get("output", file.replace(file.split(
        ".")[-1], prop.get("file_type", "terminal")))
    output.add(log, "writing %s" % to)
    with open(to, "wb+") as f:
        f.write(bytes_out)
