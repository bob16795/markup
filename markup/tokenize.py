from markup.token_class import Token, Token_List

def yaml_dict(yaml):
    if yaml.strip(" \n") != "":
      yaml_cached = yaml.split("\n")
      yaml_d = {"slave" : "False"}
      for i in yaml_cached:
          j = i.split(":")
          if i.split(" | ")[0] == "s" and yaml_d['slave'] == "True":
              yaml_d[j[0].split(" | ")[1]] = j[1].strip(" ")
          elif i.split(" | ")[0] == "m" and yaml_d['slave'] == "False":
              yaml_d[j[0].split(" | ")[1]] = j[1].strip(" ")
          elif not " | " in i:
              yaml_d[j[0]] = j[1].strip(" ")
      return yaml_d
    else:
      return {}


def tokenize(file_cached, yaml_app):
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
    return Token_List(md_tokens), yaml_dict(yaml[:-1] + yaml_app)