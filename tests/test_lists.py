import markup
import os


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
    output, yaml = markup.commands._compile(compiling, False, "", tree=True)
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
    compiling = "- a\n\t- b\n\t\t- c\n\t- d\n-e\n\t\t- f\n"
    output, yaml = markup.commands._compile(compiling, False, "", tree=True)
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
