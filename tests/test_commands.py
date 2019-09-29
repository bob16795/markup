import markup
import os
import pytest
import tempfile
import re


def test_read_file_include():
    tmp_master = tempfile.NamedTemporaryFile(
        dir="C:\\Users\\Preston.precourt\\Downloads", delete=False)
    tmp_master_name = "C:\\Users\\Preston.precourt\\Downloads\\" + \
        tempfile.gettempprefix() + tmp_master.name.split("\\tmp")[-1]
    tmp_inc = tempfile.NamedTemporaryFile(
        dir="C:\\Users\\Preston.precourt\\Downloads", delete=False)
    tmp_inc_name = tempfile.gettempprefix() + tmp_inc.name.split("\\tmp")[-1]
    tmp_inc_name = tmp_inc_name.replace("\\", "\\\\")
    os.chdir("C:\\Users\\Preston.precourt\\Downloads")
    tmp_master.write(f"# lol\nInc: {tmp_inc_name}\n end".encode("utf-8"))
    tmp_inc.write("this is tmp_inc file".encode("utf-8"))
    tmp_master.close()
    tmp_inc.close()
    read = markup.commands._read(tmp_master_name)
    for file in sorted(os.listdir("C:\\Users\\Preston.precourt\\Downloads\\")):
        if re.search("^tmp.", file):
            os.remove("C:\\Users\\Preston.precourt\\Downloads\\" + file)
    assert read == '# lol\n\n---\nslave: True\n---\nthis is tmp_inc file\n---\nslave: False\n--- end'

