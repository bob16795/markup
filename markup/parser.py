from markup.nodes import Node, nullNode, HeadNode, ListNode, CodeNode, ParagraphNode, BodyNode
from markup.match import match_first, match_star, match_star_err


def Text_Parser(tokens):
    """
    Text:
        Text
    """
    if tokens.peek(["TEXT"]):
        return Node("TEXT", tokens.grab(0).value, 1)
    return nullNode()


def Singlenewline_Parser(tokens):
    """
    Singlenewline:
        "\n"
        !"\n"
    """
    node = nullNode()
    if tokens.peek(["NEWLINE"]):
        node = Node("TEXT", " ", 1)
    if tokens.peek(["NEWLINE", "NEWLINE"]):
        return nullNode()
    return node


def Multinewline_Parser(tokens):
    """
    Multinewline:
        "\n"
    """
    node = nullNode()
    if tokens.peek(["NEWLINE"]):
        node = Node("TEXT", " ", 1)
    return node


def Bold_Parser(tokens):
    """
    Bold:
        ( "**"
          Text
          "**" ) |
        ( "__"
          Text
          "__")
    """
    if tokens.peek_or([["STAR", "STAR", "TEXT", "STAR", "STAR"], ["UNDERSCORE", "UNDERSCORE", "TEXT", "UNDERSCORE", "UNDERSCORE"]]):
        return Node("BOLD", tokens.grab(2).value, 5)
    return nullNode()


def Emph_Parser(tokens):
    """
    Emph:
        ( "*"
          Text
          "*" ) |
        ( "_"
          Text
          "_")
    """
    if tokens.peek_or([["STAR", "TEXT", "STAR"], ["UNDERSCORE", "TEXT", "UNDERSCORE"]]):
        return Node("EMPH", tokens.grab(1).value, 3)
    return nullNode()


def Tag_Parser(tokens):
    """
    Tag:
        "<"
        Text
        ">"
    """
    if tokens.peek(["TAGO", "TEXT", "TAGC"]):
        return Node("TAG", tokens.grab(1).value, 3)
    return nullNode()


def Multi_Tag_Parser(tokens):
    """
    Tags:
        NL | Tag
    """
    node = match_first(tokens, [Singlenewline_Parser, Tag_Parser])
    if type(node) == nullNode:
        return nullNode()
    if not tokens.peek_at(node.consumed, ['NEWLINE', 'NEWLINE']):
        return nullNode()
    node.consumed += 2
    return node


def H1_Parser(tokens):
    """
    H3:
        "#"
        Text
    """
    if tokens.peek(["HASH", "TEXT"]):
        return HeadNode("HEAD1", tokens.grab(1).value, 2)
    return nullNode()


def H2_Parser(tokens):
    """
    H3:
        "##"
        Text
    """
    if tokens.peek(["HASH", "HASH", "TEXT"]):
        return HeadNode("HEAD2", tokens.grab(2).value, 3)
    return nullNode()


def H3_Parser(tokens):
    """
    H3:
        "###"
        Text
    """
    if tokens.peek(["HASH", "HASH", "HASH", "TEXT"]):
        return HeadNode("HEAD3", tokens.grab(3).value, 4)
    return nullNode()


def Header_Parser(tokens):
    """
    Header:
        H1 | H2 | H3
        "\n\n"
    """
    node = match_first(
        tokens, [H1_Parser, H2_Parser, H3_Parser])
    if type(node) == nullNode:
        return nullNode()
    if not tokens.peek_at(node.consumed, ['NEWLINE', 'NEWLINE']):
        return nullNode()
    node.consumed += 2
    return node


def L1_Parser(tokens):
    """
    L1:
        "*"
    """
    if tokens.peek(["STAR"]):
        return Node("LIST1", "", 1)
    return nullNode()


def L2_Parser(tokens):
    """
    L2:
        "+"
    """
    if tokens.peek(["PLUS"]):
        return Node("LIST2", "", 1)
    return nullNode()


def L3_Parser(tokens):
    """
    L3:
        "-"
    """
    if tokens.peek(["MINUS"]):
        return Node("LIST3", "", 1)
    return nullNode()


def Item_Parser(tokens):
    """
    Item:
        L1 | L2 | L3 | Sentence
    """
    return match_first(tokens, [Sentence_Parser, L1_Parser, L2_Parser, L3_Parser])


def List_Parser(tokens):
    """
    List:
        ( L1 | L2 | L3 ) & Item*
        "\n\n"
    """
    if type(match_first(tokens, [L1_Parser, L2_Parser, L3_Parser])) == nullNode:
        return nullNode()
    nodes, consumed = match_star(tokens.offset(1), Item_Parser)
    consumed += 1
    if nodes == []:
        return nullNode()
    if not tokens.peek_at(consumed, ['NEWLINE', 'NEWLINE']):
        return nullNode()
    consumed += 2
    return ListNode(nodes, consumed)


def Code_End_Parser(tokens):
    """
    Code_End:
        "```\n"
    """
    if tokens.peek(["GRAVE", "GRAVE", "GRAVE", "NEWLINE"]):
        return Node("CODE", "", 4)
    return nullNode()


def Code_Parser(tokens):
    """
    Code:
        ! Code_Start
        ( MultiNewline | Text ) *
    """
    if type(Code_End_Parser(tokens)) != nullNode:
        return nullNode()
    return match_first(tokens, [Multinewline_Parser, Text_Parser])


def Code_Multi_line_Parser(tokens):
    """
    Code_Multi_Line:
        ( "```"
          Text
          "\n" )
        | "```\n"
        Code*
        "```\n"
    """
    i = 4
    if not tokens.peek(["GRAVE", "GRAVE", "GRAVE", "TEXT", "NEWLINE"]):
        if not tokens.peek(["GRAVE", "GRAVE", "GRAVE", "NEWLINE"]):
            return nullNode()
        else:
            i += 1
    nodes, consumed = match_star_err(tokens.offset(i), Code_Parser)
    if not tokens.peek_at(consumed+i, ["GRAVE", "GRAVE", "GRAVE", 'NEWLINE']):
        return nullNode()
    consumed += i + 4
    return CodeNode(nodes, consumed)


def Sentence_Parser(tokens):
    """
    Sentence:
        Text | Emph | Bold | Single_NL
    """
    return match_first(tokens, [Text_Parser, Emph_Parser, Bold_Parser, Singlenewline_Parser])


def Sentences_NL_Parser(tokens):
    """
    Sentences_NL:
        Sentence*
        "\n\n"
    """
    nodes, consumed = match_star(tokens, Sentence_Parser)
    if nodes == []:
        return nullNode()
    if not tokens.peek_at(consumed, ['NEWLINE', 'NEWLINE']):
        return nullNode()
    consumed += 2
    return ParagraphNode(nodes, consumed)


def Sentences_EOF_Parser(tokens):
    """
    Sentences_EOF:
        Sentence*
        "EOF" | "\nEOF"
    """
    nodes, consumed = match_star(tokens, Sentence_Parser)
    if nodes == []:
        return nullNode()
    if tokens.peek_at(consumed, ['EOF']):
        consumed += 1
    elif tokens.peek_at(consumed, ['NEWLINE', 'EOF']):
        consumed += 2
    else:
        return nullNode()
    return ParagraphNode(nodes, consumed)


def Paragraph_Parser(tokens):
    """
    Paragraph:
        Tags | Code_Multi_Line | Header | List | Sentence_NL | Sentence_EOF
    """
    return match_first(tokens, [Multi_Tag_Parser, Code_Multi_line_Parser, Header_Parser, List_Parser, Sentences_NL_Parser, Sentences_EOF_Parser])


def Body_Parser(tokens):
    """
    Body:
        Paragraph*
    """
    nodes, consumed = match_star(tokens, Paragraph_Parser)
    if nodes == []:
        return nullNode()
    return BodyNode(nodes, consumed)
