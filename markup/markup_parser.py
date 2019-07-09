from markup.nodes import *
from markup.match import *


def Parse_Text(tokens):
    if tokens.peek(["TEXT"]):
        return Node("TEXT", tokens.grab(0).value, 1)
    return nullNode()


def single_newline(tokens):
    node = nullNode()
    if tokens.peek(["NEWLINE"]):
        node = Node("TEXT", " ", 1)
    if tokens.peek(["NEWLINE", "NEWLINE"]):
        return nullNode()
    return node


def multi_newline(tokens):
    node = nullNode()
    if tokens.peek(["NEWLINE"]):
        node = Node("TEXT", " ", 1)
    return node


def Parse_Bold(tokens):
    if tokens.peek_or([["STAR", "STAR", "TEXT", "STAR", "STAR"], ["UNDERSCORE", "UNDERSCORE", "TEXT", "UNDERSCORE", "UNDERSCORE"]]):
        return Node("BOLD", tokens.grab(2).value, 5)
    return nullNode()


def Parse_Emph(tokens):
    if tokens.peek_or([["STAR", "TEXT", "STAR"], ["UNDERSCORE", "TEXT", "UNDERSCORE"]]):
        return Node("EMPH", tokens.grab(1).value, 3)
    return nullNode()


def Parse_Tag(tokens):
    if tokens.peek(["TAGO", "TEXT", "TAGC"]):
        return Node("TAG", tokens.grab(1).value, 3)
    return nullNode()


def Parse_Tags(tokens):
    node = match_first(tokens, [single_newline, Parse_Tag])
    if type(node) == nullNode:
        return nullNode()
    if not tokens.peek_at(node.consumed, ['NEWLINE', 'NEWLINE']):
        return nullNode()
    node.consumed += 2
    return node


def H1_Parser(tokens):
    if tokens.peek(["HASH", "TEXT"]):
        return HeadNode("HEAD1", tokens.grab(1).value, 2)
    return nullNode()


def H2_Parser(tokens):
    if tokens.peek(["HASH", "HASH", "TEXT"]):
        return HeadNode("HEAD2", tokens.grab(2).value, 3)
    return nullNode()


def H3_Parser(tokens):
    if tokens.peek(["HASH", "HASH", "HASH", "TEXT"]):
        return HeadNode("HEAD3", tokens.grab(3).value, 4)
    return nullNode()


def Header_Parser(tokens):
    node = match_first(
        tokens, [H1_Parser, H2_Parser, H3_Parser])
    if type(node) == nullNode:
        return nullNode()
    if not tokens.peek_at(node.consumed, ['NEWLINE', 'NEWLINE']):
        return nullNode()
    node.consumed += 2
    return node


def L1_Parser(tokens):
    if tokens.peek(["STAR"]):
        return Node("LIST1", "", 1)
    return nullNode()


def L2_Parser(tokens):
    if tokens.peek(["PLUS"]):
        return Node("LIST2", "", 1)
    return nullNode()


def L3_Parser(tokens):
    if tokens.peek(["MINUS"]):
        return Node("LIST3", "", 1)
    return nullNode()


def Item_Parser(tokens):
    return match_first(tokens, [Sentence_Parser, L1_Parser, L2_Parser, L3_Parser])


def List_Parser(tokens):
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


def Code_Start_Parser(tokens):
    if tokens.peek(["GRAVE", "GRAVE", "GRAVE", "NEWLINE"]):
        return Node("CODE", "", 4)
    return nullNode()


def Code_Parser(tokens):
    if type(Code_Start_Parser(tokens)) != nullNode:
        return nullNode()
    return match_first(tokens, [multi_newline, Parse_Text])


def Code_Parser_Multiline(tokens):
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
    return match_first(tokens, [Parse_Text, Parse_Emph, Parse_Bold, single_newline])


def Sentences_NL_Parser(tokens):
    nodes, consumed = match_star(tokens, Sentence_Parser)
    if nodes == []:
        return nullNode()
    if not tokens.peek_at(consumed, ['NEWLINE', 'NEWLINE']):
        return nullNode()
    consumed += 2
    return ParagraphNode(nodes, consumed)


def Sentences_EOF_Parser(tokens):
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


def Parse_Paragraph(tokens):
    return match_first(tokens, [Parse_Tags, Code_Parser_Multiline, Header_Parser, List_Parser, Sentences_NL_Parser, Sentences_EOF_Parser])


def Parse_Body(tokens):
    nodes, consumed = match_star(tokens, Parse_Paragraph)
    if nodes == []:
        return nullNode()
    return BodyNode(nodes, consumed)
