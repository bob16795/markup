import markup
import os


def test_sentence_no_escape():
    compiling = "import lol\nlol.is_dir\n\\\\-+*lol\n"
    output, yaml = markup.commands._compile(
        compiling, False, "\n\n", tree=True)
    nodes = str(markup.nodes.BodyNode([
        markup.nodes.ParagraphNode([
            markup.nodes.Node("TEXT", "import lol lol.is_dir \\-+*lol", 11),
        ], 13)
    ], 13))
    assert output == nodes


def test_text_paragraphs_no_escape():
    compiling = "import lol\nlol.is_dir\n\\\\-+*lol\n\nimport lol\nlol.is_dir\n\\\\-+*lol\n"
    output, yaml = markup.commands._compile(
        compiling, False, "\n\n", tree=True)
    nodes = str(markup.nodes.BodyNode([
        markup.nodes.ParagraphNode([
            markup.nodes.Node("TEXT", "import lol lol.is_dir \\-+*lol", 11),
        ], 13),
        markup.nodes.ParagraphNode([
            markup.nodes.Node("TEXT", "import lol lol.is_dir \\-+*lol", 11),
        ], 13),
    ], 26))
    assert output == nodes
