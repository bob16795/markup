import click
import click.testing
import markup
import os
import pytest
import tempfile


def test_file_not_found():
    runner = click.testing.CliRunner()
    result = runner.invoke(markup.cli.compile, ['this_is_a_file.mu'])
    assert result.exit_code == 1
    assert result.output != ''


def test_file_is_directory():
    runner = click.testing.CliRunner()
    with runner.isolated_filesystem():
        os.mkdir("folder")
        result = runner.invoke(markup.cli.compile, ['folder'])
        assert result.exit_code == 1
        assert result.output != ''


def test_multi_file():
    runner = click.testing.CliRunner()
    with runner.isolated_filesystem():
        with open('main.mu', 'w') as f:
            f.write('Hello World!')
        with open('dual.mu', 'w') as f:
            f.write('Hello World2!')
        result = runner.invoke(markup.cli.compile, ['main.mu', 'dual.mu'])
        assert result.exit_code == 0
        assert result.output != ''
