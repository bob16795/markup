class blank():
    def __init__(self, out):
        pass

    def __iadd__(self, out):
        pass

    def format(self, **options):
        pass


class Formater():
    def __init__(self, f):
        self.f = f
    # pygments formater class

    def fmt(self):
        f = blank
        f.__init__ = self.f.fmt_init
        f.format = self.f.fmt_format
        return f
    # output class

    def outer(self, *args, **kwargs):
        f = blank
        f.__init__ = self.f.outer_init
        f.__iadd__ = self.f.outer_add
        return f
    # misc

    def start(self, *args, **kwargs):
        f = self.f.start
        return f

    def end(self, *args, **kwargs):
        f = self.f.end
        return f

    def tag(self, *args, **kwargs):
        f = self.f.tag
        return f
    # text

    def add_new_line(self, *args, **kwargs):
        f = self.f.add_new_line
        return f

    def add_text(self, *args, **kwargs):
        f = self.f.add_text
        return f

    def bold_text(self, *args, **kwargs):
        f = self.f.bold_text
        return f

    def emph_text(self, *args, **kwargs):
        f = self.f.emph_text
        return f
    # code

    def start_code(self, *args, **kwargs):
        f = self.f.start_code
        return f

    def code_line(self, *args, **kwargs):
        f = self.f.code_line
        return f

    def end_code(self, *args, **kwargs):
        f = self.f.end_code
        return f
    # headers

    def add_header_1(self, *args, **kwargs):
        f = self.f.add_header_1
        return f

    def add_header_2(self, *args, **kwargs):
        f = self.f.add_header_2
        return f

    def add_header_3(self, *args, **kwargs):
        f = self.f.add_header_3
        return f
    # lists

    def start_list(self, *args, **kwargs):
        f = self.f.start_list
        return f

    def start_list_1(self, *args, **kwargs):
        f = self.f.start_list_1
        return f

    def start_list_2(self, *args, **kwargs):
        f = self.f.start_list_2
        return f

    def start_list_3(self, *args, **kwargs):
        f = self.f.start_list_3
        return f

    def add_list_text(self, *args, **kwargs):
        f = self.f.add_list_text
        return f

    def bold_list_text(self, *args, **kwargs):
        f = self.f.bold_list_text
        return f

    def emph_list_text(self, *args, **kwargs):
        f = self.f.emph_list_text
        return f

    def end_list(self, *args, **kwargs):
        f = self.f.end_list
        return f
