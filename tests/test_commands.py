import markup
import os
import pytest
import tempfile
import re
import click


def test_read_file_include():
    output = markup.terminal.terminal(0)
    runner = click.testing.CliRunner()
    with runner.isolated_filesystem():
        tmp_master = open("tmp_master.mu", "wb+")
        tmp_inc = open("tmp_inc.mu", "wb+")
        tmp_master_name = "tmp_master.mu"
        tmp_inc_name = "tmp_inc.mu"
        tmp_master.write(("# lol\nInc: %s\n end" %
                          tmp_inc_name).encode("utf-8"))
        tmp_inc.write("this is tmp_inc file".encode("utf-8"))
        tmp_master.close()
        tmp_inc.close()
        read = markup.commands._read(tmp_master_name, output)
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
