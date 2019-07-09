import markup.markup_parser as parser


def parse_markdown(tokens):
    body = parser.Parse_Body(tokens)
    if body.consumed != -1 + tokens.length():
        print(f"error at {tokens.grab(body.consumed-1).at}")
    return body
