from markup.token_class import Token, Token_List
from markup.doc_props import doc_properties
from markup.terminal import error, log, debug, info
import click


def tokenize(file_cached, prop_app, file_name, output):
    """
    tokenizes a string

    file_cached: the string to be tokenized
    prop_app:    the properties to append
    """

    output.add(info, "tokenizing %s" % file_name)

    props = doc_properties()
    file_cached = file_cached.split("\n")
    mu = True
    token_dict = {
        "_": ["UNDERSCORE", "SYM"],
        "`": ["GRAVE", "SYM"],
        "*": ["STAR", "SYM"],
        "+": ["PLUS", "SYM"],
        "-": ["MINUS", "SYM"],
        "#": ["HASH", "SYM"],
        "<": ["TAGO", "SYM"],
        ">": ["TAGC", "SYM"],
        "\t": ["TAB", ""],
        "\n": ["NEWLINE", ""],
    }
    numbers = "1234567890"
    text_is_number = False
    md_tokens = []
    ignore = 0
    for x, i in enumerate(file_cached):
        text = ""
        i = props.tag_rep(i)
        if i == "---":
            mu = not(mu)
        else:
            if mu:
                for y, j in enumerate(i):
                    if ignore != 0:
                        ignore -= 1
                        text = text + str(j)
                    else:
                        if j == "\\":
                            ignore = 1
                        elif j in token_dict:
                            if text != "":
                                if text_is_number:
                                    text_is_number = False
                                    md_tokens.append(
                                        Token("NUM", text, "line %s, col %s" % (x+1, y), i))
                                else:
                                    md_tokens.append(
                                        Token("TEXT", text, "line %s, col %s" % (x+1, y), i))
                                text = ""
                            token = token_dict[j]
                            md_tokens.append(
                                Token(token[0], token[1], "line %s, col %s" % (x+1, y), i))
                        else:
                            if j in numbers and not text_is_number:
                                if text != "":
                                    md_tokens.append(
                                        Token("TEXT", text, "line %s, col %s" % (x+1, y), i))
                                text = ""
                                text_is_number = True
                            if text_is_number and not j in numbers:
                                if text != "":
                                    md_tokens.append(
                                        Token("NUM", text, "line %s, col %s" % (x+1, y), i))
                                text = ""
                                text_is_number = False
                            text = text + str(j)
                if text != "":
                    if text_is_number:
                        md_tokens.append(
                            Token("NUM", text, "end of last line in file", i))
                    else:
                        md_tokens.append(
                            Token("TEXT", text, "end of last line in file", i))
                md_tokens.append(
                    Token("NEWLINE", "", "end of line {x+1}", i))
            else:
                props.set(i)
    md_tokens.append(
        Token("EOF", "", "end of last line", "EOF"))
    return Token_List(md_tokens), props
