import markup
import os


def test_headings_nl2():
    compiling = "# lol\n\nlol"
    output, yaml = markup.commands._compile(compiling, False, "", tree=True)
    nodes = str(markup.nodes.BodyNode([
        markup.nodes.HeadNode("HEAD1", " lol", 4),
        markup.nodes.ParagraphNode([
            markup.nodes.Node("TEXT", "lol", 1),
            markup.nodes.Node("TEXT", " ", 1)
        ], 3)
    ], 7))
    assert output == nodes


def test_headings_nl1():
    compiling = "# lol\nlol"
    output, yaml = markup.commands._compile(
        compiling, False, "\n\n", tree=True)
    nodes = str(markup.nodes.BodyNode([
        markup.nodes.HeadNode("HEAD1", " lol", 3),
        markup.nodes.ParagraphNode([
            markup.nodes.Node("TEXT", "lol", 1),
            markup.nodes.Node("TEXT", " ", 1)
        ], 3)
    ], 6))
    assert output == nodes
