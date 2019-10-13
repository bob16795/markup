from markup.nodes import nullNode, Node


def match_first(tokens, matches):
    """
    if the first token matches any parser in the matches list 
    """
    for j in matches:
        node = j(tokens)
        if type(node) != nullNode:
            return node
    return nullNode()


def match_star(tokens, With):
    """
    matches until With dosent match

    tokens: the Token_list object
    With:   the parser to match
    """
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
        "TAGC": ">",  # FIX: dupe tokens
        "TAB": "\t",
        "NEWLINE": "\n",
    }

    while consumed < tokens.length():
        node = parser(tokens.offset(consumed))
        if type(node) == nullNode:
            if tokens.grab(consumed).value == "SYM":
                try:
                    node = Node(
                        matched_nodes[-1].type, sym_dict[tokens.grab(consumed).type], 1)
                except:
                    node = Node(
                        "TEXT", sym_dict[tokens.grab(consumed).type], 1)
            else:
                break
        matched_nodes.append(node)
        consumed += node.consumed
    return matched_nodes, consumed


def match_star_merge(tokens, With):
    """
    matches while merging like tokens

    tokens: the Token_list object
    With:   what to match
    """
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
        "TAGC": ">",  # FIX: dupe tokens
        "TAB": "\t",
        "NEWLINE": "\n",
    }

    while consumed < tokens.length():
        node = parser(tokens.offset(consumed))
        if type(node) == nullNode:
            if tokens.grab(consumed).value == "SYM":
                try:
                    node = Node(
                        matched_nodes[-1].type, sym_dict[tokens.grab(consumed).type], 1)
                except:
                    node = Node(
                        "TEXT", sym_dict[tokens.grab(consumed).type], 1)
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
    """
    matches while merging like tokens will err if theres a symbol

    tokens: the Token_list object
    With:   what to match
    """
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
    """
    matches while until the until is not nullnode

    tokens:  the Token_list object
    matches: what to match
    until:   what stops the matching
    """
    matched_nodes = []
    consumed = 0
    sym_dict = {
        "UNDERSCORE": "_",
        "GRAVE": "`",
        "STAR": "*",
        "PLUS": "+",
        "MINUS": "-",
        "HASH": "#",
        "TAGO": "<",
        "TAGC": ">",
        "TAB": "\t",
        "NEWLINE": "\n",
    }
    force_break = False
    while consumed < tokens.length() and not force_break:
        node = match_first(tokens.offset(consumed), matches)
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
            node = match_first(tokens.offset(consumed), matches)
        matched_nodes.append(node_cached)
        consumed += node.consumed
    return matched_nodes, consumed

