class Node():
    def __init__(self, type, value, consumed):
        self.type = type
        self.value = value
        self.consumed = consumed

    def __str__(self):
        return("<Sentence type: %s, value: \"%s\", Consumed: %s>" % (self.type, self.value, self.consumed))


class nullNode():
    def __init__(self):
        self.type = None
        self.consumed = 1

    def __str__(self):
        return("<Null Consumed: %s>" % self.consumed)


class BodyNode():
    def __init__(self, paragraphs, consumed):
        self.paragraphs = paragraphs
        self.consumed = consumed

    def __str__(self):
        j = ""
        for i in self.paragraphs:
            j += i.__str__()
        return("<Body Paragprphs: %s, Consumed: %s>" % (j, self.consumed))


class ParagraphNode():
    def __init__(self, sentences, consumed):
        self.sentences = sentences
        self.consumed = consumed

    def __str__(self):
        j = ""
        for i in self.sentences:
            j += i.__str__() + ","
        return("<Paragraph sentences: %s, Consumed: %s>" % (j[:-1], self.consumed))


class ListNode():
    def __init__(self, sentences, consumed):
        self.sentences = sentences
        self.consumed = consumed

    def __str__(self):
        j = ""
        for i in self.sentences:
            j += i.__str__() + ","
        return("<List sentences: %s, Consumed: %s>" % (j[:-1], self.consumed))


class CodeNode():
    def __init__(self, sentences, consumed, value):
        self.sentences = sentences
        self.consumed = consumed
        self.value = value

    def __str__(self):
        j = ""
        for i in self.sentences:
            j += i.__str__() + ","
        return("<Code sentences: %s, Consumed: %s>" % (j[:-1], self.consumed))


class HeadNode():
    def __init__(self, type, value, consumed):
        self.type = type
        self.value = value
        self.consumed = consumed

    def __str__(self):
        return("<Head type: %s, value: \"%s\", Consumed: %s>" % (self.type, self.value, self.consumed))
