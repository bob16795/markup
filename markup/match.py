from markup.nodes import nullNode, Node

def match_first(tokens, matches):
    for j in matches:
        node = j(tokens)
        if type(node) != nullNode:
            return node
    return nullNode()


def match_star(tokens, With):
    matched_nodes = []
    consumed = 0
    parser = With
    sym_dict = {
        "UNDERSCORE": "_",
        "GRAVE": "`",
        "STAR": "*",
        "PLUS": "+",
        "MINUS": "-",
        "HASH": "#",
        "TAGO": "<",
        "TAGC": ">",
        "NEWLINE": "\n",
    }

    while consumed < tokens.length():
        node = parser(tokens.offset(consumed))
        if type(node) == nullNode:
            if tokens.grab(consumed).value == "SYM":
                node = Node("TEXT", sym_dict[tokens.grab(consumed).type], 1)
            else:
                break
        matched_nodes.append(node)
        consumed += node.consumed
    return matched_nodes, consumed


def match_star_err(tokens, With):
    matched_nodes = []
    consumed = 0
    parser = With

    while consumed < tokens.length():
        node = parser(tokens.offset(consumed))
        if type(node) == nullNode:
            break
        matched_nodes.append(node)
        consumed += node.consumed
    return matched_nodes, consumed
