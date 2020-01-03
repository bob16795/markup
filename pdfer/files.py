import pdfer.objects as objs

class pdf_file():
    def __init__(self):
        self.catalog = objs.catalog_object()
        self.pages = objs.pages_object()
        self.catalog.add_pages(self.pages)
        self.outlines = objs.outlines_object()
        self.add_page()

    def add_page(self):
        self.font = objs.font_object("/F1")
        page = objs.page_object(self.font)
        self.pages.append(page)
    def add_text(self):
        text = objs.text_object()
        text.append("BT\n/F1 24 Tf\n100 100 Td\n(HI) Tj\nET")
        self.pages.pages[-1].append(text)

    def allocate(self):
        objects_ordered = []
        objects_ordered.append(self.catalog)
        objects_ordered.append(self.outlines)
        objects_ordered.append(self.pages)
        for page in self.pages.pages:
            objects_ordered.append(page)
            for text in page.text_objs:
                objects_ordered.append(text)
        objects_ordered.append(self.font)
        return objects_ordered

    def __str__(self):
        objects_ordered = self.allocate()
        text = "%PDF-1.4\n"
        footer = f"xref\n0 {len(objects_ordered) - 1}\n0000000000 65535 f\n"
        end = f"trailer\n<< /Size {len(objects_ordered) - 1}\n/Root 1 0 R\n>>\nstartxref\n"
        for i, object in enumerate(objects_ordered):
            text += f"{i + 1} 0 obj\n{object.__str__()}endobj\n"
            footer += "{:0=10} 00000 n\n".format(len(text) - 1)
        for i, object in enumerate(objects_ordered):
            text = text.replace(f"%%{object}%%", f"{i + 1} 0 R")
        end += f"{len(text)}\n%%EOF"
        return text + footer + end

if __name__=="__main__":
    file = pdf_file()
    file.add_text()
    print(file.__str__())