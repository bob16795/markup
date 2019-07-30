from markup.nodes import *
from docx.shared import RGBColor
from pygments import highlight
from pygments.lexers import PythonLexer
import importlib


def add_to_doc(file, parsed, to, adderstr, addermodstr, info):
    module = importlib.import_module(addermodstr)
    adder = getattr(module, adderstr)
    out = adder.outer()(adder.start()(), info)
    if type(parsed) is not nullNode:
        for i in parsed.paragraphs:
            if type(i) is HeadNode or type(i) is Node or type(i) is nullNode:
                if i.type == "HEAD1":
                    out += adder.add_header_1()(i.value.strip(" "))
                elif i.type == "HEAD2":
                    out += adder.add_header_2()(i.value.strip(" "))
                elif i.type == "HEAD3":
                    out += adder.add_header_3()(i.value.strip(" "))
                if i.type == "TAG":
                    out += adder.tag()(i.value)
            elif type(i) is ListNode:
                out += adder.start_list()()
                l = 1
                for j in i.sentences:
                    if j.type == "LIST1":
                        out += adder.start_list_1()(l)
                        l = 1
                    elif j.type == "LIST2":
                        out += adder.start_list_2()(l)
                        l = 2
                    elif j.type == "LIST3":
                        out += adder.start_list_3()(l)
                        l = 3
                    elif j.value != "" and j.value != " " and j.type == "TEXT":
                        out += adder.add_list_text()(f"{j.value} ")
                    elif j.value != "" and j.value != " " and j.type == "EMPH":
                        out += adder.emph_list_text()(f"{j.value} ")
                    elif j.value != "" and j.value != " " and j.type == "BOLD":
                        out += adder.bold_list_text()(f"{j.value} ")
                out += adder.end_list()(l)
            elif type(i) is CodeNode:
                out += adder.start_code()()
                code = ""
                for j in i.sentences:
                    if j.type == "TEXT":
                        if j.value != " ":
                            code += adder.code_line()(j.value)
                fmt = adder.fmt()()
                highlight(code.strip("\n"), PythonLexer(), fmt, outfile=out)
                out += adder.end_code()()
            else:
                for j in i.sentences:
                    if j.type == "TEXT":
                        out += adder.add_text()(f"{j.value}")
                    elif j.value != "" and j.value != " " and j.type == "EMPH":
                        out += adder.emph_text()(f"{j.value}")
                    elif j.value != "" and j.value != " " and j.type == "BOLD":
                        out += adder.bold_text()(f"{j.value}")
                out += adder.add_new_line()()
    adder.end()(out, to)
