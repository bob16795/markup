"""
handles .doc files
"""
def setup(doc):
    """
    formats a .doc file
    """
    doc.styles.add_style("Quote", 1, True)

def header(doc, title, *_):
    """
    Adds a heading to a .doc file
    """
    print(f" + Doc {title}")
    par = doc.paragraphs[0]
    par.text = title
    par.style = "Title"
