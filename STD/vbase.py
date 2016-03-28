# coding: utf-8

import Tkinter as tk

class VBase:
        # base class of View-classes of pages in main window

        def __init__(self, tk_obj, toggle, path, db, xl, st, ft):
		self.color_bg       = "#E8E8E8"
		self.color_bar      = "#384556"
		self.color_high_bar = "#505D6E"
		self.color_high_bg  = "#A4A8AF"

		self.DB = db # Database object of application
		self.XL = xl # Excel object of application
		self.ST = st # Sets object of application
		self.FT = ft # main font of GUI

                self.ROOT = tk.Frame(tk_obj, bg=self.color_bg)
                self.TOGGLE = toggle
                self.PATH = path

		self.ROOT2 = None # trigger of 2-level's window (Form object)
		self.ROOT3 = None # trigger of 3-level's window (Form object)

		self.HEAD = tk.Frame(self.ROOT, bg=self.color_bar) # Bar frame
		self.HEAD.pack(fill=tk.X) # fill for horizontal

		self.BODY = tk.Frame(self.ROOT, bd=0, bg=self.color_bg) # frame of body
		self.BODY.pack(fill=tk.BOTH, expand=1) # fill for horizontal

		self.STAT = tk.Frame(self.ROOT, bg=self.color_bar, padx=5) # frame of statics bar
		self.STAT.pack(fill=tk.X) # fill for horizontal

        def start_page(self):
                self.ROOT.pack(fill=tk.BOTH, expand=1)

        def forget_page(self):
                self.ROOT.pack_forget()

	def close_root2(self): # protocol of "WM_DELETE_WINDOW" for 2-level's windows
                self.ROOT2.close_form() # closing window
                self.ROOT2 = None # toggle trigger

                if self.ROOT3: self.close_root3() # if ROOT2 was father of ROOT3 then close ROOT3

	def close_root3(self): # protocol of "WM_DELETE_WINDOW" for 3-level's windows
		self.ROOT3.close_form()
                self.ROOT3 = None

	def close(self): # close program
		try:
			self.DB.close() # quiting DB-connection, committing transaction
		finally:
			exit()          # quiting python

        def Bar(self): pass  # virtual method of generating Bar

        def Body(self): pass # virtual method of generating Body

        def Stat(self): pass # virtual method of generating Stat
