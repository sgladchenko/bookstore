# coding: utf-8

import Tkinter as tk
from empty import Empty

class Table:
	# widget of table with books

	def __init__(self, root, img, bg="#E8E8E8", hbg="#A4A8AF", fg="black", hfg="black", font=("Calibri", 13)):
		self.ROOT   = root                                    # parent of Table
		self.GFRAME = tk.Frame(self.ROOT, bg=bg, bd=0)        # frame of Table
		self.CANVAS = tk.Canvas(self.GFRAME, bg=bg)     # canvas frame of Table
		self.FRAME  = tk.Frame(self.CANVAS, bg=bg, bd=0, padx=7, pady=5)      # content frame

		self.SCROLL = tk.Scrollbar(self.GFRAME, orient="vertical", command=self.CANVAS.yview) # scrollbar
		self.CANVAS.configure(yscrollcommand=self.SCROLL.set)                                 # configuring scrollbar for canvas

		self.SCROLL.pack(side="right", fill=tk.Y)                        # packing scrollbar
		self.CANVAS.pack(side="left", fill=tk.BOTH, expand=1)            # packing
		self.CANVAS.create_window(0,0, window=self.FRAME, anchor='nw') # insert content to canvas
		self.FRAME.bind("<Configure>", self.conf) # resizing scrollregion after resizing main frame of widgets

                self.CANVAS["border"]=-2

		self.BG  = bg   # color of background
		self.HBG = hbg  # color of selected element
		self.PH  = img  # pictogram of elements
		self.FT  = font # font of table

		self.ROW = 0    # count of rows in Table
		self.CURRENT = None # current element of Table (selected widget)
                self.EMP = None

		self.EMNS = [] # list of elements: [(IMG,TEXT), (IMG,TEXT)]

	def conf(self, event):
		self.CANVAS.configure(scrollregion=self.CANVAS.bbox("all")) # replacing 

	def insert(self, data): # insert element
		self.limg  = tk.Label(self.FRAME, image=self.PH, bd=0, bg=self.BG, padx=3, pady=3)  # image of element
		self.ltext = tk.Label(self.FRAME, text=data, bd=0, bg=self.BG, padx=5, pady=3, font=self.FT, justify=tk.LEFT, anchor="w", width=200)  # text of elememnt
		self.ltext.bind("<ButtonPress>", self.pressed) # binding event for element (for button pressing)

		self.limg.grid(row=self.ROW, column=0, padx=3, pady=3)  # packing
		self.ltext.grid(row=self.ROW, column=1, sticky="nse", padx=3, pady=3)

		self.EMNS.append((self.limg, self.ltext)) # saving in list of elements

		self.ROW += 1 # incriment count of rows in Table

	def erase(self): # erasing all elements from Table
		for self.e in self.EMNS:
			self.e[0].destroy() # destroy image of element
			self.e[1].destroy() # destroy text of element

		self.CURRENT = None # no elements in Table

		self.ROW = 0 # count of rows to 0

	def get(self):
		if self.CURRENT:
			self.CURRENT["bg"] = self.BG # toggle color

		self.TEMP = self.CURRENT     # temp-var for returning
		self.CURRENT = None          # no current element

		if self.TEMP: return self.TEMP["text"]     # return pressed
		else: return None

	def pressed(self, event):
		if self.CURRENT: self.CURRENT["bg"] = self.BG # if someone book has been alredy pressed

		self.CURRENT = event.widget   # new current element
		event.widget["bg"] = self.HBG # toggle color

	def pack(self):
		self.GFRAME.pack(fill=tk.BOTH, expand=1)

        def forget(self):
                self.GFRAME.pack_forget()
