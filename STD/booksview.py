# coding: utf-8

import Tkinter as tk
import ttk, os
import form, page, listbook, vbase

import PIL.ImageTk as ImageTk
import PIL.Image as Image

from sqlalchemy.exc import OperationalError, ProgrammingError

class BooksView(vbase.VBase):
	# View-page in main table of books

	def __init__(self, tk_obj, db, xl, st, path, ft, toggle):
		# main attributes of Tk object of window
                vbase.VBase.__init__(self, tk_obj, toggle, path, db, xl, st, ft)

		# images of buttons and other graphics
		self.PH_NEW      = ImageTk.PhotoImage(Image.open(path + "GUI\\New.png"))
		self.PH_SEARCH   = ImageTk.PhotoImage(Image.open(path + "GUI\\Search.png"))
		self.PH_EXPORT   = ImageTk.PhotoImage(Image.open(path + "GUI\\Export.png"))
		self.PH_SETS     = ImageTk.PhotoImage(Image.open(path + "GUI\\Settings.png"))
		self.PH_EXIT     = ImageTk.PhotoImage(Image.open(path + "GUI\\Exit.png"))
		self.PH_REF      = ImageTk.PhotoImage(Image.open(path + "GUI\\Refresh.png"))
		self.PH_BCK      = ImageTk.PhotoImage(Image.open(path + "GUI\\Back.png"))
		self.PH_BOOK     = ImageTk.PhotoImage(Image.open(path + "GUI\\Book.png"))
		self.PH_INF      = ImageTk.PhotoImage(Image.open(path + "GUI\\Logo.png"))
		self.PH_EXC      = ImageTk.PhotoImage(Image.open(path + "GUI\\Excel.png"))
		self.PH_HELP     = ImageTk.PhotoImage(Image.open(path + "GUI\\Help.png"))
                self.PH_EMP_A    = ImageTk.PhotoImage(Image.open(path + "GUI\\Empty_all.png"))
                self.PH_EMP_S    = ImageTk.PhotoImage(Image.open(path + "GUI\\Empty_search.png"))
                self.PH_SHD      = ImageTk.PhotoImage(Image.open(path + "GUI\\Shadow.png"))
		self.PH_DEL      = ImageTk.PhotoImage(Image.open(path + "GUI\\Button01.png"))
		self.PH_EDIT     = ImageTk.PhotoImage(Image.open(path + "GUI\\Button02.png"))
		self.PH_SEE      = ImageTk.PhotoImage(Image.open(path + "GUI\\Button03.png"))
                self.PH_ARR      = ImageTk.PhotoImage(Image.open(path + "GUI\\Arrow.png"))

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

		self.Bar()       # generate upper bar of main window
		self.Body()      # generate body - main part of main window
                self.Stat()      # generate statics bar in bottom

		self.Fill_list() # fill main listbox

	###################################
	# TECHNICAL                       #
	# METHODS                         #
	###################################

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
			self.result_create = self.DB.new_book(self.CLASS, self.NAME, self.SUBJECT, self.AUTHOR, self.PUBLISH)
			if self.result_create: # if ok
				self.close_root2() # close 2-level's window
				self.Fill_list() # refresh main listbox
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
			if not(self.CLASS and self.SUBJECT and self.NAME and self.AUTHOR and self.PUBLISH):
			        # if some entries are empty
				self.Error(u"Введите все данные\nв поля ввода!") # generate window of error

			elif len(self.DB.crt_books(CLASS=self.CLASS, SUBJECT=self.SUBJECT,
                                                   AUTHOR=self.AUTHOR, PUBLISH=self.PUBLISH)[0]) != 0:
                                                   # if there are some books like that

				if not self.ROOT3: # opened 3-level's window?

					self.Fill_list(mode="search", CLASS=self.CLASS, SUBJECT=self.SUBJECT, AUTHOR=self.AUTHOR, PUBLISH=self.PUBLISH)

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
                                                                        text=u"Уже существуют схожие книги в базе\n(в центральном списке)\n\nПродолжать создание?",
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

	def search_books(self):
		# getting data
                self.CLASS   = self.ROOT2.get()["e1"]
                self.SUBJECT = self.ROOT2.get()["e2"]
                self.AUTHOR  = self.ROOT2.get()["e3"]
                self.PUBLISH = self.ROOT2.get()["e4"]

		# convertion for View.Fill_list() -> Database.crt_books()
		if not self.CLASS:   self.CLASS   = None
		if not self.SUBJECT: self.SUBJECT = None
		if not self.AUTHOR:  self.AUTHOR   = None
		if not self.PUBLISH: self.PUBLISH = None

		self.close_root2() # closing 2-level's window
		self.Fill_list(mode="search", CLASS=self.CLASS, SUBJECT=self.SUBJECT, AUTHOR=self.AUTHOR, PUBLISH=self.PUBLISH)

	def edit_book(self):
		# getting data
                if self.ROOT3:
                        self.CLASS   = self.ROOT3.get()["e1"]
                        self.NAME    = self.ROOT3.get()["e2"]
                        self.SUBJECT = self.ROOT3.get()["e3"]
                        self.AUTHOR  = self.ROOT3.get()["e4"]
                        self.PUBLISH = self.ROOT3.get()["e5"]
                else:
                        self.CLASS   = self.ROOT2.get()["e1"]
                        self.NAME    = self.ROOT2.get()["e2"]
                        self.SUBJECT = self.ROOT2.get()["e3"]
                        self.AUTHOR  = self.ROOT2.get()["e4"]
                        self.PUBLISH = self.ROOT2.get()["e5"]

		try:
			if not(self.CLASS and self.SUBJECT and self.NAME and self.AUTHOR and self.PUBLISH): # if some entries are empty
				self.Error(u"Введите все данные\nв поля ввода!") # generate window of error

			elif len(self.DB.crt_books(CLASS=self.CLASS, NAME=self.NAME, SUBJECT=self.SUBJECT,
                                                   AUTHOR=self.AUTHOR, PUBLISH=self.PUBLISH)[0]) == 0:

                                # if data of book is unique

				self.DB.update_class(self.BOOK["ID"], self.CLASS)
				self.DB.update_name(self.BOOK["ID"], self.NAME)
				self.DB.update_subject(self.BOOK["ID"], self.SUBJECT)
				self.DB.update_author(self.BOOK["ID"], self.AUTHOR)
				self.DB.update_publish(self.BOOK["ID"], self.PUBLISH)

				if not(self.ROOT2 and self.ROOT3): # when this is not in-function of viewing book
					self.close_root2() # close 2-level's window
				else:
					self.BOOK = self.DB.one_book(self.BOOK["ID"])
					self.close_root3() # close 3-level's window
					self.ROOT2["pagebook"].view_page(1) # update page of current data

				self.Fill_list() # refresh main listbox
			else:
				self.Error(u"Такая книга уже существует!") # if error (not unique)
		except OperationalError:
			self.Error(u"Соединение с сервером разорвано!\nПроверьте работоспособность вашего\nсервера базы данных.")

	def delete_book(self):
		# deleting book
		try:
			self.DB.delete_book(self.BOOK["ID"])
			self.Fill_all() # refresh main listbox
			self.close_root2() # close 2-level's window

		except OperationalError:
			self.Error(u"Соединение с сервером разорвано!\nПроверьте работоспособность вашего\nсервера базы данных.")

	def get_book(self):
		# getting data from entries
		self.YEAR = self.ROOT3.get()["e1"]
		self.HOW  = self.ROOT3.get()["e2"]
		self.PRC  = self.ROOT3.get()["e3"]

		# checking types
		try:
			self.YEAR = int(self.YEAR)
			self.HOW  = int(self.HOW)
			self.PRC  = float(self.PRC)
		except:
			self.YEAR = 0.1 # special literal for identification error

		# checking data
		if not(self.YEAR and self.HOW and self.PRC): # if some entries are empty
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
				self.DB.new_get(self.BOOK["ID"], self.YEAR, self.HOW, self.PRC) # new record of control db
				self.close_root3() # close 3-level's window
				self.BOOK = self.DB.one_book(self.BOOK["ID"]) # update current Book object
				self.ROOT2["pagebook"].view_page(2) # go to control page of viewing book
				self.Fill_list()
			except OperationalError:
				self.Error(u"Соединение с сервером разорвано!\nПроверьте работоспособность вашего\nсервера базы данных.")

	def off_book(self):
		# getting data from entries
		self.YEAR = self.ROOT3.get()["e1"]
		self.HOW  = self.ROOT3.get()["e2"]

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

                elif self.BOOK["AMOUNT"] - self.HOW < 0:
                        self.Error(u"Нет необходимого числа книг!")

		else: # if ok
			try:
				self.DB.new_off(self.BOOK["ID"], self.YEAR, self.HOW) # new record of control db
				self.close_root3() # close 3-level's window
				self.BOOK = self.DB.one_book(self.BOOK["ID"]) # update current Book object
				self.ROOT2["pagebook"].view_page(2) # go to control page of viewing book
				self.Fill_list()
			except OperationalError:
				self.Error(u"Соединение с сервером разорвано!\nПроверьте работоспособность вашего\nсервера базы данных.")

	def delete_control(self):
		self.OP = self.ROOT2["pagebook"]["current"].get()["listbox"]
		self.OP = self.OP.split(" ")

		try:
			if   self.OP[1] == u"Получено":
                                if self.BOOK["AMOUNT"] - int(self.OP[5]) >= 0:
				        self.DB.delete_get(self.BOOK["ID"], int(self.OP[3]), int(self.OP[5]), float(self.OP[8]))
                                else:
                                        self.Error(u"Нет необходимого числа книг!")
			elif self.OP[1] == u"Выдано":
				self.DB.delete_give(self.BOOK["ID"], int(self.OP[3]), int(self.OP[5]))
			elif self.OP[1] == u"Списано":
				self.DB.delete_off(self.BOOK["ID"], int(self.OP[3]), int(self.OP[5]))
			self.Fill_list() # update main table
			self.BOOK = self.DB.one_book(self.BOOK["ID"]) # update Book object of current book
			self.ROOT2["pagebook"].view_page(2) # update page of control data
		except OperationalError:
			self.Error(u"Соединение с сервером разорвано!\nПроверьте работоспособность вашего\nсервера базы данных.")

        def search(self, event):
                self.searching = self.SEARCH.get()
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

	def export_table(self):
                try:
                        # generate table by criterions
		        self.XL.generate(self.ROOT2.get()["val1"], self.ROOT2.get()["val2"],
                                         self.ROOT2.get()["val3"], self.ROOT2.get()["val4"])
		        self.close_root2() # close 2-level's window
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

	def docs(self):
		os.startfile(self.PATH + "PLG\\Docs\\Main.html")

        def fill_class(self):
                self.text = self.TABLE.PAGEBOOK.current_text.replace(u" кл.", "")
                self.TABLE.PAGEBOOK["current"]["table"].erase()
                self.books = self.DB.crt_books(CLASS=self.text)[0]

                print self.text

                for self.e in self.books:
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

                        self.TABLE.insert_line("current", self.LINE)

	###################################
	# GRAPHICS                        #
	# METHODS                         #
	###################################

	def Error(self, text):
                # form
                self.EROOT = form.Form(title=u" BookStore | Ошибка", height=250, width=500)

                # head of form
		self.EROOT["title"] = tk.Label(self.EROOT.HEAD, text=u"Ошибка", font=(self.FT, 17), bg=self.color_bar, fg="#EFEFEF") # head
		self.EROOT["title"].pack(fill=tk.X)

		self.EROOT["content"] = tk.Label(self.EROOT.BODY, text=text, font=(self.FT, 12), bg=self.color_bg, height=5)
		self.EROOT["content"].pack()

                self.EROOT.start_form(x=250, y=500)

	def Bar(self): # Upper bar of main window
		# BUTTONS OF BAR
                self.HEAD["pady"] = 5
                self.HEAD["padx"] = 3

		#self.INFIN  = tk.Label(self.HEAD, image=self.PH_INF, bd=0, bg=self.color_bar, height=40)
		#self.INFIN.pack(side="left")

		self.BHEAD2 = tk.Button(self.HEAD, image=self.PH_SEARCH, bg=self.color_bar, bd=0, command=self.Search_list,
                                        activebackground=self.color_high_bar, width=110, anchor="w")
		self.BHEAD2.pack(side="left", padx=4)

                self.BTOGGLE = tk.Button(self.HEAD, image=self.PH_ARR, bg=self.color_bar,
                                         bd=0, activebackground=self.color_bar,
                                         activeforeground="#E8E8E8", command=self.TOGGLE)
                self.BTOGGLE.pack(side="right")

                self.SEARCH_FR = tk.Frame(self.HEAD, bg=self.color_bg, height=38)
                self.SEARCH_FR.pack(fill=tk.X, side="right", expand=1)

                self.SPLIT = tk.Frame(self.SEARCH_FR, bg=self.color_bar, width=20)
                self.SPLIT.pack(side="right", fill=tk.Y)

                self.SEARCH_VAR = tk.StringVar()
                self.SEARCH = tk.Entry(self.SEARCH_FR, bg=self.color_bg, font=(self.FT, 13), relief=tk.FLAT, border=2, textvariable=self.SEARCH_VAR)
                self.SEARCH.pack(fill=tk.X)

	def Body(self): # main part of main window: main listbox and lower bar of statics
		self.FORBACK = False # trigger of inputting button to back

                self.INDEX = 0 # index of the last class in pagebook

		self.TABLE = listbook.Listbook(self.BODY, self.PH_EMP_A, self.PH_EMP_S, self.PH_BOOK) # main table of books
		self.TABLE.pack()

        def Stat(self):
		self.SVAL0 = tk.StringVar()   # statics variable - searching mode
		self.SVAL0.set(u"Все книги ") # default value

		self.SVAL1 = tk.StringVar() # statics variable - how many books
		self.SVAL1.set("0")         # default value

		self.SVAL2 = tk.StringVar() # statics variable - how many instances
		self.SVAL2.set("0")         # default value

		self.SVAL3 = tk.StringVar() # statics variable - how much do books cost
		self.SVAL3.set("0.0")       # default value

		self.VAL0 = tk.Label(self.STAT, textvariable=self.SVAL0, font=(self.FT, 13),
                                     bg=self.color_bar, fg="#EFEFEF")
		self.VAL0.pack(side="left") # label of statics - searching mode

                self.BSEP = tk.Label(self.STAT, image=self.PH_SEP, bg=self.color_bar, width=15)
                self.BSEP.pack(side="left")

		self.STAT1 = tk.Label(self.STAT, text=u"Книг:", font=(self.FT, 12),
                                      bg=self.color_bar, fg="#EFEFEF")
		self.STAT1.pack(side="left")

		self.VAL1 = tk.Label(self.STAT, textvariable=self.SVAL1, font=(self.FT, 12),
                                     bg=self.color_bar, fg="#EFEFEF")
		self.VAL1.pack(side="left") # label of statics - how many books

		self.STAT2 = tk.Label(self.STAT, text=u" Экземпляров:", font=(self.FT, 12),
                                      bg=self.color_bar, fg="#EFEFEF")
		self.STAT2.pack(side="left")

		self.VAL2 = tk.Label(self.STAT, textvariable=self.SVAL2, font=(self.FT, 12),
                                     bg=self.color_bar, fg="#EFEFEF")
		self.VAL2.pack(side="left") # label of statics - how many instances

		self.STAT3 = tk.Label(self.STAT, text=u" Стоимость:", font=(self.FT, 12),
                                      bg=self.color_bar, fg="#EFEFEF")
		self.STAT3.pack(side="left")

		self.VAL3 = tk.Label(self.STAT, textvariable=self.SVAL3, font=(self.FT, 12),
                                     bg=self.color_bar, fg="#EFEFEF")
		self.VAL3.pack(side="left") # label of statics - how much do books cost

		self.BHEADH = tk.Button(self.STAT, image=self.PH_HELP, bg=self.color_bar, bd=0,
                                        activebackground=self.color_high_bar, command=self.docs)
		self.BHEADH.pack(side="right")

		self.BHEADR = tk.Button(self.STAT, image=self.PH_REF, bg=self.color_bar, bd=0, command=self.Fill_list,
                                        activebackground=self.color_high_bar)
		self.BHEADR.pack(side="right")

		self.b_see = tk.Button(self.STAT, image=self.PH_SEE, bd=0, bg=self.color_bar,
                                       command=self.See_book, activebackground=self.color_high_bar) # button of viewing book
		self.b_see.pack(side="right")

		self.b_edit = tk.Button(self.STAT, image=self.PH_EDIT, bd=0, bg=self.color_bar,
                                        command=self.Edit, activebackground=self.color_high_bar) # button of editing book
		self.b_edit.pack(side="right")

		self.b_del = tk.Button(self.STAT, image=self.PH_DEL, bd=0, bg=self.color_bar,
                                       command=self.Delete, activebackground=self.color_high_bar) # button of deleting book
		self.b_del.pack(side="right")

        def Fill_all(self):
                if self.FORBACK:              # if back button is on the bar
			self.BHEAD7.destroy() # destroy this button
			self.FORBACK = False  # toggle trigger

                self.SVAL1.set(str(self.DB.how_all_books()))  # how many books into statics
	        self.SVAL2.set(str(self.DB.how_all_inst()))   # how many instances into statics
		self.SVAL3.set(str(self.DB.cost_all_books())) # how much do books cost into statics
		self.SVAL0.set(u"Все книги")

                if len(self.DB.all_books()) == 0:
                        self.TABLE.go_empty(1)
                        return None

                self.TABLE.create_pagebook()
                self.INDEX = 0

                for self.cl in self.DB.classes():
                        self.TABLE.new_class(self.INDEX, self.cl + u" кл.", func=self.fill_class)
                        self.INDEX += 1

		print self.DB.how_all_books()

                self.TABLE.PAGEBOOK.view_page(self.TABLE.PAGEBOOK.PAGES.keys()[0])

	def Search_list(self, mode="search"): # filling main listbox
                if self.SEARCH.get() == "": return None
                if mode == "all":
                        self.Fill_all()
                else:
                        if not self.FORBACK:
			        self.BHEAD7 = tk.Button(self.STAT, image=self.PH_BCK, bg=self.color_bar, bd=0, command=self.Fill_list,  activebackground=self.color_high_bar) # generate back button
			        self.BHEAD7.pack(side="right")

			        self.FORBACK = True # toggle trigger

			self.SVAL0.set(u"Поиск книг")
                        self.search_string = self.SEARCH.get()
                        self.SEARCH.delete(0, tk.END)

			self.book_list, self.how, self.inst, self.cost = self.DB.search_report(self.search_string) # list of Book objects
        		self.SVAL1.set(str(self.how))  # how many books
	        	self.SVAL2.set(str(self.inst)) # how many instances
		        self.SVAL3.set(str(self.cost)) # how many instances

                        if self.how == 0:
                                self.TABLE.go_empty(2)
                                return None

                        self.TABLE.create_table()

                        for self.e in self.book_list:
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

                                self.TABLE.insert(self.LINE)

	def Fill_list(self, mode="all", CLASS=None, SUBJECT=None, AUTHOR=None, PUBLISH=None): # filling main listbox
                if mode == "all":
                        self.Fill_all()
                else:
                        if not self.FORBACK:
			        self.BHEAD7 = tk.Button(self.STAT, image=self.PH_BCK, bg=self.color_bar, bd=0, command=self.Fill_list,  activebackground=self.color_high_bar) # generate back button
			        self.BHEAD7.pack(side="right")

			        self.FORBACK = True # toggle trigger

			self.SVAL0.set(u"Поиск книг")

			self.book_list, self.how, self.inst, self.cost = self.DB.crt_books(CLASS=CLASS, SUBJECT=SUBJECT,
                                                                                           AUTHOR=AUTHOR, PUBLISH=PUBLISH) # list of Book objects
        		self.SVAL1.set(str(self.how))  # how many books
	        	self.SVAL2.set(str(self.inst)) # how many instances
		        self.SVAL3.set(str(self.cost)) # how many instances

                        if self.how == 0:
                                self.TABLE.go_empty(2)
                                return None

                        self.TABLE.create_table()

                        for self.e in self.book_list:
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

                                self.TABLE.insert(self.LINE)

	def New(self):
                try:
                        self.DB.how_all_books()
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

			# labels of entries in fo
			# rm
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

	def Search(self):
                try:
                        self.DB.how_all_books()
                except OperationalError:
                        self.Error(u"Соединение с сервером разорвано!\nПроверьте работоспособность вашего\nсервера базы данных.")
                        return None

		if not self.ROOT2: # opened 2-level's window?
			# form
                        self.ROOT2 = form.Form(title=u" BookStore | Поиск книг", height=350, width=550, protocol=self.close_root2)

                        # head of form
			self.ROOT2["title"] = tk.Label(self.ROOT2.HEAD, text=u"Поиск",
                                                       font=(self.FT, 17), bg=self.color_bar, fg="#EFEFEF")
			self.ROOT2["title"].pack(fill=tk.X)

		        # info
			self.ROOT2["info"] = tk.Label(self.ROOT2.BODY, text=u"Введите критерии поиска:",
                                                      font=(self.FT, 12), bg=self.color_bg, height=2)
			self.ROOT2["info"].grid(row=0, column=0, columnspan=2)

			# labels of entries
			self.ROOT2["l1"] = tk.Label(self.ROOT2.BODY, text=u"Класс:",
                                                    font=(self.FT, 13), bg=self.color_bg, anchor="w", width=20)
                        self.ROOT2["l1"].grid(row=1, column=0)

			self.ROOT2["l2"] = tk.Label(self.ROOT2.BODY, text=u"Предмет:",
                                                    font=(self.FT, 13), bg=self.color_bg, anchor="w", width=20)
                        self.ROOT2["l2"].grid(row=2, column=0)

			self.ROOT2["l3"] = tk.Label(self.ROOT2.BODY, text=u"Автор:",
                                                    font=(self.FT, 13), bg=self.color_bg, anchor="w", width=20)
                        self.ROOT2["l3"].grid(row=3, column=0)

			self.ROOT2["l4"] = tk.Label(self.ROOT2.BODY, text=u"Издательство:",
                                                    font=(self.FT, 13), bg=self.color_bg, anchor="w", width=20)
                        self.ROOT2["l4"].grid(row=4, column=0)

			# entries
			self.ROOT2["e1"] = tk.Entry(self.ROOT2.BODY, width=31,
                                                    font=(self.FT, 13), bd=1)
                        self.ROOT2["e1"].grid(row=1, column=1)

			self.ROOT2["e2"] = ttk.Combobox(self.ROOT2.BODY, width=32,
                                                        font=(self.FT, 12), values=self.DB.subjects())
                        self.ROOT2["e2"].grid(row=2, column=1)

			self.ROOT2["e3"] = ttk.Combobox(self.ROOT2.BODY, width=32,
                                                        font=(self.FT, 12), values=self.DB.authors())
                        self.ROOT2["e3"].grid(row=3, column=1)

			self.ROOT2["e4"] = ttk.Combobox(self.ROOT2.BODY, width=32,
                                                        font=(self.FT, 12), values=self.DB.publishes())
                        self.ROOT2["e4"].grid(row=4, column=1)

			# empty separator and button
			self.ROOT2["sep"] = tk.Label(self.ROOT2.BODY, text="-", foreground=self.color_bg,
                                                     bg=self.color_bg, height=2)
                        self.ROOT2["sep"].grid(row=5, column=0)

			self.ROOT2["submit"] = tk.Button(self.ROOT2.BODY, image=self.BH_SEARCH,
                                                         width=200, bg=self.color_bg, command=self.search_books,
                                                         bd=0, activebackground=self.color_bg)
                        self.ROOT2["submit"].grid(row=6, column=0, sticky="w")

                        self.ROOT2["cancel"] = tk.Button(self.ROOT2.BODY, image=self.BH_CANCEL,
                                                         width=200, bg=self.color_bg, command=self.close_root2,
                                                         bd=0, activebackground=self.color_bg)
                        self.ROOT2["cancel"].grid(row=6, column=1, sticky="e")

                        self.ROOT2.start_form()

	def Edit_page(self, root):
                # head of form
		root["title"] = tk.Label(root.HEAD, text=u"Редактирование",
                                              font=(self.FT, 17), bg=self.color_bar, fg="#EFEFEF")
		root["title"].pack(fill=tk.X)

		# labels of entries
		root["l1"] = tk.Label(root.BODY, text=u"Класс:",
                                      font=(self.FT, 13), bg=self.color_bg, anchor="w", width=20)
                root["l1"].grid(row=0, column=0)

		root["l2"] = tk.Label(root.BODY, text=u"Наименование:",
                                      font=(self.FT, 13), bg=self.color_bg, anchor="w", width=20)
                root["l2"].grid(row=1, column=0)

		root["l3"] = tk.Label(root.BODY, text=u"Предмет:",
                                      font=(self.FT, 13), bg=self.color_bg, anchor="w", width=20)
                root["l3"].grid(row=2, column=0)

		root["l4"] = tk.Label(root.BODY, text=u"Автор:",
                                      font=(self.FT, 13), bg=self.color_bg, anchor="w", width=20)
                root["l4"].grid(row=3, column=0)

		root["l5"] = tk.Label(root.BODY, text=u"Издательство:",
                                      font=(self.FT, 13), bg=self.color_bg, anchor="w", width=20)
                root["l5"].grid(row=4, column=0)

		# entries
		root["e1"] = tk.Entry(root.BODY, width=31, font=(self.FT, 13), bd=1)
                root["e1"].grid(row=0, column=1)
                root["e1"].insert(tk.END, self.BOOK["CLASS"])

        	root["e2"] = tk.Entry(root.BODY, width=31, font=(self.FT, 13), bd=1)
                root["e2"].grid(row=1, column=1)
                root["e2"].insert(tk.END, self.BOOK["NAME"])

		root["e3"] = ttk.Combobox(root.BODY, width=32,font=(self.FT, 12), values=self.DB.subjects())
                root["e3"].grid(row=2, column=1)
                root["e3"].insert(tk.END, self.BOOK["SUBJECT"])

		root["e4"] = ttk.Combobox(root.BODY, width=32, font=(self.FT, 12), values=self.DB.authors())
                root["e4"].grid(row=3, column=1)
                root["e4"].insert(tk.END, self.BOOK["AUTHOR"])

	        root["e5"] = ttk.Combobox(root.BODY, width=32, font=(self.FT, 12), values=self.DB.publishes())
                root["e5"].grid(row=4, column=1)
                root["e5"].insert(tk.END, self.BOOK["PUBLISH"])

		# empty separator and button
		root["sep"] = tk.Label(root.BODY, text="-", foreground=self.color_bg,
                                             bg=self.color_bg, height=3)
                root["sep"].grid(row=5, column=0)

		root["submit"] = tk.Button(root.BODY, image=self.BH_SAVE,
                                                 bg=self.color_bg, command=self.edit_book, width=170,
                                                 bd=0, activebackground=self.color_bg)
                root["submit"].grid(row=6, column=0, sticky="w")

		root["cancel"] = tk.Button(root.BODY, image=self.BH_CANCEL,
                                                 bg=self.color_bg, command=self.close_root2, width=170,
                                                 bd=0, activebackground=self.color_bg)
                root["cancel"].grid(row=6, column=1, sticky="e")

                root.start_form()

	def Edit(self):
                try:
                        self.DB.how_all_books()
                except OperationalError:
                        self.Error(u"Соединение с сервером разорвано!\nПроверьте работоспособность вашего\nсервера базы данных.")
                        return None

                print self.ROOT2

		if not self.ROOT2: # opened 2-level's window?
			try:                                                    # handler
				self.BOOK = self.TABLE.get()                    # of string-lines
				self.BOOK = self.BOOK.split(" | ")              # handle if string
				self.BOOK = self.DB.one_book(int(self.BOOK[0])) # is empty
			except:
				self.BOOK = None                                # handling
				self.ROOT2 = None

			if self.BOOK != None:
				# form
                                self.ROOT2 = form.Form(title=u" BookStore | Редактирование",
                                                       height=350, width=550, protocol=self.close_root2)

				self.Edit_page(self.ROOT2) # start page of editing book

	def Delete_page(self, root):
                # head of form
		root["title"] = tk.Label(root.HEAD, text=u"Удаление",
                                              font=(self.FT, 17), bg=self.color_bar, fg="#EFEFEF")
		root["title"].pack(fill=tk.X)

		# info
		root["info"] = tk.Label(root.BODY, text=u"Вы уверены, что хотите удалить книгу:", font=(self.FT, 13), bg=self.color_bg)
		root["info"].pack()

		# info of book
		root["infobook"] = tk.Label(root.BODY,
                                            text=self.BOOK["CLASS"]+", "+self.BOOK["SUBJECT"]+"\n"+self.BOOK["NAME"]+"\n"+self.BOOK["AUTHOR"]+", "+self.BOOK["PUBLISH"],
                                            font=(self.FT, 12), bg=self.color_bg, height=4)
		root["infobook"].pack()

		# button and empty separator
		root["sep"] = tk.Label(root.BODY, text="-", foreground=self.color_bg,
                                             bg=self.color_bg, height=3)
                root["sep"].pack()

		root["submit"] = tk.Button(root.BODY, image=self.BH_DELETE,
                                                 bg=self.color_bg, command=self.delete_book, width=210,
                                                 bd=0, activebackground=self.color_bg)
                root["submit"].pack(side="left")

		root["cancel"] = tk.Button(root.BODY, image=self.BH_CANCEL,
                                                 bg=self.color_bg, command=self.close_root2, width=210,
                                                 bd=0, activebackground=self.color_bg)
                root["cancel"].pack(side="right")

                root.start_form()

	def Delete(self):
                try:
                        self.DB.how_all_books()
                except OperationalError:
                        self.Error(u"Соединение с сервером разорвано!\nПроверьте работоспособность вашего\nсервера базы данных.")
                        return None

		if not self.ROOT2: # opened 2-level's window?
			try:                                                    # handler
				self.BOOK = self.TABLE.get()                    # of string-lines
				self.BOOK = self.BOOK.split(" | ")              # handle if string
				self.BOOK = self.DB.one_book(int(self.BOOK[0])) # is empty
			except:
				self.BOOK = None                              # handling
				self.ROOT2 = None

			if self.BOOK != None:
				# form
                                self.ROOT2 = form.Form(title=u" BookStore | Удаление",
                                                       height=350, width=550, protocol=self.close_root2)

				self.Delete_page(self.ROOT2) # start page of editing book

	def Current(self):
                self.ROOT2["pagebook"]["current"].clear()

		# help-labels of book's table
		self.ROOT2["pagebook"]["current"]["l1"] = tk.Label(self.ROOT2["pagebook"]["current"].BODY,
                                                                   text=u"Индекс:", font=(self.FT, 13),
                                                                   bg=self.color_bg, anchor="w", width=20)
		self.ROOT2["pagebook"]["current"]["l2"] = tk.Label(self.ROOT2["pagebook"]["current"].BODY,
                                                                   text=u"Класс:", font=(self.FT, 13),
                                                                   bg=self.color_bg, anchor="w", width=20)
		self.ROOT2["pagebook"]["current"]["l3"] = tk.Label(self.ROOT2["pagebook"]["current"].BODY,
                                                                   text=u"Наименование:", font=(self.FT, 13),
                                                                   bg=self.color_bg, anchor="w", width=20)
		self.ROOT2["pagebook"]["current"]["l4"] = tk.Label(self.ROOT2["pagebook"]["current"].BODY,
                                                                   text=u"Предмет:", font=(self.FT, 13),
                                                                   bg=self.color_bg, anchor="w", width=20)
		self.ROOT2["pagebook"]["current"]["l5"] = tk.Label(self.ROOT2["pagebook"]["current"].BODY,
                                                                   text=u"Автор:", font=(self.FT, 13),
                                                                   bg=self.color_bg, anchor="w", width=20)
		self.ROOT2["pagebook"]["current"]["l6"] = tk.Label(self.ROOT2["pagebook"]["current"].BODY,
                                                                   text=u"Издательство:", font=(self.FT, 13),
                                                                   bg=self.color_bg, anchor="w", width=20)

		self.ROOT2["pagebook"]["current"]["sp"] = tk.Label(self.ROOT2["pagebook"]["current"].BODY,
                                                                   text="-", bg=self.color_bg, fg=self.color_bg)

		self.ROOT2["pagebook"]["current"]["l7"] = tk.Label(self.ROOT2["pagebook"]["current"].BODY,
                                                                   text=u"Всего:", font=(self.FT, 13),
                                                                   bg=self.color_bg, anchor="w", width=20)
		self.ROOT2["pagebook"]["current"]["l8"] = tk.Label(self.ROOT2["pagebook"]["current"].BODY,
                                                                   text=u"Списано:", font=(self.FT, 13),
                                                                   bg=self.color_bg, anchor="w", width=20)
		self.ROOT2["pagebook"]["current"]["l9"] = tk.Label(self.ROOT2["pagebook"]["current"].BODY,
                                                                   text=u"Стоимость:", font=(self.FT, 13),
                                                                   bg=self.color_bg, anchor="w", width=20)

		self.ROOT2["pagebook"]["current"]["l1"].grid(row=0, column=0)
		self.ROOT2["pagebook"]["current"]["l2"].grid(row=1, column=0)
		self.ROOT2["pagebook"]["current"]["l3"].grid(row=2, column=0)
		self.ROOT2["pagebook"]["current"]["l4"].grid(row=3, column=0)
		self.ROOT2["pagebook"]["current"]["l5"].grid(row=4, column=0)
		self.ROOT2["pagebook"]["current"]["l6"].grid(row=5, column=0)
		self.ROOT2["pagebook"]["current"]["sp"].grid(row=6, column=0)
		self.ROOT2["pagebook"]["current"]["l7"].grid(row=7, column=0)
		self.ROOT2["pagebook"]["current"]["l8"].grid(row=8, column=0)
		self.ROOT2["pagebook"]["current"]["l9"].grid(row=9, column=0)

		# info-labels of book's table
		self.ROOT2["pagebook"]["current"]["l11"] = tk.Label(self.ROOT2["pagebook"]["current"].BODY,
                                                                    text=str(self.BOOK["ID"]), font=(self.FT, 13),
                                                                    bg=self.color_bg, anchor="w", width=40)
		self.ROOT2["pagebook"]["current"]["l12"] = tk.Label(self.ROOT2["pagebook"]["current"].BODY,
                                                                    text=self.BOOK["CLASS"], font=(self.FT, 13),
                                                                    bg=self.color_bg, anchor="w", width=40)
		self.ROOT2["pagebook"]["current"]["l13"] = tk.Label(self.ROOT2["pagebook"]["current"].BODY,
                                                                    text=self.BOOK["NAME"], font=(self.FT, 13),
                                                                    bg=self.color_bg, anchor="w", width=40)
		self.ROOT2["pagebook"]["current"]["l14"] = tk.Label(self.ROOT2["pagebook"]["current"].BODY,
                                                                    text=self.BOOK["SUBJECT"], font=(self.FT, 13),
                                                                    bg=self.color_bg, anchor="w", width=40)
		self.ROOT2["pagebook"]["current"]["l15"] = tk.Label(self.ROOT2["pagebook"]["current"].BODY,
                                                                    text=self.BOOK["AUTHOR"], font=(self.FT, 13),
                                                                    bg=self.color_bg, anchor="w", width=40)
		self.ROOT2["pagebook"]["current"]["l16"] = tk.Label(self.ROOT2["pagebook"]["current"].BODY,
                                                                    text=self.BOOK["PUBLISH"], font=(self.FT, 13),
                                                                    bg=self.color_bg, anchor="w", width=40)

		self.ROOT2["pagebook"]["current"]["sp2"] = tk.Label(self.ROOT2["pagebook"]["current"].BODY,
                                                                    text="-", bg=self.color_bg, fg=self.color_bg)

		self.ROOT2["pagebook"]["current"]["l17"] = tk.Label(self.ROOT2["pagebook"]["current"].BODY,
                                                                    text=str(self.BOOK["AMOUNT"]), font=(self.FT, 13),
                                                                    bg=self.color_bg, anchor="w", width=40)
		self.ROOT2["pagebook"]["current"]["l18"] = tk.Label(self.ROOT2["pagebook"]["current"].BODY,
                                                                    text=str(self.BOOK["OFFED"]), font=(self.FT, 13),
                                                                    bg=self.color_bg, anchor="w", width=40)
		self.ROOT2["pagebook"]["current"]["l19"] = tk.Label(self.ROOT2["pagebook"]["current"].BODY,
                                                                    text=str(self.BOOK["COST"]), font=(self.FT, 13),
                                                                    bg=self.color_bg, anchor="w", width=40)

		self.ROOT2["pagebook"]["current"]["l11"].grid(row=0, column=1)
		self.ROOT2["pagebook"]["current"]["l12"].grid(row=1, column=1)
		self.ROOT2["pagebook"]["current"]["l13"].grid(row=2, column=1)
		self.ROOT2["pagebook"]["current"]["l14"].grid(row=3, column=1)
		self.ROOT2["pagebook"]["current"]["l15"].grid(row=4, column=1)
		self.ROOT2["pagebook"]["current"]["l16"].grid(row=5, column=1)
		self.ROOT2["pagebook"]["current"]["sp2"].grid(row=6, column=1)
		self.ROOT2["pagebook"]["current"]["l17"].grid(row=7, column=1)
		self.ROOT2["pagebook"]["current"]["l18"].grid(row=8, column=1)
		self.ROOT2["pagebook"]["current"]["l19"].grid(row=9, column=1)

	def Control(self):
                self.ROOT2["pagebook"]["current"].clear()

                # frame for listbox and scrollbar
		self.ROOT2["pagebook"]["current"]["lf"] = tk.Frame(self.ROOT2["pagebook"]["current"].BODY, bg=self.color_bg)

                # scrollbar of listbox
		self.ROOT2["pagebook"]["current"]["scroll"] = tk.Scrollbar(self.ROOT2["pagebook"]["current"]["lf"])

		# listbox of control data
		self.ROOT2["pagebook"]["current"]["listbox"] = tk.Listbox(self.ROOT2["pagebook"]["current"]["lf"],
                                                                          height=10, bg="#EFEFEF",
                                                                          yscrollcommand=self.ROOT2["pagebook"]["current"]["scroll"].set,
                                                                          selectborderwidth=0, bd=0,
                                                                          font=(self.FT, 12), relief=tk.FLAT,
                                                                          selectforeground="black",
                                                                          selectbackground=self.color_high_bg,
                                                                          activestyle="dotbox")
		self.ROOT2["pagebook"]["current"]["listbox"].pack(fill=tk.BOTH, expand=1, side="left")

		# configuring and packing scrollbar
		self.ROOT2["pagebook"]["current"]["scroll"].config(command=self.ROOT2["pagebook"]["current"]["listbox"].yview)
		self.ROOT2["pagebook"]["current"]["scroll"].pack(fill=tk.Y, side="right")

		# packing frame
		self.ROOT2["pagebook"]["current"]["lf"].pack(fill=tk.BOTH, expand=1, side="top")

		# button and separator
		self.ROOT2["pagebook"]["current"]["b_erase"] = tk.Button(self.ROOT2["pagebook"]["current"].BODY,
                                                                         image=self.BH_ERASE, bg=self.color_bg,
                                                                         bd=0, command=self.delete_control,
                                                                         activebackground=self.color_bg)
		self.ROOT2["pagebook"]["current"]["b_erase"].pack(side="bottom")

		self.ROOT2["pagebook"]["current"]["sep"] = tk.Label(self.ROOT2["pagebook"]["current"].BODY,
                                                                    text="-", bg=self.color_bg, font="Times 15",
                                                                    fg=self.color_bg)
		self.ROOT2["pagebook"]["current"]["sep"].pack(fill=tk.X, side="bottom")

		# inputting data into listbox
		for self.e in self.BOOK.GET:
			self.line = u" Получено в " + str(self.e[0]) + u" году " + str(self.e[1]) + u" экзем. Цена: "\
                                    + str(self.e[2]) + " (" + str(self.e[1]*self.e[2]) + ")"
			self.ROOT2["pagebook"]["current"]["listbox"].insert(tk.END, self.line)

		for self.e in self.BOOK.OFF:
			self.line = u" Списано в " + str(self.e[0]) + u" году " + str(self.e[1]) + u" экзем."
			self.ROOT2["pagebook"]["current"]["listbox"].insert(tk.END, self.line)

	def See_book(self):
                try:
                        self.DB.how_all_books()
                except OperationalError:
                        self.Error(u"Соединение с сервером разорвано!\nПроверьте работоспособность вашего\nсервера базы данных.")
                        return None

		if not self.ROOT2: # opened 2-level's window?
			try:                                                    # handler
				self.BOOK = self.TABLE.get()                    # of string-lines
				self.BOOK = self.BOOK.split(" | ")              # handle if string
				self.BOOK = self.DB.one_book(int(self.BOOK[0])) # is empty
			except:
				self.BOOK = None                                # handling
				self.ROOT2 = None

			if self.BOOK != None:
                                self.ROOT2 = form.Form(title=u" BookStore | Просмотр книги",
                                                       height=450, width=750, protocol=self.close_root2,
                                                       padx=0, pady=0)

                                # head of form
		        	self.ROOT2["title"] = tk.Label(self.ROOT2.HEAD, text=u"Просмотр книги",
                                                               font=(self.FT, 17), bg=self.color_bar, fg="#EFEFEF")
        			self.ROOT2["title"].pack(fill=tk.X)

				self.ROOT2["low"]   = tk.Frame(self.ROOT2.BODY, bg=self.color_bar) # lower bar
				self.ROOT2["low"].pack(side="bottom", fill=tk.X)

                                # pagebook widget
                                self.ROOT2["pagebook"] = page.Pagebook(self.ROOT2.BODY)
                                self.ROOT2["pagebook"].add_page(1, u"Итоговые данные", 100, 30, self.Current)
                                self.ROOT2["pagebook"].add_page(2, u"Контрольные данные", 100, 30, self.Control)
                                self.ROOT2["pagebook"].start_book()

				# lower bar's buttons
				self.ROOT2["blow1"] = tk.Button(self.ROOT2["low"], bg=self.color_bar, text=u"Изменить",
                                                                width=20,
                                                                font=(self.FT, 13), fg="#EFEFEF", bd=0,
                                                                activebackground=self.color_high_bar,
                                                                activeforeground="#EFEFEF", command=self.In_edit)
				self.ROOT2["blow1"].pack(side="left")

				self.ROOT2["blow2"] = tk.Button(self.ROOT2["low"], bg=self.color_bar, text=u"Удалить",
                                                                width=20,
                                                                font=(self.FT, 13), fg="#EFEFEF", bd=0,
                                                                activebackground=self.color_high_bar,
                                                                activeforeground="#EFEFEF", command=self.In_delete)
				self.ROOT2["blow2"].pack(side="left")

				self.ROOT2["blow3"] = tk.Button(self.ROOT2["low"], bg=self.color_bar, text=u"Пополнить",
                                                                width=20,
                                                                font=(self.FT, 13), fg="#EFEFEF", bd=0,
                                                                activebackground=self.color_high_bar,
                                                                activeforeground="#EFEFEF", command=self.Get)
				self.ROOT2["blow3"].pack(side="right")

				self.ROOT2["blow4"] = tk.Button(self.ROOT2["low"], bg=self.color_bar, text=u"Списать",
                                                                width=20,
                                                                font=(self.FT, 13), fg="#EFEFEF", bd=0,
                                                                activebackground=self.color_high_bar,
                                                                activeforeground="#EFEFEF", command=self.Off)
				self.ROOT2["blow4"].pack(side="right")

                                self.ROOT2.start_form(x=450, y=750)
                                self.ROOT2["pagebook"].view_page(1)

	def In_edit(self):
		if not self.ROOT3: # opened 3-level's window
                        # form
			self.ROOT3 = form.Form(title=u" BookStore | Редактирование",
                                               height=350, width=550, protocol=self.close_root3)
                        try:
			        self.Edit_page(self.ROOT3) # start page of editing book
                        except OperationalError:
                                self.Error(u"Соединение с сервером разорвано!\nПроверьте работоспособность вашего\nсервера базы данных.")

	def In_delete(self):
		if not self.ROOT3: # opened 3-level's window
                        # form
			self.ROOT3 = form.Form(title=u" BookStore | Удаление",
                                               height=350, width=550, protocol=self.close_root3)

			self.Delete_page(self.ROOT3) # start page of editing book

	def Get(self):
		if not self.ROOT3: # opened 3-level's window
                        # form
			self.ROOT3 = form.Form(title=u" BookStore | Пополнение",
                                               height=350, width=550, protocol=self.close_root3, pady=70)

			self.ROOT3["title"] = tk.Label(self.ROOT3.HEAD, text=u"Пополнение", font=(self.FT, 17),
                                                       bg=self.color_bar, fg="#EFEFEF") # head
			self.ROOT3["title"].pack(fill=tk.X)

			# help-labels of entries
			self.ROOT3["l1"] = tk.Label(self.ROOT3.BODY, text=u"Год получения:", font=(self.FT, 13),
                                                    bg=self.color_bg, anchor="w", width=20)
			self.ROOT3["l2"] = tk.Label(self.ROOT3.BODY, text=u"Количество:", font=(self.FT, 13),
                                                    bg=self.color_bg, anchor="w", width=20)
			self.ROOT3["l3"] = tk.Label(self.ROOT3.BODY, text=u"Цена одной:", font=(self.FT, 13),
                                                    bg=self.color_bg, anchor="w", width=20)

			self.ROOT3["l1"].grid(row=0, column=0)
			self.ROOT3["l2"].grid(row=1, column=0)
			self.ROOT3["l3"].grid(row=2, column=0)

			# entries
			self.ROOT3["e1"] = tk.Entry(self.ROOT3.BODY, width=31, font=(self.FT, 13), bd=1)
			self.ROOT3["e2"] = tk.Entry(self.ROOT3.BODY, width=31, font=(self.FT, 13), bd=1)
			self.ROOT3["e3"] = tk.Entry(self.ROOT3.BODY, width=31, font=(self.FT, 13), bd=1)

			self.ROOT3["e1"].grid(row=0, column=1)
			self.ROOT3["e2"].grid(row=1, column=1)
			self.ROOT3["e3"].grid(row=2, column=1)

			# button and empty separator
			self.ROOT3["sep"] = tk.Label(self.ROOT3.BODY, text="-", foreground=self.color_bg,
                                                     bg=self.color_bg, height=2)
			self.ROOT3["submit"] = tk.Button(self.ROOT3.BODY, image=self.BH_ADD, bg=self.color_bg,
                                                         command=self.get_book, bd=0,
                                                         activebackground=self.color_bg)

			self.ROOT3["sep"].grid(row=3, column=0, columnspan=2)
			self.ROOT3["submit"].grid(row=4, column=0, columnspan=2)

                        self.ROOT3.start_form()

	def Off(self):
		if not self.ROOT3: # opened 3-level's window
                        # form
			self.ROOT3 = form.Form(title=u" BookStore | Списание",
                                               height=350, width=550, protocol=self.close_root3, pady=70)

			self.ROOT3["title"] = tk.Label(self.ROOT3.HEAD, text=u"Списание", font=(self.FT, 17),
                                                       bg=self.color_bar, fg="#EFEFEF") # head
			self.ROOT3["title"].pack(fill=tk.X)

			# help-labels of entries
			self.ROOT3["l1"] = tk.Label(self.ROOT3.BODY, text=u"Год списания:", font=(self.FT, 13),
                                                    bg=self.color_bg, anchor="w", width=20)
			self.ROOT3["l2"] = tk.Label(self.ROOT3.BODY, text=u"Количество:", font=(self.FT, 13),
                                                    bg=self.color_bg, anchor="w", width=20)

			self.ROOT3["l1"].grid(row=0, column=0)
			self.ROOT3["l2"].grid(row=1, column=0)

			# entries
			self.ROOT3["e1"] = tk.Entry(self.ROOT3.BODY, width=31, font=(self.FT, 13), bd=1)
			self.ROOT3["e2"] = tk.Entry(self.ROOT3.BODY, width=31, font=(self.FT, 13), bd=1)

			self.ROOT3["e1"].grid(row=0, column=1)
			self.ROOT3["e2"].grid(row=1, column=1)

			# button and empty separator
			self.ROOT3["sep"] = tk.Label(self.ROOT3.BODY, text="-", foreground=self.color_bg,
                                                     bg=self.color_bg, height=2)
			self.ROOT3["submit"] = tk.Button(self.ROOT3.BODY, image=self.BH_OFF, bg=self.color_bg,
                                                         command=self.off_book, bd=0,
                                                         activebackground=self.color_bg)

			self.ROOT3["sep"].grid(row=2, column=0, columnspan=2)
			self.ROOT3["submit"].grid(row=3, column=0, columnspan=2)

                        self.ROOT3.start_form()

	def Export(self):
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

	def Settings(self):
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