from markup.nodes import nullNode, Node, HeadNode, ListNode, CodeNode
from pygments import highlight
from pygments.lexers import PythonLexer
import importlib


def add_to_doc(parsed, adderstr, addermodstr, info):
    module = importlib.import_module(addermodstr)
    adder = getattr(module, adderstr)
    out = adder.outer()(adder.start()(), info)
    if type(parsed) is not nullNode:
        for node in parsed.paragraphs:
            if type(node) is HeadNode or type(node) is Node or type(node) is nullNode:
                if node.type == "HEAD1":
                    out += adder.add_header_1()(node.value.strip(" "))
                elif node.type == "HEAD2":
                    out += adder.add_header_2()(node.value.strip(" "))
                elif node.type == "HEAD3":
                    out += adder.add_header_3()(node.value.strip(" "))
                if node.type == "TAG":
                    out += adder.tag()(node.value)
            elif type(node) is ListNode:
                out += adder.start_list()()
                list_level = 1
                for sentence in node.sentences:
                    if sentence.type == "LIST1":
                        out += adder.start_list_1()(list_level)
                        list_level = 1
                    elif sentence.type == "LIST2":
                        out += adder.start_list_2()(list_level)
                        list_level = 2
                    elif sentence.type == "LIST3":
                        out += adder.start_list_3()(list_level)
                        list_level = 3
                    elif sentence.value != "" and sentence.value != " " and sentence.type == "TEXT":
                        out += adder.add_list_text()(f"{sentence.value} ")
                    elif sentence.value != "" and sentence.value != " " and sentence.type == "EMPH":
                        out += adder.emph_list_text()(f"{sentence.value} ")
                    elif sentence.value != "" and sentence.value != " " and sentence.type == "BOLD":
                        out += adder.bold_list_text()(f"{sentence.value} ")
                out += adder.end_list()(list_level)
            elif type(node) is CodeNode:
                out += adder.start_code()()
                code = ""
                for sentence in node.sentences:
                    if sentence.type == "TEXT":
                        if sentence.value != " ":
                            code += adder.code_line()(sentence.value)
                fmt = adder.fmt()()
                highlight(code.strip("\n"), PythonLexer(), fmt, outfile=out)
                out += adder.end_code()()
            else:
                for sentence in node.sentences:
                    if sentence.type == "TEXT":
                        out += adder.add_text()(f"{sentence.value}")
                    elif sentence.value != "" and sentence.value != " " and sentence.type == "EMPH":
                        out += adder.emph_text()(f"{sentence.value}")
                    elif sentence.value != "" and sentence.value != " " and sentence.type == "BOLD":
                        out += adder.bold_text()(f"{sentence.value}")
                out += adder.add_new_line()()
    return adder.end()(out)
