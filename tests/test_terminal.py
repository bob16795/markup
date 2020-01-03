import click
import click.testing
import markup
import os
import pytest
import tempfile


def test_error_quit():
    output = markup.terminal.terminal(0)
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        output.add(markup.terminal.error, "This is an Error")
    assert pytest_wrapped_e.type == SystemExit


def test_error():
    error = markup.terminal.error("This is an Error")
    error, code = error.report()
    assert error == click.style("ERROR: This is an Error", fg='red', bold=True)
    assert code == 0


def test_warn():
    warn = markup.terminal.warn("This is a Warning")
    warn, code = warn.report()
    assert warn == click.style(
        "WARNING: This is a Warning", fg='red')
    assert code == 1


def test_log():
    log = markup.terminal.log("This is a log")
    log, code = log.report()
    assert log == "LOG: This is a log"
    assert code == 2


def test_info():
    info = markup.terminal.info("This is information")
    info, code = info.report()
    assert info == "INFO: This is information"
    assert code == 3


def test_debug():
    debug = markup.terminal.debug("test_terminal.py: This is debug")
    debug, code = debug.report()
    assert debug == "DEBUG test_terminal.py: This is debug"
    assert code == 4
