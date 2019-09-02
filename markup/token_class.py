class Token():
    def __init__(self, type, value, at):
        self.type = type
        self.value = value
        self.at = at

    def __str__(self):
        return(f"<type: {self.type}, value: {self.value}>")

class Token_List():
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
