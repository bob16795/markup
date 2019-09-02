from docx.shared import RGBColor
from docx import Document
from markup.decorators import Formater
from pygments.formatter import Formatter
import subprocess

@Formater
class terminal():
    def outer_init(self, out, info):
        self.out = out

    def outer_add(self, out):
        self.out += out
        return self

    def fmt_init(self, **options):
        Formatter.__init__(self, **options)

    def fmt_format(self, tokensource, outfile):
        lastval = ''
        lasttype = None
        for ttype, value in tokensource:
            if ttype == lasttype:
                lastval += value
            else:
                if lastval:
                    outfile += lastval
                lastval = value
                lasttype = ttype
        if lastval:
            outfile += lastval.replace("\n", "")

    def add_new_line():
        return "\n"

    def add_text(text):
        return text

    def emph_text(text):
        return text

    def start():
        return ""

    def bold_text(text):
        return text

    def add_header_1(text):
        text = "\n" + text + "\n" + (len(text) * "=") + "\n"
        return text

    def add_header_2(text):
        text = "\n" + text + "\n" + (len(text) * "-") + "\n"
        return text

    def add_header_3(text):
        text = "\n" + text + "\n"
        return text

    def start_list():
        return "\n-"

    def start_code():
        return "\n"

    def code_line(text):
        return ">  " + text + "\n"

    def end_code():
        return ""

    def start_list_1(l):
        return "\n-"

    def start_list_2(l):
        return "\n  -"

    def start_list_3(l):
        return "\n    -"

    def end_list(l):
        return "\n"

    def emph_list_text(text):
        return text

    def bold_list_text(text):
        return text

    def add_list_text(text):
        return text

    def end(out):
        out += "\n"
        return out.out.encode()

    def tag(text):
        return f"link: [{text}]"


@Formater
class html():
    def outer_init(self, out, info):
        self.out = out

    def outer_add(self, out):
        self.out += out
        return self

    def fmt_init(self, **options):
        Formatter.__init__(self, **options)

        self.styles = {}

        for token, style in self.style:
            start = end = ''

            if style['color']:
                start += '<font color="#%s">' % style['color']
                end = '</font>' + end
            if style['bold']:
                start += '<b>'
                end = '</b>' + end
            if style['italic']:
                start += '<i>'
                end = '</i>' + end
            if style['underline']:
                start += '<u>'
                end = '</u>' + end
            self.styles[token] = (start, end)

    def fmt_format(self, tokensource, outfile):
        lastval = ''
        lasttype = None
        outfile += '<pre>'
        for ttype, value in tokensource:
            while ttype not in self.styles:
                ttype = ttype.parent
            if ttype == lasttype:
                lastval += value
            else:
                if lastval:
                    stylebegin, styleend = self.styles[lasttype]
                    outfile += stylebegin + lastval + styleend
                lastval = value
                lasttype = ttype
        if lastval:
            stylebegin, styleend = self.styles[lasttype]
            outfile += stylebegin + lastval + styleend
            outfile += '</pre>\n'

    def start():
        return "<!DOCTYPE html>\n<html>\n<head>\n<link rel=\"stylesheet\" href=\"main.css\">\n</head>\n<body>\n<div id=\"page\">"

    def add_text(text):
        return text

    def add_new_line():
        return "<br/>"

    def emph_text(text):
        return "<em>" + text + "</em>"

    def bold_text(text):
        return "<b>" + text + "</b>"

    def add_header_1(text):
        return "<h1>" + text + "</h1>"

    def add_header_2(text):
        return "<h2>" + text + "</h2>"

    def add_header_3(text):
        return "<h3>" + text + "</h3>"

    def start_code():
        return "\n"

    def code_line(text):
        return "" + text + "\n"

    def end_code():
        return ""

    def start_list():
        return "<ul><li>"

    def start_list_1(l):
        if l == 1:
            return "</li><li>"
        if l == 2:
            return "</li></ul><li>"
        if l == 3:
            return "</li></ul></ul><li>"

    def start_list_2(l):
        if l == 1:
            return "</li><ul><li>"
        if l == 2:
            return "</li><li>"
        if l == 3:
            return "</li></ul><li>"

    def start_list_3(l):
        if l == 1:
            return "</li><ul><ul><li>"
        if l == 2:
            return "</li><ul><li>"
        if l == 3:
            return "</li><li>"

    def end_list(l):
        if l == 1:
            return "</li></ul>"
        if l == 2:
            return "</li></ul></ul>"
        if l == 3:
            return "</li></ul></ul></ul>"

    def emph_list_text(text):
        return "<em>" + text + "</em>"

    def bold_list_text(text):
        return "<b>" + text + "</b>"

    def add_list_text(text):
        return text

    def end(out):
        out += "</div>\n</body>\n</html>"
        return out.out.encode()

    def tag(text):
        if "](" in text:
            text = text.split("](")
            link = text[0]
            text = text[-1]
        else:
            text = text.split(": ")
            link = text[0]
            text = text[-1]
        return f"<a href={text}> {link} </a><br/>"


@Formater
class docx():
    def outer_init(self, out, info):
        if "template" in info:
            self.doc = Document(info["template"])
        else:
            self.doc = Document()

    def outer_add(self, out):
        for i in out:
            ttype = i.split(": ")[0]
            text = i.split(": ")[-1]
            if ttype == "\n":
                self.p = None
            elif ttype == "H1":
                self.doc.add_heading(text, 1)
                self.p = None
            elif ttype == "H2":
                self.doc.add_heading(text, 2)
                self.p = None
            elif ttype == "H3":
                self.doc.add_heading(text, 3)
                self.p = None
            elif ttype == "BOLD":
                if self.p == None:
                    self.p = self.doc.add_paragraph()
                self.r = self.p.add_run(text)
                self.r.bold = True
            elif ttype == "EMPH":
                if self.p == None:
                    self.p = self.doc.add_paragraph()
                self.r = self.p.add_run(text)
                self.r.italic = True
            else:
                if self.p == None:
                    self.p = self.doc.add_paragraph()
                self.r = self.p.add_run(text)
        return self

    def fmt_init(self, **options):
        Formatter.__init__(self, **options)

        # create a dict of (start, end) tuples that wrap the
        # value of a token so that we can use it in the format
        # method later
        self.styles = {}

        # we iterate over the `_styles` attribute of a style item
        # that contains the parsed style values.
        for token, style in self.style:
            # a style item is a tuple in the following form:
            # colors are readily specified in hex: 'RRGGBB'
            if style['color'] == None:
                color = RGBColor.from_string("000000")
            else:
                color = RGBColor.from_string(style['color'])
            self.styles[token] = (color, style['bold'],
                                  style['italic'], style['underline'])

    def fmt_format(self, tokensource, outfile):
        # lastval is a string we use for caching
        # because it's possible that an lexer yields a number
        # of consecutive tokens with the same token type.
        # to minimize the size of the generated html markup we
        # try to join the values of same-type tokens here
        lastval = ''
        lasttype = None
        doc = outfile
        self.p = doc.add_paragraph(style="Source Code")
        # wrap the whole output with <pre>

        for ttype, value in tokensource:
            # if the token type doesn't exist in the stylemap
            # we try it with the parent of the token type
            # eg: parent of Token.Literal.String.Double is
            # Token.Literal.String
            while ttype not in self.styles:
                ttype = ttype.parent
            if ttype == lasttype:
                # the current token type is the same of the last
                # iteration. cache it
                lastval += value
            else:
                # not the same token as last iteration, but we
                # have some data in the buffer. wrap it with the
                # defined style and write it to the output file
                if lastval:
                    color, bold, italic, underline = self.styles[lasttype]
                    r = self.p.add_run(lastval)
                    r.font.color.rgb = color
                    r.font.bold = bold
                    r.font.italic = italic
                    r.font.underline = underline
                # set lastval/lasttype to current5 values
                lastval = value
                lasttype = ttype

        # if something is left in the buffer, write it to the
        if lastval:
            color, bold, italic, underline = self.styles[lasttype]
            r = self.p.add_run(lastval.replace("\n", ""))
            r.font.color.rgb = color
            r.font.bold = bold
            r.font.italic = italic
            r.font.underline = underline

    def start():
        return []

    def add_text(text):
        return [text]

    def add_new_line():
        return ["\n"]

    def emph_text(text):
        return [f"EMPH: {text}"]

    def bold_text(text):
        return [f"BOLD: {text}"]

    def add_header_1(text):
        return [f"H1: {text}"]

    def add_header_2(text):
        return [f"H2: {text}"]

    def add_header_3(text):
        return [f"H3: {text}"]

    def start_code():
        return ["\n"]

    def code_line(text):
        return [text, "\n"]

    def end_code():
        return []

    def start_list():
        return []

    def start_list_1(l):
        return [f"L1: "]

    def start_list_2(l):
        return [f"L2: "]

    def start_list_3(l):
        return [f"L3: "]

    def end_list(l):
        return []

    def emph_list_text(text):
        return [f"EMPH: {text}"]

    def bold_list_text(text):
        return [f"BOLD: {text}"]

    def add_list_text(text):
        return [f"{text}"]

    def end(out):
        out.doc.save("/tmp/tmp.docx")
        with open("/tmp/tmp.docx", "rb") as f:
            text = f.read()
        return text

    def tag(text):
        if "](" in text:
            text = text.split("](")
            link = text[0]
            text = text[-1]
        else:
            text = text.split(": ")
            link = text[0]
            text = text[-1]
        return [f"<a href={text}> {link} </a><br/>"]


@Formater
class pdf_groff():
    def outer_init(self, out, info):
        self.pp = False
        self.title_heading_level = 0
        self.author = ""
        self.title  = ""
        if "author" in  info:
            self.author = info["author"]
        if "title" in  info:
            self.title = info["title"]
            if "title_page" in info:
                out += "\n()TTL()\n.bp\n"
        if "title_head" in info:
            self.title_heading_level = int(info["title_head"])

        out = out.replace("()TTL()", self.title)
        out = out.replace("()AUT()", self.author)
        self.out = out

    def outer_add(self, out):
        out = out.replace("()HL1()", str(self.title_heading_level))
        out = out.replace("()HL2()", str(self.title_heading_level + 1))
        out = out.replace("()HL3()", str(self.title_heading_level + 2))
        if not out == "":
            if out[0] == "\n" or out[:3] == ".SH" or \
                    out[:3] == "LI;":
                if out[:3] == "LI;":
                    out = out[3:]
                elif self.out[-1] != "\n":
                    self.out += "\n"
                self.pp = False
            elif self.pp == False:
                if self.out[-1] != "\n":
                    self.out += "\n"
                self.pp = True
                self.out += ".PP\n"
            if not out == "\n":
                self.out += out
        return self

    def fmt_init(self, **options):
        Formatter.__init__(self, **options)
        self.styles = {}
        for token, style in self.style:
            if style['color'] == None:
                color = "000000"
            else:
                color = style['color']
            self.styles[token] = (color, style['bold'],
                                  style['italic'], style['underline'])

    def fmt_format(self, tokensource, outfile):
        lastval = ''
        lasttype = None
        outfile += "\n.in 0\n.fcolor gray\n.LP\n"
        indent = 0
        for ttype, value in tokensource:
            if not(value.strip(" ")):
                indent = len(value)-len(value.strip(" "))
            if lastval.strip(" "):
                color = self.styles[lasttype][0]
                val = lastval.replace('\n', f'\n.in {float(indent/6)}c\n')
                outfile += f".defcolor pyg rgb #{color}\n.gcolor pyg\n{val}\n.gcolor\n"
            # set lastval/lasttype to current values
            lastval = value
            lasttype = ttype
        if lastval.strip(" "):
            color = self.styles[lasttype][0]
            val = lastval.replace('\n', f'\n.in {float(indent/6)}c\n')
            outfile += f".defcolor pyg rgb #{color}\n.gcolor pyg\n{val}\n.gcolor\n"
        # set lastval/lasttype to current values
        lastval = value
        lasttype = ttype
        outfile += f".fcolor\n"

    def add_new_line():
        return f"\n"

    def add_text(text):
        if text.strip(" ") != "":
            return f"{text}\n"
        return ""

    def emph_text(text):
        return f".UL \"{text}\"\n"

    def start():
        # \\X'papersize=5.5i,8.5i'\n
        return "\n.OH '''%'\n.EH '''%'\n.nr PO .3i\n.nr LL 7.4i\n.nr FM .5i\n.nr HM .3i\n.nr LT 7.4i\n.color 1\n.OF '()AUT()'''\n.EF '''()TTL()'\n"

    def bold_text(text):
        return f".B {text}\n"

    def add_header_1(text):
        return f".OH '%'-{text}-''\n.EH ''-{text}-'%'\n.bp\n.NH ()HL1()\n{text}\n.XS\n.B\n{text}\n.XE\n.PP\n"

    def add_header_2(text):
        return f".NH ()HL2()\n{text}\n.XS\n\t{text}\n.XE\n.PP\n"

    def add_header_3(text):
        return f".NH ()HL3()\n{text}\n.XS\n\t\t{text}\n.XE\n.PP\n"

    def start_list():
        return ".IP \\(bu 2\n"

    def start_code():
        return "LI;\n.LP\n"

    def code_line(text):
        return text.replace("\\TS", "#\\.RS\n")\
            .replace("\\TE", "#\\.RE\n") + "\n"

    def end_code():
        return ""

    def start_list_1(l):
        if l == 1:
            return ".IP \\(bu 2\n"
        if l == 2:
            return ".RE\n.IP \\(bu 2\n"
        if l == 3:
            return ".RE\n.RE\n.IP \\(bu 2\n"

    def start_list_2(l):
        if l == 1:
            return ".RS\n.IP \\(bu 2\n"
        if l == 2:
            return ".IP \\(bu 2\n"
        if l == 3:
            return ".RE\n.IP \\(bu 2\n"

    def start_list_3(l):
        if l == 1:
            return ".RS\n.RS\n.IP \\(bu 2\n"
        if l == 2:
            return ".RS\n.IP \\(bu 2\n"
        if l == 3:
            return ".IP \\(bu 2\n"

    def end_list(l):
        if l == 1:
            return ""
        if l == 2:
            return ".RE\n"
        if l == 3:
            return ".RE\n.RE\n"

    def emph_list_text(text):
        return f"LI;{text}"

    def bold_list_text(text):
        return f"LI;{text}"

    def add_list_text(text):
        return f"LI;{text}"

    def end(out):
        out += ".OH '%'-Table Of Contents-''\n.EH ''-Table Of Contents-'%'\n.de TOC\n.MC 155p .3i\n.SH\nTable Of Contents\n..\n.TC"
        out.out = out.out.replace("\n\n", "\n")
        o = subprocess.Popen(f"groff -Tpdf -dpaper=a4 -P-pa4 -ms".split(" "), stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        return o.communicate(input=out.out.encode())[0]

    def tag(text):
        if "](" in text:
            text = text.split("](")
            link = text[0]
            text = text[-1]
        else:
            text = text.split(": ")
            link = text[0]
            text = text[-1]
        if link == "COL":
            return f"\n.MC {text}i\n"
        if link == "CPT":
            if text[-1] == "!":
                return f"\n.bp\n.NH 0\n{text[:-1]}\n"
            else:
                return f".OH '%'-Table Of Contents-''\n.EH ''-Table Of Contents-'%'\n.de TOC\n.MC 155p .3i\n.SH\nTable Of Contents\n..\n.TC\n.bp\n.NH 0\n{text}\n.rm toc*div\n.rm toc*num\n"
        # return f"<a href={text}> {link} </a><br/>"
        return f"{text}\n"

class pdf_latex():
    def outer_init(self, out, info):
        self.pp = False
        self.title_heading_level = 0
        self.author = ""
        self.title  = ""
        if "author" in  info:
            self.author = info["author"]
        if "title" in  info:
            self.title = info["title"]
            if "title_page" in info:
                #   \begin{titlepage}
                #     \begin{center}
                #         \vspace*{1cm}
                #         \Huge
                #         \textbf{Thesis Title}
                #         \vspace{2.0cm}
                #         \textbf{Author Name}
                #         \vfill
                #         A thesis presented for the degree of\\
                #         Doctor of Philosophy
                #         \vspace{0.8cm}
                #         \includegraphics[width=0.4\textwidth]{university}
                #         \Large
                #         Department Name\\
                #         University Name\\
                #         Country\\
                #         Date
                #     \end{center}
                # \end{titlepage}
                out += "\\begin{titlepage}\n\\begin{center}\\vspace*{1cm}\n\\Huge\n\\textbf{()TTL()}\n\\vspace{2.0cm}\n\textbf{()AUT()}\n\\end{center}\n\\end{titlepage}"
        if "title_head" in info:
            self.title_heading_level = int(info["title_head"])

        out = out.replace("()TTL()", self.title)
        out = out.replace("()AUT()", self.author)
        self.out = out

