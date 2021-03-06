class Token():
    def __init__(self, type, value, at, context):
        self.type = type
        self.value = value
        self.at = at
        self.context = context

    def __str__(self):
        return("<type: %s, value: %s>" % (self.type, self.value))


class Token_List():
    """
    a list of tokens with tools
    """

    def __str__(self):
        tokens = ""
        for token in self.tokens:
            tokens += token.__str__()
        return tokens

    def __init__(self, tokens):
        self.tokens = tokens

    def length(self):
        return len(self.tokens)

    def peek_or(self, choices):
        for choice in choices:
            if self.peek(choice):
                return True
        return False

    def peek(self, types):
        peeked = [i.type for i in self.tokens[:(len(types))]]
        if peeked == types:
            return True
        return False

    def peek_at(self, index, types):
        return self.offset(index).peek(types)

    def offset(self, index):
        if index == 0:
            return self
        return Token_List(self.tokens[index:])

    def grab(self, index):
        return self.tokens[index]

    def grab_num(self, index, num):
        return self.tokens[index:index+num]
