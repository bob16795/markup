import markup
import os
import pytest
import tempfile
import re


def test_tokenize_symbols():
    text = "_`*+-#<>\t\n"
    tokens = markup.tokenize.tokenize(text, "", "", 0)[0]
    assert tokens.__str__() == '<type: UNDERSCORE, value: SYM><type: GRAVE, value: SYM><type: STAR, value: SYM><type: PLUS, value: SYM><type: MINUS, value: SYM><type: HASH, value: SYM><type: TAGO, value: SYM><type: TAGC, value: SYM><type: TAB, value: ><type: NEWLINE, value: ><type: NEWLINE, value: ><type: EOF, value: >'


def test_tokenize_numbers():
    text = "1a2b3c4d5e6f7g8h9i0j"
    tokens = markup.tokenize.tokenize(text, "", "", 0)[0]
    assert tokens.__str__() == '<type: NUM, value: 1><type: TEXT, value: a><type: NUM, value: 2><type: TEXT, value: b><type: NUM, value: 3><type: TEXT, value: c><type: NUM, value: 4><type: TEXT, value: d><type: NUM, value: 5><type: TEXT, value: e><type: NUM, value: 6><type: TEXT, value: f><type: NUM, value: 7><type: TEXT, value: g><type: NUM, value: 8><type: TEXT, value: h><type: NUM, value: 9><type: TEXT, value: i><type: NUM, value: 0><type: TEXT, value: j><type: NEWLINE, value: ><type: EOF, value: >'
