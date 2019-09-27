import markup
import os
import pytest


def test_compile_args_stdout():
    with pytest.raises(FileNotFoundError):
        markup.cli.compile(["lol.mu"])

