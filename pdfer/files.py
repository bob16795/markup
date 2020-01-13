import pdfer.objects as objs
import pdfer.lib as lib

class pdf_file():
    def __init__(self):
        self.catalog = objs.catalog_object()
        self.pages = objs.pages_object()
        self.catalog.add_pages(self.pages)
        self.outlines = objs.outlines_object()
        self.font = objs.font_object("/F1")
        self.level = [0, 0, 0]
        self.cpt = 0
        self.prt = 0
        self.add_page()

    def add_page(self, text = None, size = None):
        self.y = 692
        page = objs.page_object(self.font)
        self.pages.append(page)
        if text:
            self.add_text(text, size)

    def add_space(self, space):
        self.y -= (space)
        if self.y < 100:
            self.add_page()

    def add_heading(self, text, level):
        size = 32
        number = f""
        if level > 0:
            self.level[level-1] += 1
            for i in range(level - 1):
                self.level[i] = 0
            levels = [i.__str__() for i in self.level]
            number = ".".join(levels) + " "
            while "0." in number:
                number = number.replace("0.", "")
        else:
            number = ""
            self.level = [0, 0, 0]
            if level == -1:
                self.cpt += 1
                size = 40
                if self.pages.pages[-1].text_objs != []:
                    self.add_page()
                self.add_space(250)
                self.add_text(f"Chapter {self.cpt}", size)
            if level == -2:
                self.cpt = 0
                self.prt += 1
                size = 45
                if self.pages.pages[-1].text_objs != []:
                    self.add_page()
                self.add_space(200)
                self.add_text(f"Part {self.prt}", size)
        if level == 2:
            size = 24
        if level == 3:
            size = 16
        self.add_text(f"{text}", size)
        if level == -2:
            self.add_page()

    def add_text(self, text, size = 12):
        if self.y - (size * 1.2) < 100:
            self.add_page(text, size)
        else:
            text_obj = objs.text_object()
            text_obj.append(f"BT\n{size * 1.2} TL\n/F1 {size} Tf\n100 {self.y} Td\n")
            full = False
            text = text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
            for line in text.split("\n"):
                pdf_line = []
                for word in line.split(" "):
                    if not full:
                        pdf_line.append(word)
                        if lib.get_text_size(' '.join(pdf_line), size) >= 412:
                            spacing =( 412 - lib.get_text_size(' '.join(pdf_line[:-1]), size)) / (len(pdf_line[:-1]) - 1)
                            text_obj.append(f"{spacing} 0 ({' '.join(pdf_line[:-1])}) \"\n")
                            self.y -= size * 1.2
                            pdf_line = [word]
                            if self.y - (size * 1.2) < 100:
                                full = True
                                overfill = pdf_line
                    else:
                        overfill.append(word)
                if not full:
                    if pdf_line:
                        text_obj.append(f"({' '.join(pdf_line)}) '\n() '\n")
                        self.y -= size * 1.2
                        self.y -= size * 1.2
                else:
                    if overfill:
                        overfill[-1] += "\n"
            if len(text.split("\n")) == 1:
                self.y += size * 1.2
            text_obj.append("ET\n")
            self.pages.pages[-1].append(text_obj)
            if full:
                self.add_page(' '.join(overfill)[:-1].replace("\\(", "(").replace("\\)", ")").replace("\\\\", "\\"), size)

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
        text = "%PDF-1.2\n"
        footer = f"xref\n0 {len(objects_ordered) - 1}\n0000000000 65535 f\n"
        end = f"trailer\n<< /Size {len(objects_ordered) - 1}\n/Root 1 0 R\n>>\nstartxref\n"
        for i, object in enumerate(objects_ordered):
            text += f"{i + 1} 0 obj\n{object.__str__()}endobj\n"
            footer += "{:0=10} 00000 n\n".format(len(text) - 1)
        for i, object in enumerate(objects_ordered):
            text = text.replace(f"%%{object.ident()}%%", f"{i + 1} 0 R")
        end += f"{len(text)}\n%%EOF"
        return text + footer + end

if __name__=="__main__":
    file = pdf_file()
    print(file.__str__())