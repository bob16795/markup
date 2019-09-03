import markup
import os

def test_code_no_escape():
    compiling = "import lol\nlol.is_dir\n\\\\-+*lol\n\nimport lol\nlol.is_dir\n\\\\-+*lol\n"
    output, yaml = markup.commands._compile(compiling, False, "\n\n", tree=True)
    nodes = str(markup.nodes.BodyNode([
      markup.nodes.ParagraphNode([
        markup.nodes.Node("TEXT", "import lol", 1),
        markup.nodes.Node("TEXT", " ", 1),
        markup.nodes.Node("TEXT", "lol.is", 1),
        markup.nodes.Node("TEXT", "_", 1),
        markup.nodes.Node("TEXT", "dir", 1),
        markup.nodes.Node("TEXT", " ", 1),
        markup.nodes.Node("TEXT", "\\", 1),
        markup.nodes.Node("TEXT", "-", 1),
        markup.nodes.Node("TEXT", "+", 1),
        markup.nodes.Node("TEXT", "*", 1),
        markup.nodes.Node("TEXT", "lol", 1),
      ], 13),
      markup.nodes.ParagraphNode([
        markup.nodes.Node("TEXT", "import lol", 1),
        markup.nodes.Node("TEXT", " ", 1),
        markup.nodes.Node("TEXT", "lol.is", 1),
        markup.nodes.Node("TEXT", "_", 1),
        markup.nodes.Node("TEXT", "dir", 1),
        markup.nodes.Node("TEXT", " ", 1),
        markup.nodes.Node("TEXT", "\\", 1),
        markup.nodes.Node("TEXT", "-", 1),
        markup.nodes.Node("TEXT", "+", 1),
        markup.nodes.Node("TEXT", "*", 1),
        markup.nodes.Node("TEXT", "lol", 1),
      ], 13),
    ], 26))
    assert output == nodes