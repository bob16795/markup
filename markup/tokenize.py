from markup.token_class import Token, Token_List


def prop_to_dict(prop):
    """
    converts a prop string to a dict object

    prop: the prop string
    """

    if prop.strip(" \n") != "":
        while "\n\n" in prop:
            prop = prop.replace("\n\n", "\n")
        prop_cached = prop.split("\n")
        prop_d = {"slave": "False"}
        for prop_line in prop_cached:
            if "|" in prop_line:
                req = prop_line.split("|")[0].strip("! ")
                cmd = prop_line.split("|")[1]
                property = cmd.split(":")[0].strip(" ")
                value = cmd.split(":")[1].strip(" ")
                req_value = "True"
                if "=" in req:
                    req_value = req.split("=")[1].strip(" ")
                    req = req.split("=")[0].strip(" ")
                req_bool = True
                if "!" in prop_line:
                    req_bool = False
                if req in prop_d:
                    if req_bool == ( req_value == prop_d[req]):
                        prop_d[property] = value
            else:
                cmd = prop_line
                property = cmd.split(":")[0].strip(" ")
                value = cmd.split(":")[1].strip(" ")
                prop_d[property] = value
        return prop_d
    else:
        return {}


def tokenize(file_cached, prop_app):
    """
    tokenizes a string

    file_cached: the string to be tokenized
    prop_app:    the properties to append
    """
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
        "[": ["TAGO", "SYM"],
        ")": ["TAGC", "SYM"],
        "\t": ["TAB", ""],
        "\n": ["NEWLINE", ""],
    }
    numbers = "1234567890"
    text_is_number = False
    md_tokens = []
    prop = ""
    ignore = 0
    for x, i in enumerate(file_cached):
        text = ""
        if i == "---":
            mu = not(mu)
        else:
            if mu:
                for y, j in enumerate(i):
                    if ignore != 0:
                        ignore -= 1
                        text = f"{text}{j}"
                    else:
                        if j == "\\":
                            ignore = 1
                        elif j in token_dict:
                            if text != "":
                                if text_is_number:
                                    text_is_number = False
                                    md_tokens.append(
                                        Token("NUM", text, f"line {x+1}, col {y}", i))
                                else:
                                    md_tokens.append(
                                        Token("TEXT", text, f"line {x+1}, col {y}", i))
                                text = ""
                            token = token_dict[j]
                            md_tokens.append(
                                Token(token[0], token[1], f"line {x+1}, col {y}", i))
                        else:
                            if j in numbers and not text_is_number:
                                if text != "":
                                    md_tokens.append(
                                        Token("TEXT", text, f"line {x+1}, col {y}", i))
                                text = ""
                                text_is_number = True
                            if text_is_number and not j in numbers:
                                if text != "":
                                    md_tokens.append(
                                        Token("NUM", text, f"line {x+1}, col {y}", i))
                                text = ""
                                text_is_number = False
                            text = f"{text}{j}"
                if text != "":
                    if text_is_number:
                        md_tokens.append(
                            Token("NUM", text, f"end of last line in file", i))
                    else:
                        md_tokens.append(
                            Token("TEXT", text, f"end of last line in file", i))
                md_tokens.append(
                    Token("NEWLINE", "", f"end of line {x+1}", i))
            else:
                prop += f"{i}\n"
    md_tokens.append(
        Token("EOF", "", f"end of last line", "EOF"))
    return Token_List(md_tokens), prop_to_dict(prop[:-1] + prop_app)
