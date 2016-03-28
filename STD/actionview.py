# coding: utf-8

import Tkinter as tk
import vbase, form, table, page # classes of application
import os, area, ttk

import PIL.ImageTk as ImageTk
import PIL.Image as Image
from sqlalchemy.exc import OperationalError

class ActionView(vbase.VBase):
        # View-page in main table of books' actions

        def __init__(self, tk_obj, db, xl, st, path, ft, toggle):
		# main attributes of Tk object of window
                vbase.VBase.__init__(self, tk_obj, toggle, path, db, xl, st, ft)

                # images of buttons and other graphics
                self.PH_ARR      = ImageTk.PhotoImage(Image.open(path + "GUI\\Arrow.png"))
                self.PH_EXIT     = ImageTk.PhotoImage(Image.open(path + "GUI\\Exit.png"))
                self.PH_HELP     = ImageTk.PhotoImage(Image.open(path + "GUI\\Help.png"))
                self.PH_LOGO     = ImageTk.PhotoImage(Image.open(path + "GUI\\Logo.png"))
                self.PH_BOOK     = ImageTk.PhotoImage(Image.open(path + "GUI\\Book.png"))
                self.PH_EXC      = ImageTk.PhotoImage(Image.open(path + "GUI\\Excel.png"))

		self.BH_EDIT     = ImageTk.PhotoImage(Image.open(path + "GUI\\Buttons\\Edit.png"))
		self.BH_CANCEL   = ImageTk.PhotoImage(Image.open(path + "GUI\\Buttons\\Cancel.png"))
		self.BH_SEARCH   = ImageTk.PhotoImage(Image.open(path + "GUI\\Buttons\\Search.png"))
		self.BH_ADD      = ImageTk.PhotoImage(Image.open(path + "GUI\\Buttons\\Add.png"))
		self.BH_CONT     = ImageTk.PhotoImage(Image.open(path + "GUI\\Buttons\\Continue.png"))
		self.BH_CREATE   = ImageTk.PhotoImage(Image.open(path + "GUI\\Buttons\\Create.png"))
		self.BH_TABLE    = ImageTk.PhotoImage(Image.open(path + "GUI\\Buttons\\Table.png"))
		self.BH_SAVE     = ImageTk.PhotoImage(Image.open(path + "GUI\\Buttons\\Save.png"))
		self.BH_ERASE    = ImageTk.PhotoImage(Image.open(path + "GUI\\Buttons\\Erase.png"))
		self.BH_OFF      = ImageTk.PhotoImage(Image.open(path + "GUI\\Buttons\\Off.png"))
		self.PH_SEP      = ImageTk.PhotoImage(Image.open(path + "GUI\\Separator.png"))
                self.BH_DELETE   = ImageTk.PhotoImage(Image.open(path + "GUI\\Buttons\\Delete.png"))

                # Tk object of window
                self.TK = tk_obj

                # initialization main parts of interface
                self.Bar()
                self.Body()
                self.Stat()

                self.Refresh()

	###################################
	# TECHNICAL                       #
	# METHODS                         #
	###################################

	def docs(self): # start documentation
		os.startfile(self.PATH + "PLG\\Docs\\Main.html")

	def new_book(self): # mechanical part of inserting new book by GUI
		if self.ROOT3: # if opened 3-level's window
			self.close_root3() # then destroy window

		# getting data
                self.CLASS   = self.ROOT2.get()["e1"]
                self.NAME    = self.ROOT2.get()["e2"]
                self.SUBJECT = self.ROOT2.get()["e3"]
                self.AUTHOR  = self.ROOT2.get()["e4"]
                self.PUBLISH = self.ROOT2.get()["e5"]

		# creating new book
		try:
			self.RCREATE = self.DB.new_book(self.CLASS, self.NAME, self.SUBJECT, self.AUTHOR, self.PUBLISH)
			if self.RCREATE: # if ok
				self.close_root2() # close 2-level's window
				self.Refresh() # refresh statics
			else:
				self.Error(u"Такая книга уже существует!") # if error

		except OperationalError:
			self.Error(u"Соединение с сервером разорвано!\nПроверьте работоспособность вашего\nсервера базы данных.")

	def handler_new(self): # if there are books like that book
		# getting data
                self.CLASS   = self.ROOT2.get()["e1"]
                self.NAME    = self.ROOT2.get()["e2"]
                self.SUBJECT = self.ROOT2.get()["e3"]
                self.AUTHOR  = self.ROOT2.get()["e4"]
                self.PUBLISH = self.ROOT2.get()["e5"]

		try:
			if not(self.CLASS and self.SUBJECT and self.NAME and self.AUTHOR and self.PUBLISH): # if some entries are empty
				self.Error(u"Введите все данные\nв поля ввода!") # generate window of error

			elif len(self.DB.crt_books(CLASS=self.CLASS, NAME=None, SUBJECT=self.SUBJECT, AUTHOR=self.AUTHOR, PUBLISH=self.PUBLISH)[0]) != 0: # if there are some books like that
				if not self.ROOT3: # opened 3-level's window?
                                        # form
                                        self.ROOT3 = form.Form(title=u" BookStore | Уведомление", height=300, width=450, protocol=self.close_root3)

                                        # head of form
					self.ROOT3["title"]  = tk.Label(self.ROOT3.HEAD,
                                                                        text=u"Уведомление",
                                                                        font=(self.FT, 17),
                                                                        bg=self.color_bar,
                                                                        fg="#EFEFEF")
                                        self.ROOT3["title"].pack(fill=tk.X)

                                        # content of form
					self.ROOT3["info"]   = tk.Label(self.ROOT3.BODY,
                                                                        text=u"Уже существуют схожие книги в базе\n\nПродолжать создание?",
                                                                        font=(self.FT, 12),
                                                                        bg=self.color_bg, height=6)
                                        self.ROOT3["info"].pack()

                                        # submit of form
					self.ROOT3["submit"] = tk.Button(self.ROOT3.BODY,
                                                                         text=u"Продолжить",
                                                                         font=(self.FT, 13),
                                                                         bg=self.color_high_bg, width=20,
                                                                         command=self.new_book, bd=0)
                                        self.ROOT3["submit"].pack()

                                        self.ROOT3.start_form(x=250, y=500) # starting window

			else: # if ok
					self.new_book()
		except OperationalError:
			self.Error(u"Соединение с сервером разорвано!\nПроверьте работоспособность вашего\nсервера базы данных.")

        def add_book(self):
		# getting data from entries
                try:
                        self.ID   = int(self.ROOT2["table"].get().split("|")[0])
                except:
                        self.Error(u"Выберите книгу из списка!")
                        return None

		self.YEAR = self.ROOT2.get()["e1"]
		self.HOW  = self.ROOT2.get()["e2"]
		self.PRC  = self.ROOT2.get()["e3"]

		# checking types
		try:
			self.YEAR = int(self.YEAR)
			self.HOW  = int(self.HOW)
			self.PRC  = float(self.PRC)
		except:
			self.YEAR = 0.1 # special literal for identification error

		# checking data
		if not(self.YEAR and self.HOW and self.PRC): # if some entries are empty
                        print "aaa"
			self.Error(u"Введите все данные\nв поля ввода!") # generate window of error

		elif self.YEAR == 0.1: # if types of data in entries is not correct
			self.Error(u"Ошибка типов данных!")

		elif self.YEAR < 2000: # if year is so old
			self.Error(u"Слишком ранний год!")

		elif self.HOW <= 0:
			self.Error(u"Отрицательное\nили нулевое\nколичество!")

		elif self.PRC < 0:
			self.Error(u"Отрицательная\nцена!")

		else: # if ok
			try:
				self.DB.new_get(self.ID, self.YEAR, self.HOW, self.PRC) # new record of control db
				self.close_root2() # close 3-level's window
				self.Refresh()
			except OperationalError:
				self.Error(u"Соединение с сервером разорвано!\nПроверьте работоспособность вашего\nсервера базы данных.")

        def off_book(self):
		# getting data from entries
                try:
                        self.ID   = int(self.ROOT2["table"].get().split("|")[0])
                except:
                        self.Error(u"Выберите книгу из списка!")
                        return None

		self.YEAR = self.ROOT2.get()["e1"]
		self.HOW  = self.ROOT2.get()["e2"]

		# checking types
		try:
			self.YEAR = int(self.YEAR)
			self.HOW  = int(self.HOW)
		except:
			self.YEAR = 0.1 # special literal for identification error

		# checking data
		if not(self.YEAR and self.HOW): # if some entries are empty
			self.Error(u"Введите все данные\nв поля ввода!") # generate window of error

		elif self.YEAR == 0.1: # if types of data in entries is not correct
			self.Error(u"Ошибка типов данных!")

		elif self.YEAR < 2000: # if year is so old
			self.Error(u"Слишком ранний год!")

		elif self.HOW <= 0:
			self.Error(u"Отрицательное\nили нулевое\nколичество!")

                elif self.DB.one_book(self.ID)["AMOUNT"] - self.HOW < 0:
                        self.Error(u"Нет необходимого числа книг!")

		else: # if ok
			try:
				self.DB.new_off(self.ID, self.YEAR, self.HOW) # new record of control db
				self.close_root2() # close 3-level's window
				self.Refresh()
			except OperationalError:
				self.Error(u"Соединение с сервером разорвано!\nПроверьте работоспособность вашего\nсервера базы данных.")

        def primary_search(self):
                if self.DB.how_all_books() == 0: return None
                for self.e in self.DB.search(self.DB.classes()[0]):
                        self.LINE = u""

                        if self.e["ID"] < 10:
				self.LINE += "000000"
			elif self.e["ID"] > 9 and self.e["ID"] < 100:
				self.LINE += "00000"
			elif self.e["ID"] > 99 and self.e["ID"] < 1000:
				self.LINE += "0000"
			elif self.e["ID"] > 999 and self.e["ID"] < 10000:
				self.LINE += "000"
			elif self.e["ID"] > 9999 and self.e["ID"] < 100000:
				self.LINE += "00"
			elif self.e["ID"] > 99999 and self.e["ID"] < 1000000:
				self.LINE += "0"

                        self.LINE += str(self.e["ID"]) + " | " # append ID into line
                        self.LINE += self.e["CLASS"] + ", "  + self.e["SUBJECT"] + ", "  + self.e["NAME"] + ", "  + self.e["AUTHOR"] + ", "  + self.e["PUBLISH"] + u"\nВсего: " + str(self.e["AMOUNT"]) + u", Стоимость: " + str(self.e["COST"])

                        self.ROOT2["table"].insert(self.LINE)

        def search(self, event):
                self.searching = self.ROOT2.get()["e_search"]
                if self.searching == "": return None
                self.ROOT2["table"].erase()

                for self.e in self.DB.search(self.searching):
                        self.LINE = u""

                        if self.e["ID"] < 10:
				self.LINE += "000000"
			elif self.e["ID"] > 9 and self.e["ID"] < 100:
				self.LINE += "00000"
			elif self.e["ID"] > 99 and self.e["ID"] < 1000:
				self.LINE += "0000"
			elif self.e["ID"] > 999 and self.e["ID"] < 10000:
				self.LINE += "000"
			elif self.e["ID"] > 9999 and self.e["ID"] < 100000:
				self.LINE += "00"
			elif self.e["ID"] > 99999 and self.e["ID"] < 1000000:
				self.LINE += "0"

                        self.LINE += str(self.e["ID"]) + " | " # append ID into line
                        self.LINE += self.e["CLASS"] + ", "  + self.e["SUBJECT"] + ", "  + self.e["NAME"] + ", "  + self.e["AUTHOR"] + ", "  + self.e["PUBLISH"] + u"\nВсего: " + str(self.e["AMOUNT"]) + u", Стоимость: " + str(self.e["COST"])

                        self.ROOT2["table"].insert(self.LINE)

        def delete_book(self):
		# deleting book
		try:
			self.DB.delete_book(int(self.ROOT2["table"].get().split("|")[0]))
			self.close_root2() # close 2-level's window
                        self.Refresh()
		except OperationalError:
			self.Error(u"Соединение с сервером разорвано!\nПроверьте работоспособность вашего\nсервера базы данных.")

	def set_e1(self): # set username's entry
		if self.ROOT2["pagebook"]["current"]["val1"].get(): # remember
			self.ROOT2["pagebook"]["current"]["e1"]["state"] = tk.NORMAL
			self.ROOT2["pagebook"]["current"]["e1"]["bg"] = "white"
		else: # don't remember
			self.ROOT2["pagebook"]["current"]["e1"].delete(0, tk.END)
			self.ROOT2["pagebook"]["current"]["e1"]["state"] = tk.DISABLED
			self.ROOT2["pagebook"]["current"]["e1"]["bg"] = self.color_bg

	def set_e2(self): # set password's entry
		if self.ROOT2["pagebook"]["current"]["val2"].get(): # remember
			self.ROOT2["pagebook"]["current"]["e2"]["state"] = tk.NORMAL
			self.ROOT2["pagebook"]["current"]["e2"]["bg"] = "white"
		else: # don't remember
			self.ROOT2["pagebook"]["current"]["e2"].delete(0, tk.END)
			self.ROOT2["pagebook"]["current"]["e2"]["state"] = tk.DISABLED
			self.ROOT2["pagebook"]["current"]["e2"]["bg"] = self.color_bg

	def save_sets(self): # saver of settings
                try:
                        self.ST["USER"]    = self.ROOT2["pagebook"][1].get()["e1"]
                        self.ST["PWD"]     = self.ROOT2["pagebook"][1].get()["e2"]

                        self.ST["SOCK"]    = self.ROOT2["pagebook"][2].get()["e1"]
                        self.ST["DB_NAME"] = self.ROOT2["pagebook"][2].get()["e2"]

                        self.ST["EXC_DIR"] = self.ROOT2["pagebook"][3].get()["e1"]

                except:
                        self.Error(u"Ошибка сохранения!")
                else:
                        self.close_root2()
                        # form
                        self.ROOT4 = form.Form(title=u" BookStore | Уведомление", height=250, width=500)

		        self.ROOT4["title"] = tk.Label(self.ROOT4.HEAD,
                                                       text=u"Уведомление", font=(self.FT, 17),
                                                       bg=self.color_bar, fg="#EFEFEF") # head
		        self.ROOT4["title"].pack(fill=tk.X)

		        self.ROOT4["info"] = tk.Label(self.ROOT4.BODY,
                                                      text=u"Настройки успешно сохранены!", font=(self.FT, 12),
                                                      bg=self.color_bg, height=5)
		        self.ROOT4["info"].pack()

                        self.ROOT4.start_form()

	def export_table(self):
                try:
                        # generate table by criterions
		        self.XL.generate(self.ROOT2.get()["val1"], self.ROOT2.get()["val2"],
                                         self.ROOT2.get()["val3"], self.ROOT2.get()["val4"])
		        self.close_root2() # close 2-level's window
                except OperationalError:
                        self.Error(u"Соединение с сервером разорвано!\nПроверьте работоспособность вашего\nсервера базы данных.")

	###################################
	# GRAPHICS                        #
	# METHODS                         #
	###################################

        def Refresh(self):
                self.SVAL1.set(str(self.DB.how_all_books()))
                self.SVAL2.set(str(self.DB.how_all_inst()))
                self.SVAL3.set(str(self.DB.cost_all_books()))

	def Error(self, text):
                # form
                self.EROOT = form.Form(title=u" BookStore | Ошибка", height=250, width=500)

                # head of form
		self.EROOT["title"] = tk.Label(self.EROOT.HEAD, text=u"Ошибка", font=(self.FT, 17), bg=self.color_bar, fg="#EFEFEF") # head
		self.EROOT["title"].pack(fill=tk.X)

		self.EROOT["content"] = tk.Label(self.EROOT.BODY, text=text, font=(self.FT, 12), bg=self.color_bg, height=5)
		self.EROOT["content"].pack()

                self.EROOT.start_form(x=250, y=500)

        def Bar(self):
                # padding of frame
                self.HEAD["padx"] = 5
                self.HEAD["pady"] = 3

                # logo of bookstore
                self.LOGO = tk.Label(self.HEAD, image=self.PH_LOGO, bg=self.color_bar)
                self.LOGO.pack(side="left")

                # toggle of modes (ActionView and BooksView)
                self.BTOGGLE = tk.Button(self.HEAD, image=self.PH_ARR, bg=self.color_bar,
                                         bd=0, activebackground=self.color_bar,
                                         activeforeground="#E8E8E8", command=self.TOGGLE)
                self.BTOGGLE.pack(side="right")

        def Body(self):
                self.AREA = area.Area(self.PATH, self.BODY, self.TK,
                                      (self.New_book, self.Add_books, self.Off_books, self.Export, self.Connection, self.Settings),
                                      self.color_bg, self.color_high_bg)
                self.AREA.pack()

        def Stat(self):
                # statics
                self.SVAL1 = tk.StringVar()
                self.SVAL1.set("0")

                self.SVAL2 = tk.StringVar()
                self.SVAL2.set("0")

                self.SVAL3 = tk.StringVar()
                self.SVAL3.set("0.0")

                # how many books
                self.SHOW = tk.Label(self.STAT, text=u"  Книг:", font=(self.FT, 13), bg=self.color_bar,
                                     fg="#E8E8E8")
                self.SHOW.pack(side="left")

                self.HOW = tk.Label(self.STAT, textvariable=self.SVAL1, font=(self.FT, 13),
                                    bg=self.color_bar, fg="#E8E8E8")
                self.HOW.pack(side="left")

                # how many instances
                self.SINST = tk.Label(self.STAT, text=u" Экземпляров:", font=(self.FT, 13), bg=self.color_bar,
                                      fg="#E8E8E8")
                self.SINST.pack(side="left")

                self.INST = tk.Label(self.STAT, textvariable=self.SVAL2, font=(self.FT, 13),
                                    bg=self.color_bar, fg="#E8E8E8")
                self.INST.pack(side="left")

                # how much cost
                self.SCOST = tk.Label(self.STAT, text=u" Стоимость:", font=(self.FT, 13), bg=self.color_bar,
                                      fg="#E8E8E8")
                self.SCOST.pack(side="left")

                self.COST = tk.Label(self.STAT, textvariable=self.SVAL3, font=(self.FT, 13),
                                    bg=self.color_bar, fg="#E8E8E8")
                self.COST.pack(side="left")

		self.BDOCS = tk.Button(self.STAT, image=self.PH_HELP, bg=self.color_bar, bd=0,
                                        activebackground=self.color_high_bar, command=self.docs)
		self.BDOCS.pack(side="right")

                self.BEXIT = tk.Button(self.STAT, image=self.PH_EXIT, bg=self.color_bar, width=110,
                                       activebackground=self.color_high_bar, bd=0, command=self.close, anchor="w")
                self.BEXIT.pack(side="right")

        def New_book(self, event):
                try:
                        self.DB.all_books()
                except OperationalError:
                        self.Error(u"Соединение с сервером разорвано!\nПроверьте работоспособность вашего\nсервера базы данных.")
                        return None

		if not self.ROOT2: # opened 2-level's window?
			# form
                        self.ROOT2 = form.Form(title=u" BookStore | Новая книга", height=350, width=550, protocol=self.close_root2)

                        # head of form
			self.ROOT2["title"] = tk.Label(self.ROOT2.HEAD,
                                                       text=u"Новая книга", font=(self.FT, 17),
                                                       bg=self.color_bar, fg="#EFEFEF")
                        self.ROOT2["title"].pack(fill=tk.X)

			# labels of entries in form
			self.ROOT2["l1"] = tk.Label(self.ROOT2.BODY,
                                                    text=u"Класс:", font=(self.FT, 13),
                                                    bg=self.color_bg, anchor="w", width=20)
                        self.ROOT2["l1"].grid(row=0, column=0)

			self.ROOT2["l2"] = tk.Label(self.ROOT2.BODY,
                                                    text=u"Наименование:", font=(self.FT, 13),
                                                    bg=self.color_bg, anchor="w", width=20)
                        self.ROOT2["l2"].grid(row=1, column=0)

			self.ROOT2["l3"] = tk.Label(self.ROOT2.BODY,
                                                    text=u"Предмет:", font=(self.FT, 13),
                                                    bg=self.color_bg, anchor="w", width=20)
                        self.ROOT2["l3"].grid(row=2, column=0)

			self.ROOT2["l4"] = tk.Label(self.ROOT2.BODY,
                                                    text=u"Автор:", font=(self.FT, 13),
                                                    bg=self.color_bg, anchor="w", width=20)
                        self.ROOT2["l4"].grid(row=3, column=0)

			self.ROOT2["l5"] = tk.Label(self.ROOT2.BODY,
                                                    text=u"Издательство:", font=(self.FT, 13),
                                                    bg=self.color_bg, anchor="w", width=20)
                        self.ROOT2["l5"].grid(row=4, column=0)

			# entries of form
			self.ROOT2["e1"] = tk.Entry(self.ROOT2.BODY, width=31,
                                                    font=(self.FT, 13), bd=1)
                        self.ROOT2["e1"].grid(row=0, column=1)

			self.ROOT2["e2"] = tk.Entry(self.ROOT2.BODY, width=31,
                                                    font=(self.FT, 13), bd=1)
                        self.ROOT2["e2"].grid(row=1, column=1)

			self.ROOT2["e3"] = ttk.Combobox(self.ROOT2.BODY, width=32,font=(self.FT, 12),
                                                        values=self.DB.subjects())
                        self.ROOT2["e3"].grid(row=2, column=1)

			self.ROOT2["e4"] = ttk.Combobox(self.ROOT2.BODY, width=32, font=(self.FT, 12),
                                                        values=self.DB.authors())
                        self.ROOT2["e4"].grid(row=3, column=1)

			self.ROOT2["e5"] = ttk.Combobox(self.ROOT2.BODY, width=32, font=(self.FT, 12),
                                                        values=self.DB.publishes())
                        self.ROOT2["e5"].grid(row=4, column=1)

			# empty separator and button
			self.ROOT2["sep"] = tk.Label(self.ROOT2.BODY, text="-", foreground=self.color_bg,
                                                     bg=self.color_bg, height=3)
                        self.ROOT2["sep"].grid(row=5, column=0)

			self.ROOT2["submit"] = tk.Button(self.ROOT2.BODY, image=self.BH_SAVE,
                                                         bg=self.color_bg, command=self.handler_new, width=170,
                                                         bd=0, activebackground=self.color_bg)
                        self.ROOT2["submit"].grid(row=6, column=0, sticky="w")

			self.ROOT2["cancel"] = tk.Button(self.ROOT2.BODY, image=self.BH_CANCEL,
                                                         bg=self.color_bg, command=self.close_root2, width=170,
                                                         bd=0, activebackground=self.color_bg)
                        self.ROOT2["cancel"].grid(row=6, column=1, sticky="e")

                        self.ROOT2.start_form()

        def Delete_book(self, event):
                try:
                        self.DB.all_books()
                except OperationalError:
                        self.Error(u"Соединение с сервером разорвано!\nПроверьте работоспособность вашего\nсервера базы данных.")
                        return None

		if not self.ROOT2: # opened 2-level's window?
			# form
                        self.ROOT2 = form.Form(title=u" BookStore | Удалить книгу", height=450, width=700,
                                               protocol=self.close_root2, padx=0, pady=0)

                        self.ROOT2.HEAD["pady"] = 15

                        # head of form
			self.ROOT2["title"] = tk.Label(self.ROOT2.HEAD,
                                                       text=u"Удалить книгу", font=(self.FT, 17),
                                                       bg=self.color_bar, fg="#EFEFEF")
                        self.ROOT2["title"].pack(fill=tk.X)

                        self.ROOT2["f_search"] = tk.Frame(self.ROOT2.BODY, bg=self.color_bar, bd=1)
                        self.ROOT2["f_search"].pack(fill=tk.X, side="top")

                        self.ROOT2["e_search"] = tk.Entry(self.ROOT2["f_search"], bg=self.color_bg, font=(self.FT, 13),
                                                          relief=tk.FLAT, bd=0)
                        self.ROOT2["e_search"].pack(fill=tk.X)

                        self.ROOT2["b_search"] = tk.Label(self.ROOT2["f_search"], bg=self.color_high_bg,
                                                           font=(self.FT, 13), relief=tk.FLAT, bd=0, text=u"   Поиск   ")
                        self.ROOT2["b_search"].bind("<ButtonPress>", self.search)
                        self.ROOT2["b_search"].place(x=700, y=0, anchor="ne")

                        self.ROOT2["books"] = tk.Frame(self.ROOT2.BODY, bg="#D5D5D5", bd=1)
                        self.ROOT2["books"].pack(fill=tk.BOTH, expand=1)

                        self.ROOT2["buttons"] = tk.Frame(self.ROOT2.BODY, bg=self.color_bg, padx=20, pady=20)
                        self.ROOT2["buttons"].pack(fill=tk.X, side="bottom")

                        self.ROOT2["submit"] = tk.Button(self.ROOT2["buttons"], bd=0, bg=self.color_bg,
                                                         image=self.BH_DELETE, activebackground=self.color_bg,
                                                         command=self.delete_book)
                        self.ROOT2["submit"].pack(side="left")

                        self.ROOT2["cancel"] = tk.Button(self.ROOT2["buttons"], bd=0, bg=self.color_bg,
                                                         image=self.BH_CANCEL, activebackground=self.color_bg,
                                                         command=self.close_root2)
                        self.ROOT2["cancel"].pack(side="right")

                        self.ROOT2["table"] = table.Table(self.ROOT2["books"], self.PH_BOOK)
                        self.ROOT2["table"].pack()

                        self.ROOT2.start_form(y=700, x=450)

        def Add_books(self, event):
                try:
                        self.DB.all_books()
                except OperationalError:
                        self.Error(u"Соединение с сервером разорвано!\nПроверьте работоспособность вашего\nсервера базы данных.")
                        return None

		if not self.ROOT2: # opened 2-level's window?
			# form
                        self.ROOT2 = form.Form(title=u" BookStore | Пополнить книги",
                                               protocol=self.close_root2, padx=0, pady=0)

                        self.ROOT2.HEAD["pady"] = 10

                        # head of form
			self.ROOT2["title"] = tk.Label(self.ROOT2.HEAD,
                                                       text=u"Пополнить книги", font=(self.FT, 17),
                                                       bg=self.color_bar, fg="#EFEFEF")
                        self.ROOT2["title"].pack(fill=tk.X)

                        self.ROOT2["books"] = tk.Frame(self.ROOT2.BODY, bd=3, width=650, bg=self.color_bg)
                        self.ROOT2["books"].pack(fill=tk.Y, side="left")
                        self.ROOT2["books"].pack_propagate(False)

                        self.ROOT2["entries"] = tk.Frame(self.ROOT2.BODY, bd=3, bg=self.color_bg, padx=15, pady=70)
                        self.ROOT2["entries"].pack(fill=tk.BOTH, side="right", expand=1)
                        self.ROOT2["entries"].pack_propagate(False)

                        self.ROOT2["f_search"] = tk.Frame(self.ROOT2["books"], bg=self.color_high_bg, bd=1)
                        self.ROOT2["f_search"].pack(fill=tk.X, side="top")

                        self.ROOT2["e_search"] = tk.Entry(self.ROOT2["f_search"], bg=self.color_bg, font=(self.FT, 13),
                                                          relief=tk.FLAT, bd=0)
                        self.ROOT2["e_search"].pack(fill=tk.X)

                        self.ROOT2["b_search"] = tk.Label(self.ROOT2["f_search"], bg=self.color_high_bg,
                                                           font=(self.FT, 13), relief=tk.FLAT, bd=0, text=u"   Поиск   ")
                        self.ROOT2["b_search"].bind("<ButtonPress>", self.search)
                        self.ROOT2["b_search"].place(relx=1.0, rely=0, anchor="ne")

                        self.ROOT2["table"] = table.Table(self.ROOT2["books"], self.PH_BOOK, font=("Calibri", 10))
                        self.ROOT2["table"].pack()

			# help-labels of entries
			self.ROOT2["l1"] = tk.Label(self.ROOT2["entries"], text=u"Год получения:", font=(self.FT, 13),
                                                    bg=self.color_bg, anchor="w", width=15)
			self.ROOT2["l2"] = tk.Label(self.ROOT2["entries"], text=u"Количество:", font=(self.FT, 13),
                                                    bg=self.color_bg, anchor="w", width=15)
			self.ROOT2["l3"] = tk.Label(self.ROOT2["entries"], text=u"Цена одной:", font=(self.FT, 13),
                                                    bg=self.color_bg, anchor="w", width=15)

			self.ROOT2["l1"].grid(row=0, column=0, pady=5)
			self.ROOT2["l2"].grid(row=1, column=0, pady=5)
			self.ROOT2["l3"].grid(row=2, column=0, pady=5)

			# entries
			self.ROOT2["e1"] = tk.Entry(self.ROOT2["entries"], width=10, font=(self.FT, 13), bd=1)
			self.ROOT2["e2"] = tk.Entry(self.ROOT2["entries"], width=10, font=(self.FT, 13), bd=1)
			self.ROOT2["e3"] = tk.Entry(self.ROOT2["entries"], width=10, font=(self.FT, 13), bd=1)

			self.ROOT2["e1"].grid(row=0, column=1)
			self.ROOT2["e2"].grid(row=1, column=1)
			self.ROOT2["e3"].grid(row=2, column=1)

                        self.ROOT2["submit"] = tk.Button(self.ROOT2["entries"], bd=0, bg=self.color_bg,
                                                         image=self.BH_ADD, activebackground=self.color_bg,
                                                         command=self.add_book)
                        self.ROOT2["submit"].pack(side="bottom")

                        self.primary_search()

                        self.ROOT2.start_form(y=1000, x=500)

        def Off_books(self, event):
                try:
                        self.DB.all_books()
                except OperationalError:
                        self.Error(u"Соединение с сервером разорвано!\nПроверьте работоспособность вашего\nсервера базы данных.")
                        return None

		if not self.ROOT2: # opened 2-level's window?
			# form
                        self.ROOT2 = form.Form(title=u" BookStore | Списать книги",
                                               protocol=self.close_root2, padx=0, pady=0)

                        self.ROOT2.HEAD["pady"] = 10

                        # head of form
			self.ROOT2["title"] = tk.Label(self.ROOT2.HEAD,
                                                       text=u"Списать книги", font=(self.FT, 17),
                                                       bg=self.color_bar, fg="#EFEFEF")
                        self.ROOT2["title"].pack(fill=tk.X)

                        self.ROOT2["books"] = tk.Frame(self.ROOT2.BODY, bd=3, width=650, bg=self.color_bg)
                        self.ROOT2["books"].pack(fill=tk.Y, side="left")
                        self.ROOT2["books"].pack_propagate(False)

                        self.ROOT2["entries"] = tk.Frame(self.ROOT2.BODY, bd=3, bg=self.color_bg, padx=15, pady=70)
                        self.ROOT2["entries"].pack(fill=tk.BOTH, side="right", expand=1)
                        self.ROOT2["entries"].pack_propagate(False)

                        self.ROOT2["f_search"] = tk.Frame(self.ROOT2["books"], bg=self.color_high_bg, bd=1)
                        self.ROOT2["f_search"].pack(fill=tk.X, side="top")

                        self.ROOT2["e_search"] = tk.Entry(self.ROOT2["f_search"], bg=self.color_bg, font=(self.FT, 13),
                                                          relief=tk.FLAT, bd=0)
                        self.ROOT2["e_search"].pack(fill=tk.X)

                        self.ROOT2["b_search"] = tk.Label(self.ROOT2["f_search"], bg=self.color_high_bg,
                                                           font=(self.FT, 13), relief=tk.FLAT, bd=0, text=u"   Поиск   ")
                        self.ROOT2["b_search"].bind("<ButtonPress>", self.search)
                        self.ROOT2["b_search"].place(relx=1.0, rely=0, anchor="ne")

                        self.ROOT2["table"] = table.Table(self.ROOT2["books"], self.PH_BOOK, font=("Calibri", 10))
                        self.ROOT2["table"].pack()

			# help-labels of entries
			self.ROOT2["l1"] = tk.Label(self.ROOT2["entries"], text=u"Год списания:", font=(self.FT, 13),
                                                    bg=self.color_bg, anchor="w", width=15)
			self.ROOT2["l2"] = tk.Label(self.ROOT2["entries"], text=u"Количество:", font=(self.FT, 13),
                                                    bg=self.color_bg, anchor="w", width=15)

			self.ROOT2["l1"].grid(row=0, column=0, pady=5)
			self.ROOT2["l2"].grid(row=1, column=0, pady=5)

			# entries
			self.ROOT2["e1"] = tk.Entry(self.ROOT2["entries"], width=10, font=(self.FT, 13), bd=1)
			self.ROOT2["e2"] = tk.Entry(self.ROOT2["entries"], width=10, font=(self.FT, 13), bd=1)

			self.ROOT2["e1"].grid(row=0, column=1)
			self.ROOT2["e2"].grid(row=1, column=1)

                        self.ROOT2["submit"] = tk.Button(self.ROOT2["entries"], bd=0, bg=self.color_bg,
                                                         image=self.BH_OFF, activebackground=self.color_bg,
                                                         command=self.off_book)
                        self.ROOT2["submit"].pack(side="bottom")

                        self.primary_search()

                        self.ROOT2.start_form(y=1000, x=500)

	def Set_login(self): # not fill-method of Pagebook
		self.ROOT2["pagebook"][1]["val1"] = tk.BooleanVar() # trigger of remembering username
		self.ROOT2["pagebook"][1]["val1"].set(bool(self.ST["USER"]))

		self.ROOT2["pagebook"][1]["val2"] = tk.BooleanVar() # trigger of remembering password
		self.ROOT2["pagebook"][1]["val2"].set(bool(self.ST["PWD"]))

		# username part
		self.ROOT2["pagebook"][1]["l1"]  = tk.Label(self.ROOT2["pagebook"][1].BODY,
                                                                    text=u"Логин:", font=(self.FT, 12),
                                                                    bg=self.color_bg, width=10, anchor="w")
		self.ROOT2["pagebook"][1]["e1"]  = tk.Entry(self.ROOT2["pagebook"][1].BODY,
                                                                    width=30, font=(self.FT, 12))
                # insert username from Sets object
		self.ROOT2["pagebook"][1]["e1"].insert(tk.END, self.ST["USER"])
		self.ROOT2["pagebook"][1]["c1"] = tk.Checkbutton(self.ROOT2["pagebook"][1].BODY,
                                                                         text=u"Хранить стандартный логин?",
                                                                         bg=self.color_bg, anchor="w", width=40,
                                                                         font=(self.FT, 11),
                                                                         variable=self.ROOT2["pagebook"][1]["val1"],
                                                                         onvalue=True, offvalue=False,
                                                                         command=self.set_e1,
                                                                         activebackground=self.color_bg)
                # if needn't save login -> disable login's entry
		if not self.ROOT2["pagebook"][1]["val1"].get():
                        self.ROOT2["pagebook"][1]["e1"]["state"] = tk.DISABLED

		self.ROOT2["pagebook"][1]["l1"].grid(row=0, column=0)
		self.ROOT2["pagebook"][1]["e1"].grid(row=0, column=1)
		self.ROOT2["pagebook"][1]["c1"].grid(row=1, column=0, columnspan=2)

		# empty separator
		self.ROOT2["pagebook"][1]["sp1"]  = tk.Label(self.ROOT2["pagebook"][1].BODY,
                                                                     text=u"-", font=(self.FT, 12),
                                                                     bg=self.color_bg, width=20, fg=self.color_bg)
		self.ROOT2["pagebook"][1]["sp1"].grid(row=2, column=0, columnspan=2)

		# password part
		self.ROOT2["pagebook"][1]["l2"]  = tk.Label(self.ROOT2["pagebook"][1].BODY,
                                                            text=u"Пароль:", font=(self.FT, 12),
                                                            bg=self.color_bg, width=10, anchor="w")
		self.ROOT2["pagebook"][1]["e2"]  = tk.Entry(self.ROOT2["pagebook"][1].BODY,
                                                            width=30, font=(self.FT, 12), show="•")

                # insert password from Sets object
		self.ROOT2["pagebook"][1]["e2"].insert(tk.END, self.ST["PWD"])
		self.ROOT2["pagebook"][1]["c2"] = tk.Checkbutton(self.ROOT2["pagebook"][1].BODY,
                                                                 text=u"Хранить ваш пароль?",
                                                                 bg=self.color_bg, anchor="w", width=40,
                                                                 font=(self.FT, 11),
                                                                 variable=self.ROOT2["pagebook"][1]["val2"],
                                                                 onvalue=True, offvalue=False,
                                                                 command=self.set_e2, activebackground=self.color_bg)
		if not self.ROOT2["pagebook"][1]["val2"].get():
                        self.ROOT2["pagebook"][1]["e2"]["state"] = tk.DISABLED

		self.ROOT2["pagebook"][1]["l2"].grid(row=3, column=0)
		self.ROOT2["pagebook"][1]["e2"].grid(row=3, column=1)
		self.ROOT2["pagebook"][1]["c2"].grid(row=4, column=0, columnspan=2)

		# empty separator
		self.ROOT2["pagebook"][1]["sp2"]  = tk.Label(self.ROOT2["pagebook"][1].BODY,
                                                                     text=u"-", font=(self.FT, 12),
                                                                     bg=self.color_bg, width=20, fg=self.color_bg)
		self.ROOT2["pagebook"][1]["sp2"].grid(row=5, column=0, columnspan=2)

	def Set_db(self): # not fill-method of Pagebook
		self.ROOT2["pagebook"][2]["val1"] = tk.BooleanVar() # trigger of remembering username
		self.ROOT2["pagebook"][2]["val1"].set(bool(self.ST["DB_NAME"]))

		self.ROOT2["pagebook"][2]["val2"] = tk.BooleanVar() # trigger of remembering password
		self.ROOT2["pagebook"][2]["val2"].set(bool(self.ST["SOCK"]))

		# username part
		self.ROOT2["pagebook"][2]["l1"]  = tk.Label(self.ROOT2["pagebook"][2].BODY,
                                                                    text=u"Сокет:", font=(self.FT, 12),
                                                                    bg=self.color_bg, width=10, anchor="w")
		self.ROOT2["pagebook"][2]["e1"]  = tk.Entry(self.ROOT2["pagebook"][2].BODY,
                                                                    width=30, font=(self.FT, 12))
                # insert username from Sets object
		self.ROOT2["pagebook"][2]["e1"].insert(tk.END, self.ST["SOCK"])
		self.ROOT2["pagebook"][2]["c1"] = tk.Checkbutton(self.ROOT2["pagebook"][2].BODY,
                                                                         text=u"Хранить стандартный адрес БД?",
                                                                         bg=self.color_bg, anchor="w", width=40,
                                                                         font=(self.FT, 11),
                                                                         variable=self.ROOT2["pagebook"][2]["val1"],
                                                                         onvalue=True, offvalue=False,
                                                                         command=self.set_e1,
                                                                         activebackground=self.color_bg)
                # if needn't save login -> disable login's entry
		if not self.ROOT2["pagebook"][2]["val1"].get():
                        self.ROOT2["pagebook"][2]["e1"]["state"] = tk.DISABLED

		self.ROOT2["pagebook"][2]["l1"].grid(row=0, column=0)
		self.ROOT2["pagebook"][2]["e1"].grid(row=0, column=1)
		self.ROOT2["pagebook"][2]["c1"].grid(row=1, column=0, columnspan=2)

		# empty separator
		self.ROOT2["pagebook"][2]["sp1"]  = tk.Label(self.ROOT2["pagebook"][2].BODY,
                                                                     text=u"-", font=(self.FT, 12),
                                                                     bg=self.color_bg, width=20, fg=self.color_bg)
		self.ROOT2["pagebook"][2]["sp1"].grid(row=2, column=0, columnspan=2)

		# password part
		self.ROOT2["pagebook"][2]["l2"]  = tk.Label(self.ROOT2["pagebook"][2].BODY,
                                                            text=u"Имя БД:", font=(self.FT, 12),
                                                            bg=self.color_bg, width=10, anchor="w")
		self.ROOT2["pagebook"][2]["e2"]  = tk.Entry(self.ROOT2["pagebook"][2].BODY,
                                                            width=30, font=(self.FT, 12))

                # insert password from Sets object
		self.ROOT2["pagebook"][2]["e2"].insert(tk.END, self.ST["DB_NAME"])
		self.ROOT2["pagebook"][2]["c2"] = tk.Checkbutton(self.ROOT2["pagebook"][2].BODY,
                                                                 text=u"Хранить имя БД?",
                                                                 bg=self.color_bg, anchor="w", width=40,
                                                                 font=(self.FT, 11),
                                                                 variable=self.ROOT2["pagebook"][2]["val2"],
                                                                 onvalue=True, offvalue=False,
                                                                 command=self.set_e2, activebackground=self.color_bg)
		if not self.ROOT2["pagebook"][2]["val2"].get():
                        self.ROOT2["pagebook"][2]["e2"]["state"] = tk.DISABLED

		self.ROOT2["pagebook"][2]["l2"].grid(row=3, column=0)
		self.ROOT2["pagebook"][2]["e2"].grid(row=3, column=1)
		self.ROOT2["pagebook"][2]["c2"].grid(row=4, column=0, columnspan=2)

		# empty separator
		self.ROOT2["pagebook"][2]["sp2"]  = tk.Label(self.ROOT2["pagebook"][2].BODY,
                                                                     text=u"-", font=(self.FT, 12),
                                                                     bg=self.color_bg, width=20, fg=self.color_bg)
		self.ROOT2["pagebook"][2]["sp2"].grid(row=5, column=0, columnspan=2)

	def Set_other(self):
		self.ROOT2["pagebook"][3]["l1"]  = tk.Label(self.ROOT2["pagebook"][3].BODY,
                                                            text=u"Папка таблиц:", font=(self.FT, 12),
                                                            bg=self.color_bg, width=17, anchor="w")
		self.ROOT2["pagebook"][3]["e1"]  = tk.Entry(self.ROOT2["pagebook"][3].BODY,
                                                            width=30, font=(self.FT, 12))

                # insert address from Sets object
		self.ROOT2["pagebook"][3]["e1"].insert(tk.END, self.ST["EXC_DIR"])

		self.ROOT2["pagebook"][3]["l1"].grid(row=0, column=0)
		self.ROOT2["pagebook"][3]["e1"].grid(row=0, column=1)

		# empty separator
		self.ROOT2["pagebook"][3]["sep"]  = tk.Label(self.ROOT2["pagebook"][3].BODY,
                                                                     text=u"-", font=(self.FT, 12),
                                                                     bg=self.color_bg, width=20, fg=self.color_bg)
		self.ROOT2["pagebook"][3]["sep"].grid(row=5, column=0, columnspan=2)

	def Settings(self, event):
		if not self.ROOT2: # opened 2-level's window?
			# form
                        self.ROOT2 = form.Form(title=u" BookStore | Настройки", height=400, width=650,
                                               protocol=self.close_root2, padx=0, pady=0)

                        # head of form
			self.ROOT2["title"] = tk.Label(self.ROOT2.HEAD,
                                                       text=u"Настройки", font=(self.FT, 17),
                                                       bg=self.color_bar, fg="#EFEFEF")
                        self.ROOT2["title"].pack(fill=tk.X)

                        # pagebook widget
                        self.ROOT2["pagebook"] = page.Pagebook(self.ROOT2.BODY)
                        self.ROOT2["pagebook"].add_page(1, u"Логин", 130, 40)
                        self.ROOT2["pagebook"].add_page(2, u"База данных", 130, 40)
                        self.ROOT2["pagebook"].add_page(3, u"Другие", 130, 40)
                        self.ROOT2["pagebook"].start_book()

                        self.Set_login()
                        self.Set_db()
                        self.Set_other()

                  	self.ROOT2["sep"] = tk.Label(self.ROOT2.BODY, font=(self.FT, 7),
                                                     text="-", foreground=self.color_bg, bg=self.color_bg, height=1)
                        self.ROOT2["sep"].pack(side="bottom")

                        self.ROOT2["buttons"] = tk.Frame(self.ROOT2.BODY, bg=self.color_bg, padx=50)
                        self.ROOT2["buttons"].pack(side="bottom", fill=tk.X)

                        self.ROOT2["submit"] = tk.Button(self.ROOT2["buttons"], image=self.BH_SAVE,
                                                         bd=0, bg=self.color_bg,
                                                         command=self.save_sets,
                                                         activebackground=self.color_bg)
                        self.ROOT2["submit"].pack(side="left")

                        self.ROOT2["cancel"] = tk.Button(self.ROOT2["buttons"], image=self.BH_CANCEL,
                                                         bd=0, bg=self.color_bg,
                                                         command=self.close_root2,
                                                         activebackground=self.color_bg)
                        self.ROOT2["cancel"].pack(side="right")

                        self.ROOT2["pagebook"].view_page(1)

                        self.ROOT2.start_form(x=400, y=650)

        def Connection(self, event):
		if not self.ROOT2: # opened 2-level's window?
                                self.ROOT2 = form.Form(title=u" BookStore | Подключение",
                                                       height=450, width=750, protocol=self.close_root2,
                                                       padx=0, pady=0)

                                # head of form
		        	self.ROOT2["title"] = tk.Label(self.ROOT2.HEAD, text=u"Подключение",
                                                               font=(self.FT, 17), bg=self.color_bar, fg="#EFEFEF")
        			self.ROOT2["title"].pack(fill=tk.X, side="top")

                                self.ROOT2.HEAD["pady"] = 8

                                self.ROOT2["url_frame"] = tk.Frame(self.ROOT2.HEAD, bg=self.color_bar, pady=4)
                                self.ROOT2["url_frame"].pack(side="bottom")
                                #self.ROOT2["url_frame"].pack_propagate(False)

                                self.ROOT2["url_label"] = tk.Label(self.ROOT2["url_frame"], text=u"   URL",
                                                                   bg=self.color_bar, font=(self.FT, 13), fg="#E8E8E8")
                                self.ROOT2["url_label"].pack(side="left")

                                self.ROOT2["url_text"] = tk.Label(self.ROOT2["url_frame"], text=" " + self.DB.URL,
                                                                  font=(self.FT, 12), fg=self.color_high_bg,
                                                                  bg=self.color_bar)
                                self.ROOT2["url_text"].pack(side="right")

                                self.ROOT2["stat_frame"] = tk.Frame(self.ROOT2.BODY, bg=self.color_bg, padx=70, pady=40)
                                self.ROOT2["stat_frame"].pack(fill=tk.BOTH, expand=1)

                                if self.DB.URL.startswith("sqlite"):
                                        self.mode = u"оффлайн режим"
                                else:
                                        self.mode = u"подключение по сети"

                                self.ROOT2["status"] = tk.Label(self.ROOT2["stat_frame"], text=u"Статус:", bg=self.color_bg,
                                                                font=(self.FT, 13), anchor="w", width=22)
                                self.ROOT2["status"].grid(row=0, column=0, pady=15)

                                self.ROOT2["status_text"] = tk.Label(self.ROOT2["stat_frame"], text=self.mode, bg=self.color_bg,
                                                                font=(self.FT, 13), anchor="w", width=40)
                                self.ROOT2["status_text"].grid(row=0, column=1, pady=15)

                                if self.mode == u"оффлайн режим":
                                        self.ROOT2["db"] = tk.Label(self.ROOT2["stat_frame"], text=u"СУБД:", bg=self.color_bg,
                                                                    font=(self.FT, 13), width=22, anchor="w")
                                        self.ROOT2["db"].grid(row=1, column=0, pady=1)

                                        self.ROOT2["db_text"] = tk.Label(self.ROOT2["stat_frame"], text="SQLite",
                                                                         font=(self.FT, 13), width=40, anchor="w", bg=self.color_bg)
                                        self.ROOT2["db_text"].grid(row=1, column=1, pady=1)

                                        self.ROOT2["file"] = tk.Label(self.ROOT2["stat_frame"], text=u"Файл БД:", bg=self.color_bg,
                                                                      font=(self.FT, 13), width=22, anchor="w")
                                        self.ROOT2["file"].grid(row=2, column=0, pady=1)

                                        self.ROOT2["file_text"] = tk.Label(self.ROOT2["stat_frame"], text=self.DB.FILE,
                                                                           font=(self.FT, 13), width=40, anchor="w", bg=self.color_bg)
                                        self.ROOT2["file_text"].grid(row=2, column=1, pady=1)

                                        self.ROOT2["time"] = tk.Label(self.ROOT2["stat_frame"], text=u"Последнее подключение:", bg=self.color_bg,
                                                                      font=(self.FT, 13), width=22, anchor="w")
                                        self.ROOT2["time"].grid(row=3, column=0, pady=15)

                                        self.ROOT2["time_text"] = tk.Label(self.ROOT2["stat_frame"], text=self.DB.TIME,
                                                                           font=(self.FT, 13), width=40, anchor="w", bg=self.color_bg)
                                        self.ROOT2["time_text"].grid(row=3, column=1, pady=15)
                                else:
                                        self.ROOT2["db"] = tk.Label(self.ROOT2["stat_frame"], text=u"СУБД:", bg=self.color_bg,
                                                                    font=(self.FT, 13), width=22, anchor="w")
                                        self.ROOT2["db"].grid(row=1, column=0, pady=1)

                                        self.ROOT2["db_text"] = tk.Label(self.ROOT2["stat_frame"], text="PostgreSQL",
                                                                         font=(self.FT, 13), width=40, anchor="w", bg=self.color_bg)
                                        self.ROOT2["db_text"].grid(row=1, column=1, pady=1)

                                        self.ROOT2["host"] = tk.Label(self.ROOT2["stat_frame"], text=u"Сервер:", bg=self.color_bg,
                                                                      font=(self.FT, 13), width=22, anchor="w")
                                        self.ROOT2["host"].grid(row=2, column=0, pady=1)

                                        self.ROOT2["host_text"] = tk.Label(self.ROOT2["stat_frame"], text=self.DB.SOCK,
                                                                           font=(self.FT, 13), width=40, anchor="w", bg=self.color_bg)
                                        self.ROOT2["host_text"].grid(row=2, column=1, pady=1)

                                        self.ROOT2["user"] = tk.Label(self.ROOT2["stat_frame"], text=u"Пользователь:", bg=self.color_bg,
                                                                      font=(self.FT, 13), width=22, anchor="w")
                                        self.ROOT2["user"].grid(row=3, column=0, pady=1)

                                        self.ROOT2["user_text"] = tk.Label(self.ROOT2["stat_frame"], text=self.DB.LOGIN,
                                                                           font=(self.FT, 13), width=40, anchor="w", bg=self.color_bg)
                                        self.ROOT2["user_text"].grid(row=3, column=1, pady=1)

                                        self.ROOT2["name"] = tk.Label(self.ROOT2["stat_frame"], text=u"Имя БД:", bg=self.color_bg,
                                                                      font=(self.FT, 13), width=22, anchor="w")
                                        self.ROOT2["name"].grid(row=4, column=0, pady=1)

                                        self.ROOT2["name_text"] = tk.Label(self.ROOT2["stat_frame"], text=self.DB.DB,
                                                                           font=(self.FT, 13), width=40, anchor="w", bg=self.color_bg)
                                        self.ROOT2["name_text"].grid(row=4, column=1, pady=1)

                                        self.ROOT2["time"] = tk.Label(self.ROOT2["stat_frame"], text=u"Последнее подключение:", bg=self.color_bg,
                                                                      font=(self.FT, 13), width=22, anchor="w")
                                        self.ROOT2["time"].grid(row=5, column=0, pady=15)

                                        self.ROOT2["time_text"] = tk.Label(self.ROOT2["stat_frame"], text=self.DB.TIME,
                                                                           font=(self.FT, 13), width=40, anchor="w", bg=self.color_bg)
                                        self.ROOT2["time_text"].grid(row=5, column=1, pady=15)

                                self.ROOT2.start_form()

	def Export(self, event):
		if not self.ROOT2: # opened 2-level's window?
			# form
                        self.ROOT2 = form.Form(title=u" BookStore | Экспорт таблицы", height=350, width=550,
                                               protocol=self.close_root2, padx=60, pady=15)

                        # head of form
			self.ROOT2["title"] = tk.Label(self.ROOT2.HEAD, text=u"Экспорт Excel",
                                                       font=(self.FT, 17), bg=self.color_bar, fg="#EFEFEF")
			self.ROOT2["title"].pack(fill=tk.X)

			# variables of checkbuttons
			self.ROOT2["val1"]  = tk.BooleanVar()
			self.ROOT2["val1"].set(True) # default

			self.ROOT2["val2"]  = tk.BooleanVar()
			self.ROOT2["val3"]  = tk.BooleanVar()
			self.ROOT2["val4"]  = tk.BooleanVar()

                        # info
			self.ROOT2["info"] = tk.Label(self.ROOT2.BODY,
                                                      text=u"Вы можете создать отчет о книгах в библиотеке\n" +
                                                           u"в формате таблиц MS Excel.", font=(self.FT, 12),
                                                      bg=self.color_bg, height=3)
			self.ROOT2["info"].grid(row=0, column=0, columnspan=2)

			self.ROOT2["checks"] = tk.Frame(self.ROOT2.BODY, bg=self.color_bg) # frame of checkbuttons
			self.ROOT2["checks"].grid(row=1, column=0)

			# checkbuttons of criterions for generating table
			self.ROOT2["check1"] = tk.Checkbutton(self.ROOT2["checks"], bg=self.color_bg,
                                                              activebackground=self.color_bg, font=(self.FT, 12),
                                                              onvalue=True, offvalue=False,
                                                              variable=self.ROOT2["val1"], text=u"Главные данные",
                                                              anchor="w", width=30)
			self.ROOT2["check1"].grid(row=0, column=0)

			self.ROOT2["check2"] = tk.Checkbutton(self.ROOT2["checks"], bg=self.color_bg,
                                                              activebackground=self.color_bg, font=(self.FT, 12),
                                                              onvalue=True, offvalue=False,
                                                              variable=self.ROOT2["val2"], text=u"Контрольные данные",
                                                              anchor="w", width=30)
			self.ROOT2["check2"].grid(row=1, column=0)

			self.ROOT2["check3"] = tk.Checkbutton(self.ROOT2["checks"], bg=self.color_bg,
                                                              activebackground=self.color_bg, font=(self.FT, 12),
                                                              onvalue=True, offvalue=False,
                                                              variable=self.ROOT2["val3"], text=u"Сводка по предметам",
                                                              anchor="w", width=30)
			self.ROOT2["check3"].grid(row=2, column=0)

			self.ROOT2["check4"] = tk.Checkbutton(self.ROOT2["checks"], bg=self.color_bg,
                                                              activebackground=self.color_bg, font=(self.FT, 12),
                                                              onvalue=True, offvalue=False,
                                                              variable=self.ROOT2["val4"],
                                                              text=u"Сводка по издательствам", anchor="w", width=30)
			self.ROOT2["check4"].grid(row=3, column=0)

			# mini-logo of MS Excel
			self.ROOT2["logo"] = tk.Label(self.ROOT2.BODY, image=self.PH_EXC, bg=self.color_bg, bd=0)
			self.ROOT2["logo"].grid(row=1, column=1)

			# button and empty separator
			self.ROOT2["sep"] = tk.Label(self.ROOT2.BODY,
                                                     text="-", foreground=self.color_bg, bg=self.color_bg, height=3)
			self.ROOT2["submit"] = tk.Button(self.ROOT2.BODY,
                                                         image=self.BH_TABLE, bg=self.color_bg,
                                                         activebackground=self.color_bg, bd=0, command=self.export_table)

			self.ROOT2["sep"].grid(row=2, column=0, columnspan=2)
			self.ROOT2["submit"].grid(row=3, column=0, columnspan=2)

                        self.ROOT2.start_form()
