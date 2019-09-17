import markup
import os
import pytest
import tempfile
import re


def test_yaml_parser_format():
    yaml = "lol: nope\nfoo:      bar\nths:is_random\n nope : var"
    yaml_dict = markup.tokenize.yaml_dict(yaml)
    expected = {
        "lol": "nope",
        "foo": "bar",
        "ths": "is_random",
        "nope": "var",
        "slave": "False"
    }
    assert yaml_dict == expected


def test_tokenize_symbols():
    text = "_`*+-#<>[)\t\n"
    tokens = markup.tokenize.tokenize(text, "")[0]
    assert tokens.__str__() == '<type: UNDERSCORE, value: SYM><type: GRAVE, value: SYM><type: STAR, value: SYM><type: PLUS, value: SYM><type: MINUS, value: SYM><type: HASH, value: SYM><type: TAGO, value: SYM><type: TAGC, value: SYM><type: TAGO, value: SYM><type: TAGC, value: SYM><type: TAB, value: ><type: NEWLINE, value: ><type: NEWLINE, value: ><type: EOF, value: >'


def test_tokenize_newline():
    pass
