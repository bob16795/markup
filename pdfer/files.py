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
        self.line_spacing = 2.4
        self.column_spacing = 20
        self.current_column = 1
        self._columns = 1
        self.media_box = [612, 792]
        self.title = ""
        self.title_page = False
        self.index = {}
        self.toc = {}
        self.add_page()
        
    def add_index_entry(self, entrys):
        for entry in entrys.split(";"):
            entry = entry.strip(" ")
            if entry[0] not in self.index:
                self.index[entry[0]] = {}
            if entry not in self.index[entry[0]]:
                self.index[entry[0]][entry] = []
            if not len(self.pages.pages) in self.index[entry[0]][entry]:
                self.index[entry[0]][entry].append(len(self.pages.pages))

    def add_page(self, text = None, size = None, odd = None):
        self.y = 692
        self.y_start = 692
        self.current_column = 1
        page = objs.page_object(self.font)
        self.pages.append(page)
        if (len(self.pages.pages) % 2 == 0) == odd:
            page = objs.page_object(self.font)
            self.pages.append(page)
        if text:
            self.add_text(text, size)

    def add_space(self, space):
        self.y -= (space)
        if self.y < 100:
            self.add_page()

    def add_heading(self, text, level):
        col_start = self.columns
        size = 32
        number = f""
        if level > 0:
            self.level[level-1] += 1
            for i in range(level + 1, 2):
                self.level[i] = 0
            levels = [i.__str__() for i in self.level]
            number = ".".join(levels[::1]) + " "
            while ".0" in number:
                number = number.replace(".0", "")
            self.toc[number +text] = (level, (len(self.pages.pages)))
        else:
            self.columns = 1
            number = ""
            self.level = [0, 0, 0]
            if level == -1:
                self.cpt += 1
                size = 40
                if self.pages.pages[-1].text_objs != []:
                    self.add_page(odd = True)
                self.add_space(250)
                self.add_text(f"Chapter {self.cpt}", size)
            if level == -2:
                self.cpt = 0
                self.prt += 1
                size = 45
                if self.pages.pages[-1].text_objs != []:
                    self.add_page(odd = True)
                self.add_space(200)
                self.add_text(f"Part {self.prt}", size)
        if level == 2:
            size = 24
        if level == 3:
            size = 16
        self.add_text(f"{number}{text}", size)
        if level == -2:
            self.add_page()
        self.columns = col_start
          
    @property
    def columns(self):
        return self._columns

    @columns.setter
    def columns(self, value):
        if value != self._columns:
            self.y_start = self.y
            self._columns = value
            self.current_column = 1
            if value != 1 and self.current_column != 1:
                self.add_page()

    def add_text(self, text, size = 12):
        if self.y - (size + self.line_spacing) < 100:
            if self.current_column >= self._columns:
                self.current_column = 1
                self.add_page(text, size)
            else:
                self.current_column += 1
                self.y = self.y_start
                self.add_text(text, size)
        else:
            text_obj = objs.text_object()
            column_size = ((self.media_box[0]-200) - (self.column_spacing * (self.columns - 1))) / self.columns
            col_x = ((column_size + self.column_spacing) * (self.current_column - 1)) + 100 
            text_obj.append(f"BT\n{size + self.line_spacing} TL\n/F1 {size} Tf\n{col_x} {self.y} Td\n")
            full = False
            text = lib.addbs(text).replace("\n", "\n\t")
            if "\n" in text:
                text = "" + text
            for line in text.split("\n"):
                pdf_line = []
                for word in line.split(" "):
                    if not full:
                        pdf_line.append(word)
                        if lib.get_text_size(' '.join(pdf_line), size) >= column_size:
                            spacing = 1
                            try:
                                spacing =( column_size - lib.get_text_size(' '.join(pdf_line[:-1]), size)) / (len(pdf_line[:-1]) - 1)
                            except:
                                pass
                            text_obj.append(f"{spacing} 0 ({' '.join(pdf_line[:-1])}) \"\n")
                            self.y -= size + self.line_spacing
                            pdf_line = [word]
                            if self.y - (size + self.line_spacing) < 100:
                                full = True
                                overfill = pdf_line
                    else:
                        overfill.append(word)
                if not full:
                    if pdf_line:
                        text_obj.append(f"0 0 ({' '.join(pdf_line)}) \"\n() '\n")
                        self.y -= size + self.line_spacing
                        self.y -= size + self.line_spacing
                else:
                    if overfill:
                        overfill[-1] += "\n"
            if len(text.split("\n")) == 1:
                self.y += size + self.line_spacing
            text_obj.append("ET\n")
            self.pages.pages[-1].append(text_obj)
            if full:
                if self.current_column >= self._columns:
                    self.current_column = 1
                    self.add_page(' '.join(overfill)[:-1].replace("\\(", "(").replace("\\)", ")").replace("\\\\", "\\"), size)
                else:
                    self.current_column += 1
                    self.y = self.y_start
                    self.add_text(' '.join(overfill)[:-1].replace("\\(", "(").replace("\\)", ")").replace("\\\\", "\\"), size)

    def finish(self):
        toc_file = pdf_file()
        if self.title_page:
            toc_file.add_text(self.title, 48)
            toc_file.add_page()
        toc_file.add_text("Table Of Contents", 32)
        toc_file.columns = 2
        for i in self.toc:
            toc_file.add_text(("  " * (self.toc[i][0] - 1)) + i + "   " + str(self.toc[i][1]), 12)
        length = len(toc_file.pages.pages)
        toc_file = pdf_file()
        if self.title_page:
            toc_file.add_text(self.title, 48)
            toc_file.add_page()
        toc_file.add_text("Table Of Contents", 32)
        toc_file.columns = 2
        for i in self.toc:
            toc_file.add_text(("  " * (self.toc[i][0] - 1)) + i + "   " + str(self.toc[i][1] + length - 1), 12)
        self.pages.pages[0:0] = toc_file.pages.pages
        self.add_page()
        self.columns = 1
        self.add_text("INDEX", 32)
        self.columns = 3
        for letter in sorted(self.index):
            self.add_text(letter, 24)
            for text in self.index[letter]:
                entry = text + "   " + \
                    ", ".join([str(i + length - 1) for i in self.index[letter][text]])
                self.add_text(entry, 12)
        for i, page in enumerate(self.pages.pages[1:]):
            number = objs.text_object()
            number.append(f"BT\n/F1 12 Tf\n100 50 Td\n({i}) Tj\nET")
            page.append(number)


    def sequence(self):
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
        objects_ordered = self.sequence()
        text = "%PDF-1.2\n"
        footer = f"xref\n0 {len(objects_ordered) - 1}\n0000000000 65535 f\n"
        end = f"trailer\n<< /Size {len(objects_ordered) - 1}\n/Root 1 0 R\n>>\nstartxref\n"
        for i, object in enumerate(objects_ordered):
            footer += "{:0=10} 00000 n\n".format(len(text) - 1)
            text += f"{i + 1} 0 obj\n{object.__str__()}endobj\n"
        for i, object in enumerate(objects_ordered):
            text = text.replace(f"%%{object.ident()}%%", f"{i + 1} 0 R")
        end += f"{len(text)}\n%%EOF"
        return text + footer + end

if __name__=="__main__":
    file = pdf_file()
    print(file.__str__())
