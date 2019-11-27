from pygments.lexers import get_lexer_by_name
from markup.nodes import nullNode, Node, HeadNode, ListNode, CodeNode, EquationNode
from pygments import highlight
import importlib


def add_to_doc(parsed, adderstr, addermodstr, prop):
    """
    Converts parser tree to byes object of text using a formatter class

    parsed:      the parser tree
    adderstr:    the name of the adder class
    addermodstr: the name of the modulecontaing the adder class
    prop:        the properties of the document in a dictonary
    """
    module = importlib.import_module(addermodstr)
    adder = getattr(module, adderstr)
    out = adder.outer()(adder.start()(), prop)
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
            elif type(node) is ListNode and "U" in node.sentences[0].type:
                out += adder.start_ulist()()
                ulist_level = 1
                for sentence in node.sentences:
                    if sentence.type == "ULIST1":
                        out += adder.start_ulist_1()(ulist_level)
                        ulist_level = 1
                    elif sentence.type == "ULIST2":
                        out += adder.start_ulist_2()(ulist_level)
                        ulist_level = 2
                    elif sentence.type == "ULIST3":
                        out += adder.start_ulist_3()(ulist_level)
                        ulist_level = 3
                    elif sentence.value != "" and sentence.value != " " and sentence.type == "TEXT":
                        out += adder.add_ulist_text()(sentence.value + " ")
                    elif sentence.value != "" and sentence.value != " " and sentence.type == "EMPH":
                        out += adder.emph_ulist_text()(sentence.value + " ")
                    elif sentence.value != "" and sentence.value != " " and sentence.type == "BOLD":
                        out += adder.bold_ulist_text()(sentence.value + " ")
                out += adder.end_ulist()(ulist_level)
            elif type(node) is EquationNode:
                out += adder.add_equation()(node.value)
            elif type(node) is ListNode and "O" in node.sentences[0].type:
                out += adder.start_olist()()
                olist_level = 1
                for sentence in node.sentences:
                    if sentence.type == "OLIST1":
                        out += adder.start_olist_1()(olist_level)
                        olist_level = 1
                    elif sentence.type == "OLIST2":
                        out += adder.start_olist_2()(olist_level)
                        olist_level = 2
                    elif sentence.type == "OLIST3":
                        out += adder.start_olist_3()(olist_level)
                        olist_level = 3
                    elif sentence.value != "" and sentence.value != " " and sentence.type == "TEXT":
                        out += adder.add_olist_text()(sentence.value + " ")
                    elif sentence.value != "" and sentence.value != " " and sentence.type == "EMPH":
                        out += adder.emph_olist_text()(sentence.value + " ")
                    elif sentence.value != "" and sentence.value != " " and sentence.type == "BOLD":
                        out += adder.bold_olist_text()(sentence.value + " ")
                out += adder.end_olist()(olist_level)

            elif type(node) is CodeNode:
                out += adder.start_code()()
                code = ""
                for sentence in node.sentences:
                    if sentence.type == "TEXT":
                        if sentence.value != " ":
                            code += adder.code_line()(sentence.value)
                fmt = adder.fmt()()
                lexer = get_lexer_by_name(node.value)
                code = code.strip("\n")
                highlight(code, lexer, fmt, outfile=out)
                out += adder.end_code()()
            else:
                for sentence in node.sentences:
                    if sentence.type == "TEXT":
                        out += adder.add_text()(sentence.value)
                    elif sentence.value != "" and sentence.value != " " and sentence.type == "EMPH":
                        out += adder.emph_text()(sentence.value)
                    elif sentence.value != "" and sentence.value != " " and sentence.type == "BOLD":
                        out += adder.bold_text()(sentence.value)
                out += adder.add_new_line()()
    return adder.end()(out)
