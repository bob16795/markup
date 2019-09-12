import markup
import os


def test_code_no_escape():
    compiling = "```python\nimport lol\nlol.is_dir\n\\\\-+*\n```"
    output, yaml = markup.commands._compile(
        compiling, False, "\n\n", tree=True)
    nodes = str(markup.nodes.BodyNode([
        markup.nodes.CodeNode([
            markup.nodes.Node("TEXT", "import lol", 1),
            markup.nodes.Node("TEXT", "lol.is_dir", 3),
            markup.nodes.Node("TEXT", "\\-+*", 4),
            markup.nodes.Node("TEXT", "", 0),
        ], 21),
    ], 21))
    assert output == nodes
