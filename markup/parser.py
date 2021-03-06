from markup.nodes import Node, nullNode, HeadNode, ListNode, CodeNode, ParagraphNode, BodyNode, EquationNode
from markup.match import match_first, match_star, match_star_err, match_multi_star_until, match_star_merge
import click


def parse_markdown(tokens):
    """
    feeds a token list in to a document

    tokens: the tokens to feed
    """
    body = Body_Parser(tokens)
    if body.consumed != -1 + tokens.length():
        if not tokens.grab(body.consumed-1).context == "EOF":
            list = tokens.grab_num(body.consumed-3, 5)
            context = ""
            for i in list:
                context += i.context + "\n"
            click.secho(
                "error at %s\n%s" % (tokens.grab(body.consumed-1).at, context), fg="red",
                err=True)
    return body

# ADD: inline equations
# ADD: inline code
# ADD: indent code
# ADD: tables
# ADD: inline equations


def Text_Parser(tokens):
    """
    Text:
        Text
    """
    if tokens.peek(["TEXT"]) or tokens.peek(["NUM"]):
        return Node("TEXT", tokens.grab(0).value, 1)
    return nullNode()

def link_Parser(tokens):
    """
    BTAG
    PTAG
    """
    first = match_first(tokens, [BTag_Parser])
    if (type(first) is nullNode):
        return nullNode()
    second = match_first(tokens.offset(first.consumed), [PTag_Parser])
    if (type(second) is nullNode):
        return nullNode()
    consumed = first.consumed + second.consumed
    if tokens.peek_at(consumed, ['NEWLINE']):
        consumed += 1
    if tokens.peek_at(consumed, ['EOF']):
        consumed += 1
    return Node("LINK", "%s: %s" % (first.value, second.value), consumed)


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


def Bold_Parser_End(tokens):
    if tokens.peek_or([["STAR", "STAR"], ["UNDERSCORE", "UNDERSCORE"]]):
        return Node("MATCH", "lol", 2)
    return nullNode()


def Bold_Parser(tokens):
    if tokens.peek_or([["STAR", "STAR"], ["UNDERSCORE", "UNDERSCORE"]]):
        nodes, consumed = match_multi_star_until(
            tokens.offset(2), [Text_Parser], Bold_Parser_End)
        return Node("BOLD", nodes[0].value, 3+consumed)
    return nullNode()


def Emph_Parser_End(tokens):
    if tokens.peek_or([["STAR"], ["UNDERSCORE"]]):
        return Node("MATCH", "lol", 1)
    return nullNode()


def Emph_Parser(tokens):
    if tokens.peek_or([["STAR"], ["UNDERSCORE"]]):
        nodes, consumed = match_multi_star_until(
            tokens.offset(1), [Text_Parser], Emph_Parser_End)
        return Node("EMPH", nodes[0].value, 1+consumed)
    return nullNode()


def Equation_Parser_End(tokens):
    if tokens.peek(["DOLLAR", "DOLLAR", "NEWLINE"]):
        return Node("MATCH", "lol", 3)
    return nullNode()


def Equation_Parser(tokens):
    if tokens.peek(["DOLLAR", "DOLLAR"]):
        nodes, consumed = match_multi_star_until(
            tokens.offset(2), [Text_Parser], Equation_Parser_End)
        return EquationNode(nodes[0].value, consumed+5)
    return nullNode()


def Equation_Parser_Inline_End(tokens):
    if tokens.peek(["DOLLAR"]):
        return Node("MATCH", "lol", 1)
    return nullNode()


def Equation_Parser_Inline(tokens):
    if tokens.peek(["DOLLAR"]):
        nodes, consumed = match_multi_star_until(
            tokens.offset(1), [Text_Parser], Equation_Parser_Inline_End)
        return Node("EQU", nodes[0].value, 1+consumed)
    return nullNode()


def Tag_Parser(tokens):
    """
    Tag:
        "<"
        Text *
        ">"
    """
    if tokens.peek(["TAGO"]):
        nodes, consumed = match_star_merge(tokens.offset(1), Text_Parser)
        text = ""
        for node in nodes:
            text += node.value
        if tokens.offset(consumed).peek(["TAGC"]):
            return Node("TAG", text[:-1], consumed+1)
    return nullNode()

def BTag_Parser(tokens):
    """
    Tag:
        "["
        Text *
        "]"
    """
    if tokens.peek(["BRKO"]):
        nodes, consumed = match_star_err(tokens.offset(1), Text_Parser)
        text = ""
        for node in nodes:
            text += node.value
        if tokens.offset(consumed+1).peek(["BRKC"]):
            return Node("BTAG", text, consumed+2)
    return nullNode()

def PTag_Parser(tokens):
    """
    Tag:
        "["
        Text *
        "]"
    """
    if tokens.peek(["PARO"]):
        nodes, consumed = match_star_err(tokens.offset(1), Text_Parser)
        text = ""
        for node in nodes:
            text += node.value
        if tokens.offset(consumed+1).peek(["PARC"]):
            return Node("PTAG", text, consumed+2)
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


def Number_Parser(tokens):
    """
    Number:
        Num
        -
    """
    if tokens.peek(["NUM", "MINUS"]):
        return Node("TEXT", "", 1)
    return nullNode()


def UL1_Parser(tokens):
    """
    L1:
        Bullet
    """
    if type(match_first(tokens, [Bullet_Parser])) != nullNode:
        return Node("ULIST1", "", 1)
    return nullNode()


def UL2_Parser(tokens):
    """
    L2:
        "\t"
        Bullet
    """
    if tokens.peek(["TAB"]) and type(match_first(tokens.offset(1), [Bullet_Parser])) != nullNode:
        return Node("ULIST2", "", 2)
    return nullNode()


def UL3_Parser(tokens):
    """
    L3:
        "\t\t"
        Bullet
    """
    if tokens.peek(["TAB", "TAB"]) and type(match_first(tokens.offset(2), [Bullet_Parser])) != nullNode:
        return Node("ULIST3", "", 3)
    return nullNode()


def OL1_Parser(tokens):
    """
    L1:
        Bullet
    """
    if type(match_first(tokens, [Number_Parser])) != nullNode:
        return Node("OLIST1", "", 2)
    return nullNode()


def OL2_Parser(tokens):
    """
    L2:
        "\t"
        Bullet
    """
    if tokens.peek(["TAB"]) and type(match_first(tokens.offset(1), [Number_Parser])) != nullNode:
        return Node("OLIST2", "", 3)
    return nullNode()


def OL3_Parser(tokens):
    """
    L3:
        "\t\t"
        number
    """
    if tokens.peek(["TAB", "TAB"]) and type(match_first(tokens.offset(2), [Number_Parser])) != nullNode:
        return Node("OLIST3", "", 4)
    return nullNode()


def Item_Parser(tokens):
    """
    Item:
        L1 | L2 | L3 | Sentence
    """
    return match_first(tokens, [Sentence_Parser, OL3_Parser, OL2_Parser, OL1_Parser, UL3_Parser, UL2_Parser, UL1_Parser])


def List_Parser(tokens):
    """
    List:
        ( L1 | L2 | L3 ) & Item*
        "\n\n"
    """
    if type(match_first(tokens, [UL3_Parser, UL2_Parser, UL1_Parser, OL1_Parser, OL2_Parser, OL3_Parser])) == nullNode:
        return nullNode()
    node = match_first(tokens, [UL3_Parser, UL2_Parser,
                                UL1_Parser, OL1_Parser, OL2_Parser, OL3_Parser])
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


def Tab_Parser(tokens):
    """
    Tab:
        "\t"
    """
    if tokens.peek(["TAB"]):
        return Node("TEXT", "\t", 1)
    return nullNode()


def Code_Parser(tokens):
    """
    Code:
        ! Code_Start
        ( MultiNewline | Text ) *
    """
    return match_multi_star_until(tokens, [Multinewline_Parser, Text_Parser, Tab_Parser], Code_End_Parser)


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
    return match_first(tokens, [Text_Parser, Equation_Parser_Inline, Bold_Parser, Emph_Parser, Singlenewline_Parser])


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
    return match_first(tokens, [link_Parser, Multi_Tag_Parser, Equation_Parser, Code_Multi_line_Parser, Header_Parser, List_Parser, Sentences_NL_Parser, Sentences_EOF_Parser])


def Body_Parser(tokens):
    """
    Body:
        Paragraph*
    """
    nodes, consumed = match_star(tokens, Paragraph_Parser)
    if nodes == []:
        return nullNode()
    return BodyNode(nodes, consumed)
