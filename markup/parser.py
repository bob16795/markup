from markup.nodes import Node, nullNode, HeadNode, ListNode, CodeNode, ParagraphNode, BodyNode
from markup.match import match_first, match_star, match_star_err, match_multi_star_until, match_star_merge

# ADD: inline code
# ADD: indent code
# ADD: tables
# ADD: equations


def Text_Parser(tokens):
    """
    Text:
        Text
    """
    if tokens.peek(["TEXT"]) or tokens.peek(["NUM"]):
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
    if tokens.peek_or([["STAR", "STAR", "NUM", "STAR", "STAR"], ["UNDERSCORE", "UNDERSCORE", "NUM", "UNDERSCORE", "UNDERSCORE"]]):
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
    if tokens.peek_or([["STAR", "NUM", "STAR"], ["UNDERSCORE", "NUM", "UNDERSCORE"]]):
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
    if tokens.peek(["TAGO", "NUM", "TAGC"]):
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
        Text | num *
    """
    if tokens.peek(["HASH"]):
        nodes, consumed = match_star_merge(tokens.offset(1), Text_Parser)
        text = ""
        for node in nodes:
            text += node.value
        return HeadNode("HEAD1", text, consumed + 1)
    return nullNode()


def H2_Parser(tokens):
    """
    H3:
        "##"
        Text
    """
    if tokens.peek(["HASH", "HASH"]):
        nodes, consumed = match_star_merge(tokens.offset(2), Text_Parser)
        text = ""
        for node in nodes:
            text += node.value
        return HeadNode("HEAD2", text, consumed + 2)
    return nullNode()


def H3_Parser(tokens):
    """
    H3:
        "###"
        Text
    """
    if tokens.peek(["HASH", "HASH", "HASH"]):
        nodes, consumed = match_star(tokens.offset(3), Text_Parser)
        text = ""
        for node in nodes:
            text += node.value
        return HeadNode("HEAD3", text, consumed + 3)
    return nullNode()


def Header_Parser(tokens):
    """
    Header:
        H1 | H2 | H3
        "\n" | "\n\n"
    """
    node = match_first(
        tokens, [H3_Parser, H2_Parser, H1_Parser])
    if type(node) == nullNode:
        return nullNode()

    if not tokens.peek_at(node.consumed, ['NEWLINE', 'NEWLINE']):
        if not tokens.peek_at(node.consumed, ['NEWLINE']):
            return nullNode()
        else:
            node.consumed += 1
    else:
        node.consumed += 2
    return node


def Bullet_Parser(tokens):
    """
    Bullet:
        "*" | "+" | "-"
    """
    if tokens.peek_or([["STAR"], ["PLUS"], ["MINUS"]]):
        return Node("TEXT", "", 1)
    return nullNode()


def L1_Parser(tokens):
    """
    L1:
        Bullet
    """
    if type(match_first(tokens, [Bullet_Parser])) != nullNode:
        return Node("LIST1", "", 1)
    return nullNode()


def L2_Parser(tokens):
    """
    L2:
        "\t"
        Bullet
    """
    if tokens.peek(["TAB"]) and type(match_first(tokens.offset(1), [Bullet_Parser])) != nullNode:
        return Node("LIST2", "", 2)
    return nullNode()


def L3_Parser(tokens):
    """
    L3:
        "\t\t"
        Bullet
    """
    if tokens.peek(["TAB", "TAB"]) and type(match_first(tokens.offset(2), [Bullet_Parser])) != nullNode:
        return Node("LIST3", "", 3)
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
    node = match_first(tokens, [L1_Parser, L2_Parser, L3_Parser])
    nodes, consumed = match_star_merge(
        tokens.offset(node.consumed), Item_Parser)
    consumed += node.consumed
    if nodes == []:
        return nullNode()
    if tokens.peek_at(consumed, ['EOF']):
        consumed += 1
    elif tokens.peek_at(consumed, ['NEWLINE', 'EOF']):
        consumed += 2
    else:
        if not tokens.peek_at(consumed, ['NEWLINE', 'NEWLINE']):
            return nullNode()
        consumed += 2
    nodes.insert(0, node)
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
    return match_multi_star_until(tokens, [Multinewline_Parser, Text_Parser], Code_End_Parser)


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
    value = tokens.grab(3).value
    nodes, consumed = match_multi_star_until(tokens.offset(
        i), [Multinewline_Parser, Text_Parser], Code_End_Parser)
    consumed += i + 4
    return CodeNode(nodes, consumed, value)


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
    nodes, consumed = match_star_merge(tokens, Sentence_Parser)
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
