import markup
import os


def test_code_no_escape():
    output = markup.terminal.terminal(0)
    compiling = "```python\nimport lol\nlol.is_dir\n\\\\-+*\n```"
    output, _ = markup.commands._compile(
        compiling, output, "\n\n", tree=True)
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
    output = markup.terminal.terminal(0)
    compiling = "# lol\n\nlol"
    output, _ = markup.commands._compile(compiling, output, "", tree=True)
    nodes = str(markup.nodes.BodyNode([
        markup.nodes.HeadNode("HEAD1", " lol", 4),
        markup.nodes.ParagraphNode([
            markup.nodes.Node("TEXT", "lol", 1),
            markup.nodes.Node("TEXT", " ", 1)
        ], 3)
    ], 7))
    assert output == nodes


def test_headings_number():
    output = markup.terminal.terminal(0)
    compiling = "# lol1\n\nlol"
    output, _ = markup.commands._compile(compiling, output, "", tree=True)
    nodes = str(markup.nodes.BodyNode([
        markup.nodes.HeadNode("HEAD1", " lol1", 5),
        markup.nodes.ParagraphNode([
            markup.nodes.Node("TEXT", "lol", 1),
            markup.nodes.Node("TEXT", " ", 1)
        ], 3)
    ], 8))
    assert output == nodes


def test_headings_symbol():
    output = markup.terminal.terminal(0)
    compiling = "# lol-\n\nlol"
    output, _ = markup.commands._compile(compiling, output, "", tree=True)
    nodes = str(markup.nodes.BodyNode([
        markup.nodes.HeadNode("HEAD1", " lol-", 5),
        markup.nodes.ParagraphNode([
            markup.nodes.Node("TEXT", "lol", 1),
            markup.nodes.Node("TEXT", " ", 1)
        ], 3)
    ], 8))
    assert output == nodes


def test_headings_nl1():
    output = markup.terminal.terminal(0)
    compiling = "# lol\nlol"
    output, _ = markup.commands._compile(
        compiling, output, "\n\n", tree=True)
    nodes = str(markup.nodes.BodyNode([
        markup.nodes.HeadNode("HEAD1", " lol", 3),
        markup.nodes.ParagraphNode([
            markup.nodes.Node("TEXT", "lol", 1),
            markup.nodes.Node("TEXT", " ", 1)
        ], 3)
    ], 6))
    assert output == nodes


def test_list_different_spaces():
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
        <Sentence type: ULIST2, value: "", Consumed: 1>,
        <Sentence type: TEXT, value: " b \t\t", Consumed: 3>,
        <Sentence type: ULIST3, value: "", Consumed: 1>,
        <Sentence type: TEXT, value: " c \t", Consumed: 3>,
        <Sentence type: ULIST2, value: "", Consumed: 1>,
        <Sentence type: TEXT, value: " d ", Consumed: 2>,
        <Sentence type: ULIST1, value: "", Consumed: 1>,
        <Sentence type: TEXT, value: "e \t\t", Consumed: 3>,
        <Sentence type: ULIST3, value: "", Consumed: 1>,
        <Sentence type: TEXT, value: " f", Consumed: 1>,
      Consumed: 23>,
    Consumed: 23>'
    """
    output = markup.terminal.terminal(0)
    compiling = "- a\n  - b\n    - c\n  - d\n- e\n    - f\n"
    output, _ = markup.commands._compile(compiling, output, "", tree=True)
    nodes = str(markup.nodes.BodyNode([
        markup.nodes.ListNode([
            markup.nodes.Node("ULIST1", "", 1),
            markup.nodes.Node("TEXT", " a ", 2),
            markup.nodes.Node("ULIST2", "", 2),
            markup.nodes.Node("TEXT", " b ", 2),
            markup.nodes.Node("ULIST3", "", 3),
            markup.nodes.Node("TEXT", " c ", 2),
            markup.nodes.Node("ULIST2", "", 2),
            markup.nodes.Node("TEXT", " d ", 2),
            markup.nodes.Node("ULIST1", "", 1),
            markup.nodes.Node("TEXT", " e ", 2),
            markup.nodes.Node("ULIST3", "", 3),
            markup.nodes.Node("TEXT", " f", 1),
        ], 25)
    ], 25))
    assert output == nodes


def test_list_different_tabs():
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
        <Sentence type: ULIST2, value: "", Consumed: 1>,
        <Sentence type: TEXT, value: " b \t\t", Consumed: 3>,
        <Sentence type: ULIST3, value: "", Consumed: 1>,
        <Sentence type: TEXT, value: " c \t", Consumed: 3>,
        <Sentence type: ULIST2, value: "", Consumed: 1>,
        <Sentence type: TEXT, value: " d ", Consumed: 2>,
        <Sentence type: ULIST1, value: "", Consumed: 1>,
        <Sentence type: TEXT, value: "e \t\t", Consumed: 3>,
        <Sentence type: ULIST3, value: "", Consumed: 1>,
        <Sentence type: TEXT, value: " f", Consumed: 1>,
      Consumed: 23>,
    Consumed: 23>'
    """
    output = markup.terminal.terminal(0)
    compiling = "* a\n\t+ b\n\t\t- c\n\t+ d\n*e\n\t\t- f\n"
    output, _ = markup.commands._compile(compiling, output, "", tree=True)
    nodes = str(markup.nodes.BodyNode([
        markup.nodes.ListNode([
            markup.nodes.Node("ULIST1", "", 1),
            markup.nodes.Node("TEXT", " a ", 2),
            markup.nodes.Node("ULIST2", "", 2),
            markup.nodes.Node("TEXT", " b ", 2),
            markup.nodes.Node("ULIST3", "", 3),
            markup.nodes.Node("TEXT", " c ", 2),
            markup.nodes.Node("ULIST2", "", 2),
            markup.nodes.Node("TEXT", " d ", 2),
            markup.nodes.Node("ULIST1", "", 1),
            markup.nodes.Node("TEXT", "e ", 2),
            markup.nodes.Node("ULIST3", "", 3),
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
        <Sentence type: ULIST2, value: "", Consumed: 1>,
        <Sentence type: TEXT, value: " b \t\t", Consumed: 3>,
        <Sentence type: ULIST3, value: "", Consumed: 1>,
        <Sentence type: TEXT, value: " c \t", Consumed: 3>,
        <Sentence type: ULIST2, value: "", Consumed: 1>,
        <Sentence type: TEXT, value: " d ", Consumed: 2>,
        <Sentence type: ULIST1, value: "", Consumed: 1>,
        <Sentence type: TEXT, value: "e \t\t", Consumed: 3>,
        <Sentence type: ULIST3, value: "", Consumed: 1>,
        <Sentence type: TEXT, value: " f", Consumed: 1>,
      Consumed: 23>,
    Consumed: 23>'
    """
    output = markup.terminal.terminal(0)
    compiling = "- a\n\t- b\n\t\t- c\n\t- d\n- e\n\t\t- f\n"
    output, _ = markup.commands._compile(compiling, output, "", tree=True)
    nodes = str(markup.nodes.BodyNode([
        markup.nodes.ListNode([
            markup.nodes.Node("ULIST1", "", 1),
            markup.nodes.Node("TEXT", " a ", 2),
            markup.nodes.Node("ULIST2", "", 2),
            markup.nodes.Node("TEXT", " b ", 2),
            markup.nodes.Node("ULIST3", "", 3),
            markup.nodes.Node("TEXT", " c ", 2),
            markup.nodes.Node("ULIST2", "", 2),
            markup.nodes.Node("TEXT", " d ", 2),
            markup.nodes.Node("ULIST1", "", 1),
            markup.nodes.Node("TEXT", " e ", 2),
            markup.nodes.Node("ULIST3", "", 3),
            markup.nodes.Node("TEXT", " f", 1),
        ], 25)
    ], 25))
    assert output == nodes


def test_sentence_no_escape():
    output = markup.terminal.terminal(0)
    compiling = "import lol\nlol.is_dir\n\\\\-+*lol\n"
    output, _ = markup.commands._compile(
        compiling, output, "\n\n", tree=True)
    nodes = str(markup.nodes.BodyNode([
        markup.nodes.ParagraphNode([
            markup.nodes.Node("TEXT", "import lol lol.is_dir \\-+*lol", 11),
        ], 13)
    ], 13))
    assert output == nodes


def test_paragraph_split():
    output = markup.terminal.terminal(0)
    compiling = "first paragraph.\nsecond line\n\nsecond paragraph.\nsecond line\n"
    output, _ = markup.commands._compile(
        compiling, output, "\n\n", tree=True)
    nodes = str(markup.nodes.BodyNode([
        markup.nodes.ParagraphNode([
            markup.nodes.Node("TEXT", "first paragraph. second line", 3),
        ], 5),
        markup.nodes.ParagraphNode([
            markup.nodes.Node("TEXT", "second paragraph. second line", 3),
        ], 5)
    ], 10))
    assert output == nodes


def test_text_paragraphs_no_escape():
    output = markup.terminal.terminal(0)
    compiling = "import lol\nlol.is_dir\n\\\\-+*lol\n\nimport lol\nlol.is_dir\n\\\\-+*lol\n"
    output, _ = markup.commands._compile(
        compiling, output, "\n\n", tree=True)
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
    output = markup.terminal.terminal(0)
    compiling = "<12233>\n"
    output, _ = markup.commands._compile(
        compiling, output, "\n\n", tree=True)
    nodes = str(markup.nodes.BodyNode([
        markup.nodes.Node("TAG", "12233", 5),
    ], 5))
    assert output == nodes


def test_tag_text():
    output = markup.terminal.terminal(0)
    compiling = "<tag>\n"
    output, _ = markup.commands._compile(
        compiling, output, "\n\n", tree=True)
    nodes = str(markup.nodes.BodyNode([
        markup.nodes.Node("TAG", "tag", 5),
    ], 5))
    assert output == nodes


def test_tag_text_numbers():
    output = markup.terminal.terminal(0)
    compiling = "<tag222withnum>\n"
    output, _ = markup.commands._compile(
        compiling, output, "\n\n", tree=True)
    nodes = str(markup.nodes.BodyNode([
        markup.nodes.Node("TAG", "tag222withnum", 7),
    ], 7))
    assert output == nodes
