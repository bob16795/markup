import markup.parser as parser


def parse_markdown(tokens):
    body = parser.Body_Parser(tokens)
    if body.consumed != -1 + tokens.length():
        if not tokens.grab(body.consumed-1).at == "End":
            print(f"error at {tokens.grab(body.consumed-1).at}")
    return body
