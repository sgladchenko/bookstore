# coding: utf-8

import Tkinter as tk
import wbase

class Page(wbase.WBase):
        # this is the class of single page in pagebook
        # it's for filling widgets in single page of pagebook

        def __init__(self, parent, bg, padx, pady):
                wbase.WBase.__init__(self) # initialization WBase
                self.BODY = tk.Frame(parent, bg='#E8E8E8', padx=padx, pady=pady, bd=0)

        def pack(self): # pack page in pagebook
                self.BODY.pack(side="bottom", fill=tk.BOTH, expand=1)

        def destroy(self): # destroy page in pagebook
                self.BODY.pack_forget()

class Pagebook:
        # this is the widget's class of equivalent of widget notebook with some design modernizations
        widgetName = "pagebook" # name of widget (needs for Form class)
        get = True # flag (that means the pagebook is gettable)
        def __init__(self, parent, bg="#FFFFFF", active="#A4A8AF", disable="#BFBFBF", font=("Calibri", 13), bgr="#384556"):
                self.PAGES   = {} # {INDEX:PAGE_OBJECT, INDEX:PAGE_OBJECT}
                self.FILLS   = {} # {INDEX:FILL_METHOD, INDEX:FILL_METHOD}
                self.TITLES  = {} # {INDEX:TITLE_WIDGET, INDEX:TITLE_WIDGET}
                self.LINES   = {} # {INDEX:LINE_WIDGET, INDEX:LINE_WIDGET}
                self.BINDS   = {} # {TITLE_WIDGET:INDEX, TITLE_WIDGET:INDEX}
                self.FRAMES  = {} # {INDEX:FRAME, INDEX:FRAME}
                self.TEXTS   = {} # {INDEX:TEXT} # texts in titles

                self.BG      = bg      # color of background
                self.BGR     = bgr
                self.ACTIVE  = active  # color of active foreground and line
                self.DISABLE = disable # color of disabled foreground and line
                self.CURRENT = None    # index of current (visible) page  | (PAGE_OBJECT, TITLE_WIDGET, LINE_WIDGET)
                self.FONT    = font    # font of text in titles of pages

                self.FRAME       = tk.Frame(parent, bg=bg, bd=0) # main frame of all elements of pagebook
                self.TITLE_FRAME = tk.Frame(self.FRAME, bg=bg) # frame of page marks

        def __getitem__(self, index): # return Page object of page in pagebook with index
                if index == "current" and bool(self.CURRENT): # returns current page (if current is available)
                        return self.CURRENT[0] # Page object

                try: return self.PAGES[index]
                except: return None

        def start_book(self): # start packing frames of pagebook
                self.FRAME.pack(fill=tk.BOTH, expand=1)
                self.TITLE_FRAME.pack(fill=tk.X, side="top")

        def add_page(self, index, title, padx=30, pady=30, fill=None): # fill - method of filling Page object for widgets
                self.PAGES[index] = Page(self.FRAME, bg=self.BG, padx=padx, pady=pady)
                self.FILLS[index] = fill

                self.FRAMES[index] = tk.Frame(self.TITLE_FRAME, bg=self.BGR, height=40)
                self.FRAMES[index].pack(side="left", fill=tk.X, expand=1)
                self.FRAMES[index].pack_propagate(False)

                self.TITLES[index] = tk.Label(self.FRAMES[index], bg=self.BGR, fg=self.DISABLE,
                                              text=title, font=self.FONT) # title of page
                self.TITLES[index].pack(fill=tk.X, side="top", expand=1)
                self.TITLES[index].bind("<ButtonPress>", self.bind_page) # for viewing pages

                self.LINES[index]  = tk.Frame(self.FRAMES[index], bg=self.BGR, height=4) # line under title
                self.LINES[index].pack(side="bottom", fill=tk.X)

                self.BINDS[self.TITLES[index]] = index # for binding label and action
                self.TEXTS[index] = title

        def delete_page(self, index):
                del self.BINDS[self.TITLES[index]] # deleting index of binding
                self.TITLES[index].destroy() # destroying mark of page
                self.LINES[index].destroy() # destroying mark's line of page
                del self.TITLES[index] # deleting index from marks
                del self.PAGES[index] # deleting index from pages
                del self.LINES[index] # deleting index from lines of marks
                del self.FILLS[index] # deleting index from fill-methods
                del self.TEXTS[index] # deleting text in the title

                self.view_page(self.PAGES.keys()[0])

        def delete_all(self):
                for self.PAGE in self.TITLES.values():
                        self.PAGE.destroy()

                for self.PAGE in self.FRAMES.values():
                        self.PAGE.destroy()

                for self.PAGE in self.LINES.values():
                        self.PAGE.destroy()

                self.PAGES  = {}
                self.FILLS  = {}
                self.TITLES = {}
                self.LINES  = {}
                self.BINDS  = {}
                self.FRAMES = {}
                self.TEXTS  = {}

                if self.CURRENT:
                        self.CURRENT[0].destroy()
                        self.CURRENT = None

        def disable(self, title, line):
                title["fg"] = self.DISABLE
                line["bg"] = self.BGR

        def activate(self, title, line):
                title["fg"] = self.BG
                line["bg"] = self.BG
                #line["width"] = title.winfo_width()

        def disable_current(self):
                if self.CURRENT: # disabling old page
                        self.CURRENT[0].destroy()
                        self.disable(self.CURRENT[1], self.CURRENT[2])

        def view_page(self, index): # make visible page with index
                self.disable_current()
                self.CURRENT = (self.PAGES[index], self.TITLES[index], self.LINES[index]) # new current page

                # activate this page
                self.CURRENT[0].pack()
                self.activate(self.CURRENT[1], self.CURRENT[2])
                self.current_text = self.TEXTS[index]
                if self.FILLS[index]: self.FILLS[index]() # call fill-method

        def bind_page(self, event): # view_page by binding labels in page marks
                self.current_text = self.TEXTS[self.BINDS[event.widget]]
                self.disable_current()
                # new current page
                self.CURRENT = (self.PAGES[self.BINDS[event.widget]], self.TITLES[self.BINDS[event.widget]],
                                self.LINES[self.BINDS[event.widget]])

                # activate this page
                self.CURRENT[0].pack()
                self.activate(self.CURRENT[1], self.CURRENT[2])
                if self.FILLS[self.BINDS[event.widget]]: self.FILLS[self.BINDS[event.widget]]() # call fill-method

        def get_page(self, index): # gets data from gettable widgets in Page object
                self.RESP = {} # response
                for self.name, self.data in self.PAGES[index].get(): # get-data of each page
                        self.RESP[self.name] = self.data # to response

                return self.RESP

        def get_current(self):
                return self.get_page(self.BINDS[self.CURRENT[1]])

        def get_index(self): # index of current page
                if self.CURRENT: return self.BINDS[self.CURRENT[1]]
                else: return None

        def forget_book(self): # closing pagebook with forgetting frames of pagebook
                self.FRAME.pack_forget()
                self.TITLE_FRAME.pack_forget()

        def close_book(self):
                self.FRAME.destroy()