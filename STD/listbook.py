# coding: utf-8

import page, table, empty
import Tkinter as tk

class Listbook:
        # modified Table widget

        def __init__(self, parent, emp1, emp2, img, bg="#E8E8E8", db=None):
                self.FRAME    = tk.Frame(parent, bg=bg, bd=0)
                self.PAGEBOOK = page.Pagebook(self.FRAME, )
                self.TABLE    = table.Table(self.FRAME, img)

                self.EMP1 = emp1
                self.EMP2 = emp2
                self.EMP = None
                self.IMG  = img

                self.CURRENT = None
                self.CURR_KN = None
                self.DB = db

        def pack(self):
                self.FRAME.pack(fill=tk.BOTH, expand=1)

        def get(self):
                if self.CURRENT == "table":
                        return self.TABLE.get()
                elif self.CURRENT == "pages":
                        return self.PAGEBOOK["current"]["table"].get()
                else:
                        return None

        # ACTIONS OF PAGEBOOK

        def create_pagebook(self): # view pagebook of tables
                if self.CURRENT == "table":
                        self.delete_table()
                elif self.CURRENT == "pages":
                        self.delete_pagebook()
                elif self.CURRENT == "empty":
                        self.clean_empty(self.CURR_KN)

                self.CURRENT = "pages"
                self.PAGEBOOK.start_book()

        def new_class(self, index, title, func=None): # new page of class
                if self.CURRENT != "pages": return None
                self.PAGEBOOK.add_page(index, title, padx=0, pady=0, fill=func)
                self.PAGEBOOK[index]["table"] = table.Table(self.PAGEBOOK[index].BODY, self.IMG)
                self.PAGEBOOK[index]["table"].pack()

        def clear_classes(self): # delete all pages
                if self.CURRENT != "pages": return None
                self.PAGEBOOK.delete_all()

        def insert_line(self, index, text): # insert line into page's table of class
                if self.CURRENT != "pages": return None
                self.PAGEBOOK[index]["table"].insert(text)

        def delete_pagebook(self): # forget pagebook
                if self.CURRENT != "pages": return None
                self.PAGEBOOK.delete_all()
                self.PAGEBOOK.forget_book()
                self.CURRENT = None

        # ACTIONS OF TABLE

        def create_table(self):
                if self.CURRENT == "table":
                        self.delete_table()
                elif self.CURRENT == "pages":
                        self.delete_pagebook()
                elif self.CURRENT == "empty":
                        self.clean_empty(self.CURR_KN)

                self.CURRENT = "table"
                self.TABLE.pack()

        def insert(self, text):
                if self.CURRENT != "table": return None
                self.TABLE.insert(text)

        def erase(self):
                if self.CURRENT != "table": return None
                self.TABLE.erase()

        def delete_table(self):
                if self.CURRENT != "table": return None
                self.TABLE.erase()
                self.TABLE.forget()
                self.CURRENT = None

        # ACTIONS OF EMPTY-NOTES

        def go_empty(self, kind):
                if self.CURRENT == "table":
                        self.delete_table()
                elif self.CURRENT == "pages":
                        self.delete_pagebook()
                elif self.CURRENT == "empty":
                        if self.CURR_KN == kind:
                                return None
                        else:
                                self.clean_empty(self.CURR_KN)

                self.CURR_KN = kind
                self.CURRENT = "empty"

                if kind == 1:
                        self.EM1 = empty.Empty(self.FRAME, self.EMP1)
                        self.EM1.pack_center()
                elif kind == 2:
                        self.EM2 = empty.Empty(self.FRAME, self.EMP2)
                        self.EM2.pack_center()

        def clean_empty(self, kind):
                if self.CURRENT != "empty" and self.CURR_KN != kind: return None

                if kind == 1:
                        self.EM1.destroy()
                elif kind == 2:
                        self.EM2.destroy()

                self.CURRENT = None


