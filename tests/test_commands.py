import markup
import os
import pytest
import tempfile
import re


def test_read_file_include():
    output = markup.terminal.terminal(0)
    if os.name == "nt":
        tmp_master = tempfile.NamedTemporaryFile(
            dir="C:\\Users\\Preston.precourt\\Downloads", delete=False)
        tmp_master_name = "C:\\Users\\Preston.precourt\\Downloads\\" + \
            tempfile.gettempprefix() + tmp_master.name.split("\\tmp")[-1]
        tmp_inc = tempfile.NamedTemporaryFile(
            dir="C:\\Users\\Preston.precourt\\Downloads", delete=False)
        tmp_inc_name = tempfile.gettempprefix(
        ) + tmp_inc.name.split("\\tmp")[-1]
        tmp_inc_name = tmp_inc_name.replace("\\", "\\\\")
        os.chdir("C:\\Users\\Preston.precourt\\Downloads")
        tmp_master.write(("# lol\nInc: %s\n end" %
                          tmp_inc_name).encode("utf-8"))
        tmp_inc.write("this is tmp_inc file".encode("utf-8"))
        tmp_master.close()
        tmp_inc.close()
        read = markup.commands._read(tmp_master_name, output)
        for file in sorted(os.listdir("C:\\Users\\Preston.precourt\\Downloads\\")):
            if re.search("^tmp.", file):
                os.remove("C:\\Users\\Preston.precourt\\Downloads\\" + file)
        assert read == '# lol\n\n---\nslave: True\n---\nthis is tmp_inc file\n---\nslave: False\n--- end'
    else:
        tmp_master = tempfile.NamedTemporaryFile(
            dir="/tmp/", delete=False)
        tmp_master_name = "/tmp/" + \
            tempfile.gettempprefix() + tmp_master.name.split("/tmp")[-1]
        tmp_inc = tempfile.NamedTemporaryFile(
            dir="/tmp/", delete=False)
        tmp_inc_name = tempfile.gettempprefix(
        ) + tmp_inc.name.split("/tmp")[-1]
        os.chdir("/tmp/")
        tmp_master.write(("# lol\nInc: %s\n end" %
                          tmp_inc_name).encode("utf-8"))
        tmp_inc.write("this is tmp_inc file".encode("utf-8"))
        tmp_master.close()
        tmp_inc.close()
        read = markup.commands._read(tmp_master_name, output)
        for file in sorted(os.listdir("/tmp/")):
            if re.search("^tmp.", file):
                os.remove("/tmp/" + file)
        assert read == '# lol\n\n---\nslave: True\n---\nthis is tmp_inc file\n---\nslave: False\n--- end'


def test_cleanup_newlines():
    output = markup.terminal.terminal(0)
    file_cached = "\n" * 30
    file_cached = markup.commands._cleanup(file_cached, "test", output=output)
    assert file_cached == "\n\n"


def test_cleanup_spaces():
    output = markup.terminal.terminal(0)
    file_cached = "\n  \n    \n"
    file_cached = markup.commands._cleanup(file_cached, "test", output=output)
    assert file_cached == "\n\t\n\t\t\n"
    file_cached = "\n    \n        \n"
    file_cached = markup.commands._cleanup(
        file_cached, "test", tabs=4, output=output)
    assert file_cached == "\n\t\n\t\t\n"
