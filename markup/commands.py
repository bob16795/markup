import markup.parse as parse
import markup.tokenize as tokenize
from markup.doc import add_to_doc
import os
import re
from pathlib import Path
import threading
import logging
class compiler():
  def __init__(self, conc = 4):
    self.threads = list()
    self.index = 0
    self.b = threading.Barrier(conc)

  def add_to_queue(self, args):
    logging.info("Main    : create and start thread %d.", self.index)
    x = threading.Thread(target=self.compile, args=args)
    self.threads.append(x)

  @staticmethod
  def compile(verbose, prop, file, j=1, tree=False):
    path = "./"
    if "/" in file:
        path = "/".join(file.strip(" ").split("/")[:-1])
    if verbose >= 2:
        print(f"{'  '*j}+ processing {file}")
    text = _read(file)
    text, prop_slave = _compile(
        text, verbose, "", file, j+1, tree)
    if not tree:
        if text != "":
            _output(text, file, prop_slave)
            if verbose >= 3:
                print(f"{'  '*(j+1)}- writing {file}")
  
  def finish(self):
    for index, thread in enumerate(self.threads):
      thread.start()
    for thread in self.threads:
      thread.join()
    self.threads = list()

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
                            fpath = path + "/" +f
                            if inside:
                                file_cached = f"{file_cached}{_read(fpath, True)}\n"
                            else:
                                file_cached = f"{file_cached}\n---\nslave: True\n---\n{_read(fpath, True)}\n---\nslave: False\n---\n"
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
                            file_cached = f"{file_cached}{_read(f, True)}\n"
                    os.chdir(cwd)
                file_cached = file_cached[:-1]
            else:
                file_cached = f"{file_cached}{line}"
    return file_cached


def _cleanup(file_cached, tabs=2):
    """
    unstupifies document for tokenization

    file_cached: the document to be unstupified
    """
    while "\n\n\n" in file_cached:
        file_cached = file_cached.replace("\n\n\n", "\n\n")
    file_cached = file_cached.replace("---\n\n", "---\n")
    for l in range(3, 0, -1):
        file_cached = file_cached.replace("\n" + " "*l*tabs, "\n" + "\t"*l)
    return file_cached


def _compile(file_cached, verbose, prop, file_name="test", j=1, tree=False):
    """
    comples a srting using markup

    file_cached: the string to be compiled
    verbose:     verbosity of the parser
    prop:        the properties of the document
    j:           the level of the document
    tree:        will output the parser tree of the document
    """
    if verbose >= 3:
        print(f"{'  '*j}- cleaning {file_name}")
    if "tab_to_spaces" in file_cached:
        file_cached = _cleanup(file_cached, file_cached["tab_to_spaces"])
    else:
        file_cached = _cleanup(file_cached)
    if verbose >= 3:
        print(f"{'  '*j}- tokenizing")
    tokens, prop = tokenize.tokenize(file_cached, prop)
    parsed = parse.parse_markdown(tokens)
    if tree:
        print(parsed)
        file_new = str(parsed)
    else:
        if not prop.get("ignore"):
            if verbose >= 3:
                print(f"{'  '*j}- creating text")
            file_new = add_to_doc(
                parsed,
                prop.get('file_type',     "terminal"),
                prop.get('output_module', "markup.output"),
                prop)
        else:
            file_new = ""
    if prop.get("use"):
        cwd = os.getcwd()
        use = prop.get("use")
        multitasker = compiler()
        for pattern in use.split(";"):
            path = "./"
            if "/" in pattern:
                path = "/".join(pattern.strip(" ").split("/")[:-1])
                pattern = pattern.split("/")[-1]
            for file in sorted(os.listdir(path)):
                if re.search(pattern.strip(" "), file):
                    if verbose >= 3:
                        print(f"{'  '*j}- adding {file}")
                    multitasker.add_to_queue((verbose, prop, path + "/" + file, j, tree))
        multitasker.finish()
    return file_new, prop

def _output(bytes_out, file, prop):
    """
    writes a bytes object to a document

    bytes_out: the bytes to write
    file:      the file to write them to
    prop:      properties of the document
    """
    to = prop.get("output", file.replace(file.split(".")[-1], prop.get("file_type", "terminal")))
    with open(to, "wb+") as f:
        f.write(bytes_out)
