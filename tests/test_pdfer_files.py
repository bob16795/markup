import pdfer.files as f
import pdfer.objects as o

def test_pdf_file_add_page_is_empty():
    file = f.pdf_file()
    file.add_page()
    assert file.pages.pages[-1].__str__() == o.page_object(file.font).__str__()

def test_pdf_file_add_text_exists():
    file = f.pdf_file()
    file.add_text("lol")
    assert "(lol) '" in file.__str__()

def test_pdf_file_add_text_no_extra():
    file = f.pdf_file()
    file.add_text("lol\nnope")
    print(file.__str__())
    assert not("() '" in file.__str__())
