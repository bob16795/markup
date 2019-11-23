# from docx.shared import RGBColor
# from docx import Document
from markup.decorators import Formater
from pygments.formatter import Formatter
import subprocess
import tempfile
import os
import re


@Formater
class terminal():
    def outer_init(self, out, prop):
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

    @staticmethod
    def add_new_line():
        return "\n"

    @staticmethod
    def add_text(text):
        return text

    @staticmethod
    def emph_text(text):
        return text

    @staticmethod
    def start():
        return ""

    @staticmethod
    def bold_text(text):
        return text

    @staticmethod
    def add_header_1(text):
        text = "\n" + text + "\n" + (len(text) * "=") + "\n"
        return text

    @staticmethod
    def add_header_2(text):
        text = "\n" + text + "\n" + (len(text) * "-") + "\n"
        return text

    @staticmethod
    def add_header_3(text):
        text = "\n" + text + "\n"
        return text

    @staticmethod
    def start_ulist():
        return "\n-"

    @staticmethod
    def start_code():
        return "\n"

    @staticmethod
    def code_line(text):
        return ">  " + text + "\n"

    @staticmethod
    def end_code():
        return ""

    @staticmethod
    def start_ulist_1(level):
        return "\n-"

    @staticmethod
    def start_ulist_2(level):
        return "\n  -"

    @staticmethod
    def start_ulist_3(level):
        return "\n    -"

    @staticmethod
    def end_ulist(level):
        return "\n"

    @staticmethod
    def emph_ulist_text(text):
        return text

    @staticmethod
    def bold_ulist_text(text):
        return text

    @staticmethod
    def add_ulist_text(text):
        return text

    @staticmethod
    def start_olist_1(level):
        return "\n*"

    @staticmethod
    def start_olist_2(level):
        return "\n  *"

    @staticmethod
    def start_olist_3(level):
        return "\n    *"

    @staticmethod
    def end_olist(level):
        return "\n"

    @staticmethod
    def emph_olist_text(text):
        return text

    @staticmethod
    def bold_olist_text(text):
        return text

    @staticmethod
    def add_olist_text(text):
        return text

    @staticmethod
    def end(out):
        out += "\n"
        return out.out.encode()

    @staticmethod
    def tag(text):
        return "link: [%s]" % text


@Formater
class html():
    @staticmethod
    def outer_init(self, out, prop):
        self.out = out

    @staticmethod
    def outer_add(self, out):
        self.out += out
        return self

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def start():
        return """
               <!DOCTYPE html>\\n<html>
               <head>
               <link rel=\"stylesheet\" href=\"main.css\">
               </head>
               <body>
               <div id=\"page\">
               """

    @staticmethod
    def add_text(text):
        return text

    @staticmethod
    def add_new_line():
        return "<br/>"

    @staticmethod
    def emph_text(text):
        return "<em>" + text + "</em>"

    @staticmethod
    def bold_text(text):
        return "<b>" + text + "</b>"

    @staticmethod
    def add_header_1(text):
        return "<h1>" + text + "</h1>"

    @staticmethod
    def add_header_2(text):
        return "<h2>" + text + "</h2>"

    @staticmethod
    def add_header_3(text):
        return "<h3>" + text + "</h3>"

    @staticmethod
    def start_code():
        return "\n"

    @staticmethod
    def code_line(text):
        return "" + text + "\n"

    @staticmethod
    def end_code():
        return ""

    @staticmethod
    def start_ulist():
        return "<ul><li>"

    @staticmethod
    def start_ulist_1(level):
        if level == 1:
            return "</li><li>"
        if level == 2:
            return "</li></ul><li>"
        if level == 3:
            return "</li></ul></ul><li>"

    @staticmethod
    def start_ulist_2(level):
        if level == 1:
            return "</li><ul><li>"
        if level == 2:
            return "</li><li>"
        if level == 3:
            return "</li></ul><li>"

    @staticmethod
    def start_ulist_3(level):
        if level == 1:
            return "</li><ul><ul><li>"
        if level == 2:
            return "</li><ul><li>"
        if level == 3:
            return "</li><li>"

    @staticmethod
    def end_ulist(level):
        if level == 1:
            return "</li></ul>"
        if level == 2:
            return "</li></ul></ul>"
        if level == 3:
            return "</li></ul></ul></ul>"

    @staticmethod
    def emph_ulist_text(text):
        return "<em>" + text + "</em>"

    @staticmethod
    def bold_ulist_text(text):
        return "<b>" + text + "</b>"

    @staticmethod
    def add_ulist_text(text):
        return text

    @staticmethod
    def start_olist():
        return "<ol><li>"

    @staticmethod
    def start_olist_1(level):
        if level == 1:
            return "</li><li>"
        if level == 2:
            return "</li></ol><li>"
        if level == 3:
            return "</li></ol></ol><li>"

    @staticmethod
    def start_olist_2(level):
        if level == 1:
            return "</li><ol><li>"
        if level == 2:
            return "</li><li>"
        if level == 3:
            return "</li></ol><li>"

    @staticmethod
    def start_olist_3(level):
        if level == 1:
            return "</li><ol><ol><li>"
        if level == 2:
            return "</li><ol><li>"
        if level == 3:
            return "</li><li>"

    @staticmethod
    def end_olist(level):
        if level == 1:
            return "</li></ol>"
        if level == 2:
            return "</li></ol></ol>"
        if level == 3:
            return "</li></ol></ol></ol>"

    @staticmethod
    def emph_olist_text(text):
        return "<em>" + text + "</em>"

    @staticmethod
    def bold_olist_text(text):
        return "<b>" + text + "</b>"

    @staticmethod
    def add_olist_text(text):
        return text

    @staticmethod
    def end(out):
        out += "</div>\n</body>\n</html>"
        return out.out.encode()

    @staticmethod
    def tag(text):
        if "](" in text:
            text = text.split("](")
            link = text[0]
            text = text[-1]
        else:
            text = text.split(": ")
            link = text[0]
            text = text[-1]
        return "<a href=%s> %s </a><br/>" % (text, link)


"""
@Formater
class docx():
    @staticmethod
    def outer_init(self, out, prop):
        self.doc = Document(prop.get("template"))

    @staticmethod
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
                if self.p is None:
                    self.p = self.doc.add_paragraph()
                self.r = self.p.add_run(text)
                self.r.bold = True
            elif ttype == "EMPH":
                if self.p is None:
                    self.p = self.doc.add_paragraph()
                self.r = self.p.add_run(text)
                self.r.italic = True
            else:
                if self.p is None:
                    self.p = self.doc.add_paragraph()
                self.r = self.p.add_run(text)
        return self

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def start():
        return []

    @staticmethod
    def add_text(text):
        return [text]

    @staticmethod
    def add_new_line():
        return ["\n"]

    @staticmethod
    def emph_text(text):
        return ["EMPH: " % text]

    @staticmethod
    def bold_text(text):
        return ["BOLD: " % text]

    @staticmethod
    def add_header_1(text):
        return ["H1: " % text]

    @staticmethod
    def add_header_2(text):
        return ["H2: " % text]

    @staticmethod
    def add_header_3(text):
        return ["H3: " % text]

    @staticmethod
    def start_code():
        return ["\n"]

    @staticmethod
    def code_line(text):
        return [text, "\n"]

    @staticmethod
    def end_code():
        return []

    @staticmethod
    def start_ulist():
        return []

    @staticmethod
    def start_ulist_1(level):
        return ["L1: "]

    @staticmethod
    def start_ulist_2(level):
        return ["L2: "]

    @staticmethod
    def start_ulist_3(level):
        return ["L3: "]

    @staticmethod
    def end_ulist(level):
        return []

    @staticmethod
    def emph_ulist_text(text):
        return ["EMPH: " % text]

    @staticmethod
    def bold_ulist_text(text):
        return ["BOLD: " % text]

    @staticmethod
    def add_ulist_text(text):
        return [text]

    @staticmethod
    def end(out):
        out.doc.save("/tmp/tmp.docx")
        with open("/tmp/tmp.docx", "rb") as f:
            text = f.read()
        return text

    @staticmethod
    def tag(text):
        if "](" in text:
            text = text.split("](")
            link = text[0]
            text = text[-1]
        else:
            text = text.split(": ")
            link = text[0]
            text = text[-1]
        return ["<a href=%s> %s </a><br/>" % (text, link)]
"""


@Formater
class pdf_groff():
    """
    args:
        author: the author of the document
        title: the title of the document
        title_page: if defined will add a title page to the document
        title_head: the level of the first heading
    """
    @staticmethod
    def outer_init(self, out, prop):
        self.pp = False
        self.author = prop.get("author", "")
        self.title = prop.get("title", "")
        if prop.get("title_page") and prop.get("title"):
            out += "\n()TTL()\n.bp\n"
        self.title_heading_level = int(prop.get("title_head", "0"))

        out = out.replace("()TTL()", self.title)
        out = out.replace("()AUT()", self.author)
        self.out = out

    @staticmethod
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
            elif self.pp is False:
                if self.out[-1] != "\n":
                    self.out += "\n"
                self.pp = True
                self.out += ".PP\n"
            if not out == "\n":
                self.out += out
        return self

    @staticmethod
    def fmt_init(self, **options):
        Formatter.__init__(self, **options)
        self.styles = {}
        for token, style in self.style:
            if style['color'] is None:
                color = "000000"
            else:
                color = style['color']
            self.styles[token] = (color, style['bold'],
                                  style['italic'], style['underline'])

    @staticmethod
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
                val = lastval.replace('\n', '\n.in %sc\n' % float(indent/6))
                outfile += ".defcolor pyg rgb #%s\n.gcolor pyg\n%s\n.gcolor\n"
                outfile = outfile % (color, val)
            # set lastval/lasttype to current values
            lastval = value
            lasttype = ttype
        if lastval.strip(" "):
            color = self.styles[lasttype][0]
            val = lastval.replace('\n', '\n.in %sc\n' % float(indent/6))
            outfile += ".defcolor pyg rgb #%s\n.gcolor pyg\n%s\n.gcolor\n"
            outfile = outfile % (color, val)
        # set lastval/lasttype to current values
        lastval = value
        lasttype = ttype
        outfile += ".fcolor\n"

    @staticmethod
    def add_new_line():
        return "\n"

    @staticmethod
    def add_text(text):
        if text.strip(" ") != "":
            return "%s\n" % text
        return ""

    @staticmethod
    def emph_text(text):
        return ".UL \"%s\"\n" % text

    @staticmethod
    def start():
        # \\X'papersize=5.5i,8.5i'\n
        # \n.nr PO .3i\n.nr LL 6.4i\n.nr FM .5i\n.nr HM .3i\n.nr LT 7.4i
        return """
               .OH '''%'
               .EH '''%'
               .color 1
               .OF '()AUT()'''
               .EF
               '''()TTL()'
               """

    @staticmethod
    def bold_text(text):
        return ".B %s\n" % text

    @staticmethod
    def add_header_1(text):
        return """
               .OH '%'-%s-''
               .EH ''-%s-'%'
               .bp
               .NH ()HL1()
               %s
               .XS
               .B
               %s
               .XE
               .PP
               """ % (text, text, text, text)

    @staticmethod
    def add_header_2(text):
        return ".NH ()HL2()\n%s\n.XS\n\t%s\n.XE\n.PP\n" % (text, text)

    @staticmethod
    def add_header_3(text):
        return ".NH ()HL3()\n%s\n.XS\n\t\t{text}\n.XE\n.PP\n" % (text, text)

    @staticmethod
    def start_ulist():
        return ""

    @staticmethod
    def start_code():
        return "LI;\n.LP\n"

    @staticmethod
    def code_line(text):
        return text.replace("\\TS", "#\\.RS\n")\
            .replace("\\TE", "#\\.RE\n") + "\n"

    @staticmethod
    def end_code():
        return ""

    @staticmethod
    def start_ulist_1(level):
        if level == 1:
            return ".IP \\(bu 2\n"
        if level == 2:
            return ".RE\n.IP \\(bu 2\n"
        if level == 3:
            return ".RE\n.RE\n.IP \\(bu 2\n"

    @staticmethod
    def start_ulist_2(level):
        if level == 1:
            return ".RS\n.IP \\(bu 2\n"
        if level == 2:
            return ".IP \\(bu 2\n"
        if level == 3:
            return ".RE\n.IP \\(bu 2\n"

    @staticmethod
    def start_ulist_3(level):
        if level == 1:
            return ".RS\n.RS\n.IP \\(bu 2\n"
        if level == 2:
            return ".RS\n.IP \\(bu 2\n"
        if level == 3:
            return ".IP \\(bu 2\n"

    @staticmethod
    def end_ulist(level):
        if level == 1:
            return ""
        if level == 2:
            return ".RE\n"
        if level == 3:
            return ".RE\n.RE\n"

    @staticmethod
    def emph_ulist_text(text):
        return "LI;%s" % text

    @staticmethod
    def bold_ulist_text(text):
        return "LI;%s" % text

    @staticmethod
    def add_ulist_text(text):
        return "LI;%s" % text

    @staticmethod
    def end(out):
        out += """
               .OH '%'-Table Of Contents-''
               .EH ''-Table Of Contents-'%'
               .de TOC
               .MC 200p .3i
               .SH
               Table Of Contents
               ..
               .TC
               """
        out.out = out.out.replace("\n\n", "\n")
        o = subprocess.Popen("groff -Tpdf -dpaper=a4 -P-pa4 -ms".split(" "),
                             stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        return o.communicate(input=out.out.encode())[0]

    @staticmethod
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
            # TODO: calculate coloums automatically
            return "\n.MC %si\n" % text
        if link == "CPT":
            if text[-1] == "!":
                return "\n.bp\n.NH 0\n%s\n" % text[:-1]
            else:
                return """
                       .OH '%'-Table Of Contents-''
                       .EH ''-Table Of Contents-'%%'
                       .de TOC
                       .MC 200p .3i
                       .SH
                       Table Of Contents
                       ..
                       .TC
                       .bp
                       .NH 0
                       %s
                       .rm toc*div
                       .rm toc*num
                       """ % text
        return "%s\n" % text


# TODO: chapter numbers
@Formater
class pdf_latex():
    @staticmethod
    def outer_init(self, out, prop):
        self.pp = False
        self.title_heading_level = 0
        if prop.get("index"):
            out += """
                   \\makeindex[program=makeindex,options=-s ()IDXPTH().ist]
                   """
        out += """
               \\setlength{\\columnseprule}{0pt}
               \\etocsetlevel{chapter}{()HL1()}
               \\etocsetlevel{section}{()HL2()}
               \\etocsetlevel{subsection}{()HL3()}
               \\patchcmd{\\chapter}{\\thispagestyle{plain}}{\\thispagestyle{fancy}}{}{}
               \\pagestyle{fancy}
               \\fancyhf{}
               \\renewcommand{\\footrulewidth}{1pt}
               \\rfoot{()TTL()}
               \\lfoot{()AUT()}
               \\lhead{\\leftmark}
               \\rhead{\\thepage}
               \\begin{document}
               """
        self.author = prop.get("author")
        self.title = prop.get("title")
        if prop.get("title") and prop.get("title_page"):
            out += """
                   \\begin{titlepage}
                   \\begin{center}
                   \\vspace*{1cm}
                   \\textbf{()TTL()}

                   \\vspace{0.5cm}

                   \\textbf{By: ()AUT()}
                   \\vfill
                   \\end{center}
                   \\end{titlepage}
                   """
        self.title_heading_level = int(prop.get("title_head", "0"))
        self.geometry = prop.get("geometry", "a4paper")
        self.index = False
        if prop.get("index"):
            self.index = True
        self.chapter_toc = False
        if prop.get("chapter_toc"):
            self.chapter_toc = True
        self.toc = False
        if prop.get("toc"):
            self.toc = True
            out += """
                   \\setlength{\\columnseprule}{1pt}
                   \\begin{multicols}{2}
                   \\tableofcontents
                   \\end{multicols}
                   \\clearpage
                   \\etocsettocstyle{\\subsection*{This Chapter contains:}}

                   \\setlength{\\columnseprule}{0pt}
                   """
        out = out.replace("()HL1()", str(self.title_heading_level + 0))
        out = out.replace("()HL2()", str(self.title_heading_level + 1))
        out = out.replace("()HL3()", str(self.title_heading_level + 2))
        out = out.replace("()TTL()", self.title)
        if self.author:
            out = out.replace("()AUT()", self.author)
        else:
            out = out.replace("()AUT()", "")
        out = out.replace("()PPR()", self.geometry)
        if not prop.get("no_col"):
            out += "\\begin{multicols}{1}"
        self.out = out

    @staticmethod
    def outer_add(self, out):
        if self.chapter_toc:
            out = out.replace("()LTOC()", "\n\\localtableofcontents\n")
        out = out.replace("()LTOC()", "")
        if self.author:
            out = out.replace("()AUT()", "by: " + self.author)
        else:
            out = out.replace("()AUT()", "")
        if self.geometry:
            out = out.replace("()PPR()", self.geometry)
        else:
            out = out.replace("()PPR()", "a4paper")
        if self.title:
            out = out.replace("()TTL()", self.title)
        else:
            out = out.replace("()TTL()", "")
        if self.out[-1] != "\n":
            self.out += "\n"
        if not out == "\n":
            self.out += out
        return self

    @staticmethod
    def fmt_init(self, **options):
        Formatter.__init__(self, **options)
        self.styles = {}
        for token, style in self.style:
            if style['color'] is None:
                color = "000000"
            else:
                color = style['color']
            self.styles[token] = (color, style['bold'],
                                  style['italic'], style['underline'])

    @staticmethod
    def fmt_format(self, tokensource, outfile):
        lastval = ''
        lasttype = None
        indent = 0
        outfile += "\\begin{flushleft}\n{\\texttt{\n"
        for ttype, value in tokensource:
            if not(value.strip(" ")):
                indent = len(value)-len(value.strip(" "))
            if lastval.strip(" "):
                color_r = int(self.styles[lasttype][0], 16) & int("FF0000", 16)
                color_g = int(self.styles[lasttype][0], 16) & int("00FF00", 16)
                color_b = int(self.styles[lasttype][0], 16) & int("0000FF", 16)
                color_r = str(float(color_r)/int("10000", 16))
                color_g = str(float(color_g)/int("100", 16))
                color_b = str(float(color_b))
                val = lastval.replace("\\", "{\\textbackslash}")\
                    .replace('{', '\\{')\
                    .replace('$', '\\$')\
                    .replace('}', '\\}')\
                    .replace("\n",
                             """
                             \\\\
                             \\setlength\\parindent{%ipt}
                             """ % indent*8)
                outfile += """{
                           \\definecolor{code}{rgb}{%s, %s, %s}
                           \\color{code} %s}
                           """ % (color_r, color_g, color_b, val)
            lastval = value
            lasttype = ttype
        if lastval.strip(" "):
            color_r = int(self.styles[lasttype][0], 16) & int("FF0000", 16)
            color_g = int(self.styles[lasttype][0], 16) & int("00FF00", 16)
            color_b = int(self.styles[lasttype][0], 16) & int("0000FF", 16)
            color_r = str(float(color_r)/int("10000", 16))
            color_g = str(float(color_g)/int("100", 16))
            color_b = str(float(color_b))
            val = lastval.replace("\\", "{\\textbackslash}")\
                .replace('{', '\\{')\
                .replace('$', '\\$')\
                .replace('}', '\\}')\
                .replace("\n", """\\\\
                               \\setlength\\parindent{%ipt}
                               """ % indent*8)
            outfile += """{
                       \\definecolor{code}{rgb}{%s, %s, %s}
                       \\color{code} %s}
                       """ % (color_r, color_g, color_b, val)

    @staticmethod
    def add_new_line():
        return "{\\\\}\n"

    @staticmethod
    def add_text(text):
        if text.strip(" ") != "":
            return "%s\n" % text
        return ""

    @staticmethod
    def emph_text(text):
        return "\\emph{%s}\n" % text

    @staticmethod
    def start():
        return """
               \\documentclass{book}
               \\usepackage{fancyhdr}
               \\usepackage{etoolbox}
               \\usepackage{multicol}
               \\usepackage{etoc}
               \\usepackage[()PPR()]{geometry}
               \\usepackage{xcolor}
               \\usepackage{imakeidx}
               """

    @staticmethod
    def bold_text(text):
        return "\\textbf{%s}\n" % text

    @staticmethod
    def add_header_1(text):
        return "\n\\section{%s}\n" % text

    @staticmethod
    def add_header_2(text):
        return "\n\\subsection{%s}\n" % text

    @staticmethod
    def add_header_3(text):
        return "\n\\subsubsection{%s}\n" % text

    @staticmethod
    def start_ulist():
        return "\\begin{itemize}"

    @staticmethod
    def start_code():
        return ""

    @staticmethod
    def code_line(text):
        return text+"\n"

    @staticmethod
    def end_code():
        return ""

    @staticmethod
    def start_ulist_1(level):
        if level == 1:
            return ""
        if level == 2:
            return "\\end{itemize}\n"
        if level == 3:
            return "\\end{itemize}\n\\end{itemize}\n"

    @staticmethod
    def start_ulist_2(level):
        if level == 1:
            return "\\begin{itemize}\n"
        if level == 2:
            return ""
        if level == 3:
            return "\\end{itemize}\n"

    @staticmethod
    def start_ulist_3(level):
        if level == 1:
            return "\\begin{itemize}\n\\begin{itemize}\n"
        if level == 2:
            return "\\begin{itemize}\n"
        if level == 3:
            return ""

    @staticmethod
    def end_ulist(level):
        if level == 1:
            return "\\end{itemize}\n"
        if level == 2:
            return "\\end{itemize}\n\\end{itemize}\n"
        if level == 3:
            return "\\end{itemize}\n\\end{itemize}\n\\end{itemize}\n"

    @staticmethod
    def emph_ulist_text(text):
        return "\\item \\textbf{%s}\n" % text

    @staticmethod
    def bold_ulist_text(text):
        return "\\item \\textit{%s}\n" % text

    @staticmethod
    def add_ulist_text(text):
        return "\\item %s\n" % text

    @staticmethod
    def start_olist():
        return "\\begin{enumerate}"

    @staticmethod
    def start_olist_1(level):
        if level == 1:
            return ""
        if level == 2:
            return "\\end{enumerate}\n"
        if level == 3:
            return "\\end{enumerate}\n\\end{enumerate}\n"

    @staticmethod
    def start_olist_2(level):
        if level == 1:
            return "\\begin{enumerate}\n"
        if level == 2:
            return ""
        if level == 3:
            return "\\end{enumerate}\n"

    @staticmethod
    def start_olist_3(level):
        if level == 1:
            return "\\begin{enumerate}\n\\begin{enumerate}\n"
        if level == 2:
            return "\\begin{enumerate}\n"
        if level == 3:
            return ""

    @staticmethod
    def end_olist(level):
        if level == 1:
            return "\\end{enumerate}\n"
        if level == 2:
            return "\\end{enumerate}\n\\end{enumerate}\n"
        if level == 3:
            return "\\end{enumerate}\n\\end{enumerate}\n\\end{enumerate}\n"

    @staticmethod
    def emph_olist_text(text):
        return "\\item \\textbf{%s}\n" % text

    @staticmethod
    def bold_olist_text(text):
        return "\\item \\textit{%s}\n" % text

    @staticmethod
    def add_olist_text(text):
        return "\\item %s\n" % text

    # TODO: set path to pdflatex
    @staticmethod
    def end(out):
        tmpdir = "/tmp/"
        latex = "pdflatex"
        if os.name == "nt":
            tmpdir = "C:\\Users\\Preston.precourt\\Downloads\\"
            latex = "C:\\Users\\Preston.precourt\\AppData\\Local\\Programs\\texlive\\texlive\\2019\\bin\\win32\\pdflatex.exe"
        out += "\n\\end{multicols}"
        if out.index:
            out += "\n\\printindex\n\\pagestyle{fancy}\n"
        out += "\n\\end{document}\n"
        out.out = out.out.replace("&", "\\&")\
            .replace("%", "\\%")\
            .replace("#", "\\#")\
            .replace("\\n", "{\\textbackslash}n")\
            .replace("_", "\\_").replace("|", "\\|")\
            .replace("\n\\\\\n", "\n\n")
        tempin = tempfile.NamedTemporaryFile(dir=tmpdir, delete=False)
        tempin_name = tempfile.gettempprefix() + tempin.name.split("tmp")[-1]
        path = tmpdir
        out.out = out.out.replace("()IDXPTH()", path.replace("\\", "/"))
        tempin.write(out.out.encode())
        tempin.close()
        try:
            if out.index:
                with open("%s.ist" % path, 'w+') as index_style:
                    index_style.write(
                        """
                        headings_flag 1

                        heading_prefix \"\\n\\\\centering\\\\large\\\\sffamily\\\\bfseries%
                        \\\\noindent\\\\textbf{\"
                        heading_suffix \"}\\\\par\\\\nopagebreak\\n\"

                        item_0 \"\\n \\\\item \\\\small \"
                        delim_0 \" \\\\hfill \"
                        delim_1 \" \\\\hfill \"
                        delim_2 \" \\\\hfill \"
                        """)
                    index_style.write(
                        """heading_prefix \"\\n{\\\\centering\\\\noindent\\\\textbf{\"
                        heading_suffix \"}\\\\par\\\\nopagebreak\\n}\"
                        headings_flag 1
                        """)
            if out.toc:
                o = subprocess.Popen(("%s -output-directory %s %s/%s" %
                                     (latex, tmpdir, tmpdir, tempin_name))
                                     .split(" "),
                                     stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE,
                                     cwd=path)
                out = o.communicate()
            o = subprocess.Popen(("%s -output-directory %s %s/%s" %
                                 (latex, tmpdir, tmpdir, tempin_name))
                                 .split(" "),
                                 stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 cwd=path)
            out = o.communicate()
            tempout = open("%s/%s.pdf" % (tmpdir, tempin_name), 'r+b')
            pdf = tempout.read()
            tempout.close()
        except FileNotFoundError:
            print("error")
            if type(out) is tuple:
                print(out[0].decode("utf-8"))
            pdf = ""
        for file in sorted(os.listdir(tmpdir)):
            if re.search("%s.*" % tempin_name, file):
                os.remove(tmpdir + file)
        return pdf

    @staticmethod
    def tag(text):
        if ":" in text:
            text = text.split(":")
            link = text[0].strip(" ")
            text = text[-1].strip(" ")
        else:
            return ""
        if link == "COL":
            return "\\end{multicols}\n\\begin{multicols}{" + text + "}"
        if link == "CPT":
            text = """
                   \\end{multicols}
                   \\chapter{%s}\\setlength{\\columnseprule}{1pt}
                   \\begin{multicols}{2}
                   ()LTOC()
                   \\end{multicols}
                   \\setlength{\\columnseprule}{0pt}
                   \\clearpage
                   \\begin{multicols}{2}
                   """ % text
            return text
        if link == "PRT":
            text = """
                   \\end{multicols}
                   \\clearpage
                   \\ifodd\\value{page}\\hbox{}\\newpage\\fi
                   \\part{%s}

                   \\begin{multicols}{2}
                   """ % text
            return text
        if link == "IDX":
            entry = text
            text = ""
            for item in entry.split(";"):
                text += "\n\\index{%s}\n" % item.strip(" ")
        return text + "\n"
