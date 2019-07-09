from markup.token_class import *
import os
import re


def yaml_dict(yaml):
    yaml_cached = yaml.split("\n")
    yaml_d = {}
    for i in yaml_cached:
        j = i.split(": ")
        yaml_d[j[0]] = j[1]
    return yaml_d


def tokenize_f(file, inside=False):
    with open(file, encoding='utf-8') as filew:
        file_cached = ""
        for i in filew:
            if i[:5] == "Inc: ":
                for pattern in i[5:-1].split("; "):
                    for f in os.listdir():
                        if re.search(pattern, f):
                            try:
                                file_cached = f"{file_cached}{tokenize_f(f, True)}\n"
                            except:
                                pass
                file_cached = file_cached[:-1]
            else:
                file_cached = f"{file_cached}{i}"
    return file_cached


def tokenize(file):
    file_cached = tokenize_f(file)
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
        "\n": ["NEWLINE", ""],
    }
    md_tokens = []
    yaml = ""
    ignore = 0
    for x, i in enumerate(file_cached):
        text = ""
        l = i
        if l == "---":
            mu = not(mu)
        else:
            if mu:
                for y, j in enumerate(l):
                    if ignore != 0:
                        ignore -= 1
                        text = f"{text}{j}"
                    else:
                        if j == "\\":
                            ignore = 1
                        elif j in token_dict:
                            if text != "":
                                md_tokens.append(
                                    Token("TEXT", text, f"line {x+1}, col {y}"))
                                text = ""
                            token = token_dict[j]
                            md_tokens.append(
                                Token(token[0], token[1], f"line {x+1}, col {y}"))
                        else:
                            text = f"{text}{j}"
                if text != "":
                    md_tokens.append(Token("TEXT", text, f"end of line {x+1}"))
                md_tokens.append(Token("NEWLINE", "", f"end of line {x+1}"))
            else:
                yaml += f"{l}\n"
    md_tokens.append(Token("EOF", "", f"End"))
    return Token_List(md_tokens), yaml_dict(yaml[:-1])
