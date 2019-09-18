class Node():
    def __init__(self, type, value, consumed):
        self.type = type
        self.value = value
        self.consumed = consumed

    def __str__(self):
        return(f"<Sentence type: {self.type}, value: \"{self.value}\", Consumed: {self.consumed}>")


class nullNode():
    def __init__(self):
        self.type = None
        self.consumed = 1

    def __str__(self):
        return(f"<Null Consumed: {self.consumed}>")


class BodyNode():
    def __init__(self, paragraphs, consumed):
        self.paragraphs = paragraphs
        self.consumed = consumed

    def __str__(self):
        j = ""
        for i in self.paragraphs:
            j += i.__str__()
        return(f"<Body Paragprphs: {j}, Consumed: {self.consumed}>")


class ParagraphNode():
    def __init__(self, sentences, consumed):
        self.sentences = sentences
        self.consumed = consumed

    def __str__(self):
        j = ""
        for i in self.sentences:
            j += i.__str__() + ","
        return(f"<Paragraph sentences: {j[:-1]}, Consumed: {self.consumed}>")


class ListNode():
    def __init__(self, sentences, consumed):
        self.sentences = sentences
        self.consumed = consumed

    def __str__(self):
        j = ""
        for i in self.sentences:
            j += i.__str__() + ","
        return(f"<List sentences: {j[:-1]}, Consumed: {self.consumed}>")


class CodeNode():
    def __init__(self, sentences, consumed, value):
        self.sentences = sentences
        self.consumed = consumed
        self.value = value

    def __str__(self):
        j = ""
        for i in self.sentences:
            j += i.__str__() + ","
        return(f"<Code Type: {self.value}, sentences: {j[:-1]}, Consumed: {self.consumed}>")


class HeadNode():
    def __init__(self, type, value, consumed):
        self.type = type
        self.value = value
        self.consumed = consumed

    def __str__(self):
        return(f"<Head type: {self.type}, value: \"{self.value}\", Consumed: {self.consumed}>")
