# coding: utf-8

from booksview import BooksView
from actionview import ActionView
import Tkinter as tk

class Hub:
        # this is the hub of pages in main window of GUI

        def __init__(self, db, xl, st, path, ft):
		self.TK = tk.Tk()                                   # Tk object of window
		self.TK.title(" BookStore")                         # title of window
		self.TK.geometry("1000x560+10+10")                  # size of window
		self.TK.wm_state("zoomed")                          # full screen mode
		self.TK.minsize(1000,560)                           # minimal size of window

                self.BOOKS_VIEW  = BooksView(self.TK, db, xl, st, path, ft, self.toggle)  # "1" page
                self.ACTION_VIEW = ActionView(self.TK, db, xl, st, path, ft, self.toggle) # "2" page

                self.TOGGLE = 2
                self.ACTION_VIEW.start_page() # viewing ActionView

                self.TK.mainloop() # start window
		self.TK.iconbitmap(default=path + "GUI\\Ico2.ico")  # icon of window

        def toggle(self): # toggle pages
                if self.TOGGLE == 1:
                        self.BOOKS_VIEW.forget_page()
                        self.ACTION_VIEW.start_page()
                        self.ACTION_VIEW.Refresh() # update data
                        self.TOGGLE = 2
                else:
                        self.ACTION_VIEW.forget_page()
                        self.BOOKS_VIEW.start_page()
                        self.BOOKS_VIEW.Fill_list("all") # update data
                        self.TOGGLE = 1