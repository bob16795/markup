import hashlib


class catalog_object():
    def __init__(self):
        self.dict = {"/Pages": None}

    def add_pages(self, pages):
        self.dict["/Pages"] = pages

    def ident(self):
        return hashlib.md5(self.__str__().encode('utf-8')).hexdigest()

    def __str__(self):
        text = "<</Type /Catalog\n"
        for i in self.dict:
            text += i.__str__() + " %%" + self.dict[i].ident() + "%%\n"
        text += f">>\n"
        return text


class pages_object():
    def __init__(self):
        self.pages = []

    def ident(self):
        return hashlib.md5(self.__str__().encode('utf-8')).hexdigest()

    def append(self, page):
        self.pages.append(page)

    def current(self):
        return self.pages[-1]

    def __str__(self):
        text = "<<\n/Type /Pages\n/Kids ["
        for i in self.pages:
            text += " %%" + i.ident() + "%%"
        text += f"]\n/Count {len(self.pages)}\n>>\n"
        return text


class outlines_object():
    def __init__(self):
        self.dict = []

    def ident(self):
        return hashlib.md5(self.__str__().encode('utf-8')).hexdigest()

    def __str__(self):
        text = "<</Type /Outline\n"
        for i in self.dict:
            text += i.__str__() + " %%" + self.dict[i].ident() + "%%\n"
        text += f">>\n"
        return text


class page_object():
    def __init__(self, font):
        self.text_objs = []
        self.font = font

    def ident(self):
        return hashlib.md5(self.__str__().encode('utf-8')).hexdigest()

    def append(self, text):
        self.text_objs.append(text)

    def __str__(self):
        text = "<<\n/Type /Page\n/Contents ["
        for i in self.text_objs:
            text += " %%" + i.ident() + "%%"
        text += f"]\n/MediaBox [ 0 0 612 792 ]\n/Resources <</Font << /F1 %%{self.font.ident()}%% >>\n>>\n>>\n"
        return text


class text_object():
    def __init__(self):
        self.stream = ""

    def ident(self):
        return hashlib.md5(self.__str__().encode('utf-8')).hexdigest()

    def append(self, text):
        self.stream += text

    def __str__(self):
        text = f"<< /Length {len(self.stream)}>>\n"
        text += f"stream\n{self.stream}\nendstream\n"
        return text


class font_object():
    """
    << /Type /Font
    /Subtype /Type1
    /Name /F1
    /BaseFont /Times 
    /Encoding /MacRomanEncoding
    >>
    """

    def __init__(self, name="F1"):
        self.dict = {"/Type": "/Font",
                     "/Subtype": "/Type1",
                     "/Name": name,
                     "/BaseFont": "/Times",
                     "/Encoding": "/MacRomanEncoding"}

    def add_pages(self, pages):
        self.dict["/Pages"] = pages

    def ident(self):
        return hashlib.md5(self.__str__().encode('utf-8')).hexdigest()

    def __str__(self):
        text = "<</Type /Catalog\n"
        for i in self.dict:
            text += i.__str__() + " " + self.dict[i].__str__() + "\n"
        text += f">>\n"
        return text
