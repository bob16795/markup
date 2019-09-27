import markup
import os


def test_code_no_escape():
    compiling = "```python\nimport lol\nlol.is_dir\n\\\\-+*\n```"
    output, prop = markup.commands._compile(
        compiling, False, "\n\n", tree=True)
    nodes = str(markup.nodes.BodyNode([
        markup.nodes.CodeNode([
            markup.nodes.Node("TEXT", "import lol", 1),
            markup.nodes.Node("TEXT", "lol.is_dir", 3),
            markup.nodes.Node("TEXT", "\\-+*", 4),
            markup.nodes.Node("TEXT", "", 0),
        ], 21, "python"),
    ], 21))
    assert output == nodes


def test_headings_nl2():
    compiling = "# lol\n\nlol"
    output, prop = markup.commands._compile(compiling, False, "", tree=True)
    nodes = str(markup.nodes.BodyNode([
        markup.nodes.HeadNode("HEAD1", " lol", 4),
        markup.nodes.ParagraphNode([
            markup.nodes.Node("TEXT", "lol", 1),
            markup.nodes.Node("TEXT", " ", 1)
        ], 3)
    ], 7))
    assert output == nodes


def test_headings_number():
    compiling = "# lol1\n\nlol"
    output, prop = markup.commands._compile(compiling, False, "", tree=True)
    nodes = str(markup.nodes.BodyNode([
        markup.nodes.HeadNode("HEAD1", " lol1", 5),
        markup.nodes.ParagraphNode([
            markup.nodes.Node("TEXT", "lol", 1),
            markup.nodes.Node("TEXT", " ", 1)
        ], 3)
    ], 8))
    assert output == nodes


def test_headings_symbol():
    compiling = "# lol-\n\nlol"
    output, prop = markup.commands._compile(compiling, False, "", tree=True)
    nodes = str(markup.nodes.BodyNode([
        markup.nodes.HeadNode("HEAD1", " lol-", 5),
        markup.nodes.ParagraphNode([
            markup.nodes.Node("TEXT", "lol", 1),
            markup.nodes.Node("TEXT", " ", 1)
        ], 3)
    ], 8))
    assert output == nodes


def test_headings_nl1():
    compiling = "# lol\nlol"
    output, prop = markup.commands._compile(
        compiling, False, "\n\n", tree=True)
    nodes = str(markup.nodes.BodyNode([
        markup.nodes.HeadNode("HEAD1", " lol", 3),
        markup.nodes.ParagraphNode([
            markup.nodes.Node("TEXT", "lol", 1),
            markup.nodes.Node("TEXT", " ", 1)
        ], 3)
    ], 6))
    assert output == nodes


def test_list_different():
    """
    * a
      + b
        - c
      + d
    * e
        - f

    '<Body Paragprphs:
      <List sentences: 
        <Sentence type: TEXT, value: " a \t", Consumed: 3>,
        <Sentence type: LIST2, value: "", Consumed: 1>,
        <Sentence type: TEXT, value: " b \t\t", Consumed: 3>,
        <Sentence type: LIST3, value: "", Consumed: 1>,
        <Sentence type: TEXT, value: " c \t", Consumed: 3>,
        <Sentence type: LIST2, value: "", Consumed: 1>,
        <Sentence type: TEXT, value: " d ", Consumed: 2>,
        <Sentence type: LIST1, value: "", Consumed: 1>,
        <Sentence type: TEXT, value: "e \t\t", Consumed: 3>,
        <Sentence type: LIST3, value: "", Consumed: 1>,
        <Sentence type: TEXT, value: " f", Consumed: 1>,
      Consumed: 23>,
    Consumed: 23>'
    """
    compiling = "* a\n\t+ b\n\t\t- c\n\t+ d\n*e\n\t\t- f\n"
    output, prop = markup.commands._compile(compiling, False, "", tree=True)
    nodes = str(markup.nodes.BodyNode([
        markup.nodes.ListNode([
            markup.nodes.Node("LIST1", "", 1),
            markup.nodes.Node("TEXT", " a ", 2),
            markup.nodes.Node("LIST2", "", 2),
            markup.nodes.Node("TEXT", " b ", 2),
            markup.nodes.Node("LIST3", "", 3),
            markup.nodes.Node("TEXT", " c ", 2),
            markup.nodes.Node("LIST2", "", 2),
            markup.nodes.Node("TEXT", " d ", 2),
            markup.nodes.Node("LIST1", "", 1),
            markup.nodes.Node("TEXT", "e ", 2),
            markup.nodes.Node("LIST3", "", 3),
            markup.nodes.Node("TEXT", " f", 1),
        ], 25)
    ], 25))
    assert output == nodes


def test_list_minus():
    """
    - a
      - b
        - c
      - d
    - e
        - f

    '<Body Paragprphs:
      <List sentences: 
        <Sentence type: TEXT, value: " a \t", Consumed: 3>,
        <Sentence type: LIST2, value: "", Consumed: 1>,
        <Sentence type: TEXT, value: " b \t\t", Consumed: 3>,
        <Sentence type: LIST3, value: "", Consumed: 1>,
        <Sentence type: TEXT, value: " c \t", Consumed: 3>,
        <Sentence type: LIST2, value: "", Consumed: 1>,
        <Sentence type: TEXT, value: " d ", Consumed: 2>,
        <Sentence type: LIST1, value: "", Consumed: 1>,
        <Sentence type: TEXT, value: "e \t\t", Consumed: 3>,
        <Sentence type: LIST3, value: "", Consumed: 1>,
        <Sentence type: TEXT, value: " f", Consumed: 1>,
      Consumed: 23>,
    Consumed: 23>'
    """
    compiling = "- a\n\t- b\n\t\t- c\n\t- d\n- e\n\t\t- f\n"
    output, prop = markup.commands._compile(compiling, False, "", tree=True)
    nodes = str(markup.nodes.BodyNode([
        markup.nodes.ListNode([
            markup.nodes.Node("LIST1", "", 1),
            markup.nodes.Node("TEXT", " a ", 2),
            markup.nodes.Node("LIST2", "", 2),
            markup.nodes.Node("TEXT", " b ", 2),
            markup.nodes.Node("LIST3", "", 3),
            markup.nodes.Node("TEXT", " c ", 2),
            markup.nodes.Node("LIST2", "", 2),
            markup.nodes.Node("TEXT", " d ", 2),
            markup.nodes.Node("LIST1", "", 1),
            markup.nodes.Node("TEXT", " e ", 2),
            markup.nodes.Node("LIST3", "", 3),
            markup.nodes.Node("TEXT", " f", 1),
        ], 25)
    ], 25))
    assert output == nodes


def test_sentence_no_escape():
    compiling = "import lol\nlol.is_dir\n\\\\-+*lol\n"
    output, prop = markup.commands._compile(
        compiling, False, "\n\n", tree=True)
    nodes = str(markup.nodes.BodyNode([
        markup.nodes.ParagraphNode([
            markup.nodes.Node("TEXT", "import lol lol.is_dir \\-+*lol", 11),
        ], 13)
    ], 13))
    assert output == nodes


def test_text_paragraphs_no_escape():
    compiling = "import lol\nlol.is_dir\n\\\\-+*lol\n\nimport lol\nlol.is_dir\n\\\\-+*lol\n"
    output, prop = markup.commands._compile(
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


def test_tag_numbers():
    compiling = "<12233>\n"
    output, prop = markup.commands._compile(
        compiling, False, "\n\n", tree=True)
    nodes = str(markup.nodes.BodyNode([
        markup.nodes.Node("TAG", "12233", 5),
    ], 5))
    assert output == nodes


def test_tag_text():
    compiling = "<tag>\n"
    output, prop = markup.commands._compile(
        compiling, False, "\n\n", tree=True)
    nodes = str(markup.nodes.BodyNode([
        markup.nodes.Node("TAG", "tag", 5),
    ], 5))
    assert output == nodes


def test_tag_text_numbers():
    compiling = "<tag222withnum>\n"
    output, prop = markup.commands._compile(
        compiling, False, "\n\n", tree=True)
    nodes = str(markup.nodes.BodyNode([
        markup.nodes.Node("TAG", "tag222withnum", 7),
    ], 7))
    assert output == nodes
