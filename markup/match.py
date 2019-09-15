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
        "TAGO": "[",
        "TAGC": ")",#FIX: dupe tokens
        "TAB": "\t",
        "NEWLINE": "\n",
    }

    while consumed < tokens.length():
        node = parser(tokens.offset(consumed))
        if type(node) == nullNode:
            if tokens.grab(consumed).value == "SYM":
                try:
                   node = Node(matched_nodes[-1].type, sym_dict[tokens.grab(consumed).type], 1)
                except:
                   node = Node("TEXT", sym_dict[tokens.grab(consumed).type], 1)  
            else:
                break
        matched_nodes.append(node)
        consumed += node.consumed
    return matched_nodes, consumed

def match_star_merge(tokens, With):
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
        "TAGO": "[",
        "TAGC": ")",#FIX: dupe tokens
        "TAB": "\t",
        "NEWLINE": "\n",
    }

    while consumed < tokens.length():
        node = parser(tokens.offset(consumed))
        if type(node) == nullNode:
            if tokens.grab(consumed).value == "SYM":
                try:
                   node = Node(matched_nodes[-1].type, sym_dict[tokens.grab(consumed).type], 1)
                except:
                   node = Node("TEXT", sym_dict[tokens.grab(consumed).type], 1)  
            else:
                break
        if matched_nodes != []:
            if matched_nodes[-1].type == node.type:
                matched_nodes[-1].value += node.value
                matched_nodes[-1].consumed += node.consumed
            else:
                matched_nodes.append(node)
        else:
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

def match_multi_star_until(tokens, matches, until):
    matched_nodes = []
    consumed = 0
    sym_dict = {
        "UNDERSCORE": "_",
        "GRAVE": "`",
        "STAR": "*",
        "PLUS": "+",
        "MINUS": "-",
        "HASH": "#",
        "TAGO": "[",
        "TAGC": ")",
        "TAB": "\t",
        "NEWLINE": "\n",
    }
    force_break = False
    while consumed < tokens.length() and not force_break:
        node = match_first(tokens.offset(consumed),matches)
        node_cached = Node("TEXT", "", 0)
        while tokens.grab(consumed).type != "NEWLINE":
            if type(until(tokens.offset(consumed))) != nullNode:
                force_break = True
                break
            if type(node) == nullNode:
                if tokens.grab(consumed).value == "SYM":
                    node_cached.consumed += 1
                    node_cached.value += sym_dict[tokens.grab(consumed).type]
                else:
                    force_break = True
                    break
            else:
                node_cached.value += node.value
                node_cached.consumed += node.consumed
            consumed += node.consumed
            node = match_first(tokens.offset(consumed),matches)
        matched_nodes.append(node_cached)
        consumed += node.consumed
    return matched_nodes, consumed

def match_text(tokens):
    consumed = 0
    sym_dict = {
        "UNDERSCORE": "_",
        "GRAVE": "`",
        "STAR": "*",
        "PLUS": "+",
        "MINUS": "-",
        "HASH": "#",
        "TAGO": "[",
        "TAGC": ")",
        "NEWLINE": "\n",
    }
    if tokens.peek(["TEXT"]):
        node = Node("TEXT", tokens.grab(0).value, 1)
    else:
        node = nullNode()
    node_cached = Node("TEXT", "", 0)
    while tokens.grab(consumed).type != "NEWLINE":
        if type(node) == nullNode:
            if tokens.grab(consumed).value == "SYM":
                node_cached.consumed += 1
                node_cached.value += sym_dict[tokens.grab(consumed).type]
            else:
                break
        else:
            node_cached.value += node.value
            node_cached.consumed += node.consumed
        consumed += node.consumed
        if tokens.peek_at(consumed, ["TEXT"]):
            node = Node("TEXT", tokens.grab(0).value, 1)
        else:
            node = nullNode()
    return node_cached
