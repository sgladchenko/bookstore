# coding: utf-8

import Tkinter as tk
import PIL.Image as Image
import PIL.ImageTk as ImageTk
import os, sys, time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from hub import Hub
from xlsx import Excel
from sets import Sets
import data
from page import Pagebook
from form import Form

class Start:
	# enter into role of DB and start working with BookStore

	def __init__(self, path):
                # main TK object
                self.TK = tk.Tk()
                self.TK.protocol("WM_DELETE_WINDOW", self.close)

                # Settings of BookStore
		self.PATH = path # pathname of BookStore
		self.S = Sets(self.PATH + "SET\\") # Sets object of settings

                if self.S["EXC_DIR"] == "": self.S["EXC_DIR"] = self.PATH + "EXC"

                self.PH_LOGO    = ImageTk.PhotoImage(Image.open(self.PATH + "GUI\\Logo.png"))
                self.BH_ENTER   = ImageTk.PhotoImage(Image.open(self.PATH + "GUI\\Buttons\\Enter.png"))
                self.BH_EXIT    = ImageTk.PhotoImage(Image.open(self.PATH + "GUI\\Buttons\\Exit.png"))

                self.form()

                self.TK.mainloop()

        def close(self): # closing application
                self.TK.destroy()
                exit()

        def create_db(self, address, port, username, password, db_name):
                # reading sql-code from file
                self.file_code = open(self.PATH + "STD\\sql\\postgres.sql")
                self.code = self.file_code.read().replace("\n","").split(";")
                self.file_code.close()

                # creating sql-database
                self.engine = create_engine("postgres://%s:%s@%s:%s" % (username, password, address, port))
                self.session = sessionmaker(bind=self.engine)()
                self.session.connection().connection.set_isolation_level(0)

                self.session.execute(self.code[0] % (db_name, username))
                self.session.commit()
                self.session.close()

                del self.code[0]

                # creating sql-tables in database
                self.engine = create_engine("postgres://%s:%s@%s:%s/%s" % (username, password, address, port, db_name))
                self.session = sessionmaker(bind=self.engine)()

                for self.statement in self.code: self.session.execute(self.statement)

                self.session.execute("insert into statics values (0,0,0.0);") # default values for statics
                self.session.commit()
                self.session.close()

        def init(self, path, login=None, pwd=None, address=None, port=None, db_name=None, db="postgresql"):
                # initialization objects of application
                self.DB = data.Database(db, self.PATH, address, port, db_name, login, pwd)
                print self.DB.how_all_books()
                self.ST = Sets(self.PATH + "SET\\")
                self.XL = Excel(self.DB, self.ST["EXC_DIR"])

        def log_in_server(self):
                self.DATA = self.PAGES["current"].get()

                self.username = self.DATA["e_login"]
                self.password = self.DATA["e_pwd"]
                self.address  = self.DATA["e_sock"].split(":")[0]
                self.port     = self.DATA["e_sock"].split(":")[1]
                self.db_name  = self.DATA["e_db"]

                # if all entries has a text

                if not(self.username and self.password and self.address and self.port and self.db_name):
                        self.Error(u"Введите все поля!")
                        return

                if self.PAGES[1]["var_db"].get() == True: # needs to create database
                        try:
                                self.create_db(self.address, self.port, self.username, self.password, self.db_name)
                        except:
                                self.Error(u"Ошибка при создании базы данных!")
                                return
                        else:
			        self.S["USER"]    = self.username
			        self.S["PWD"]     = self.password
			        self.S["SOCK"]    = self.address + ":" + self.port
			        self.S["DB_NAME"] = self.db_name

                # try to initialize Database and others objects

                try:
                        self.init(self.PATH, self.username, self.password, self.address, self.port, self.db_name)
                except:
                        if "password authentication" in sys.exc_info()[1].args[0]:
                                self.Error(u"Неверный логин или пароль!")
                        elif self.address in sys.exc_info()[1].args[0]:
                                self.Error(u"Неверный сокет сервера!")
                        elif self.db_name in sys.exc_info()[1].args[0]:
                                self.Error(u"Неверное имя БД!")
                        else:
                                 self.Error(u"Неизвестный тип ошибки входа:\n" + sys.exc_info()[1].args[0])
                else:
                        self.TK.destroy()
                        self.HB = Hub(self.DB, self.XL, self.ST, self.PATH, "Calibri")

        def log_in_offline(self):
                try:
                        self.init(path=self.PATH, db="sqlite")
                except:
                        self.Error(u"Неизвестный тип ошибки входа:\n" + sys.exc_info()[1].args[0])
                        print sys.exc_info()
                else:
                        self.TK.destroy()
                        self.HB = Hub(self.DB, self.XL, self.ST, self.PATH, "Calibri")

        def log_in(self): # try to login into database
                if self.PAGES.get_index() == 1:
                        self.log_in_server()

                elif self.PAGES.get_index() == 2:
                        self.log_in_offline()

        def docs(self, event):
                os.startfile(self.PATH + "PLG\\Docs\\Main.html")

	def Error(self, text): # error window
                # form
                self.EROOT = Form(title=u" BookStore | Ошибка")

                # head of form
		self.EROOT["title"] = tk.Label(self.EROOT.HEAD, text=u"Ошибка", font=("Calibri", 17), bg="#384556", fg="#EFEFEF") # head
		self.EROOT["title"].pack(fill=tk.X)

		self.EROOT["content"] = tk.Label(self.EROOT.BODY, text=text, font=("Calibri", 12), bg="#E8E8E8", height=5)
		self.EROOT["content"].pack()

                self.EROOT.start_form(x=250, y=500)

        def form(self):
                # configuring window
                self.TK.title(u" BookStore | Вход в систему")
                self.TK.iconbitmap(default=self.PATH + "GUI\\Ico.ico")

                self.TK.geometry("700x500")

                """
                self.TK.minsize(700,500)
                self.TK.maxsize(700,500)
                """

                self.MAIN = tk.Frame(self.TK)
                self.MAIN.pack(fill=tk.BOTH, expand=1)

                # head and widgets
                self.HEAD = tk.Frame(self.MAIN, bg="#384556", padx=10, pady=5)
                self.HEAD.pack(side="top", fill=tk.X)

                self.LOGO = tk.Label(self.HEAD, image=self.PH_LOGO, bg="#384556")
                self.LOGO.pack(side="left")

                self.TITLE = tk.Label(self.HEAD, text=u"Вход в систему  ", font=("Calibri, 17"), fg="#E8E8E8", bg="#384556")
                self.TITLE.pack(side="right")

                # body and widgets
                self.BODY = tk.Frame(self.MAIN, bg="#E8E8E8")
                self.BODY.pack(fill=tk.BOTH, expand=1)

                self.PAGES = Pagebook(self.BODY)
                self.PAGES.add_page(1, u"Сервер", padx=0)
                self.server_page()
                self.PAGES.add_page(2, u"Оффлайн")
                self.offline_page()
                self.PAGES.start_book()

                self.PAGES.view_page(1)

                # bottom bar
                self.BOTTOM = tk.Frame(self.MAIN, bg="#384556", padx=10, pady=4)
                self.BOTTOM.pack(side="bottom", fill=tk.X)

                self.B_HELP = tk.Label(self.BOTTOM, text=u"Помощь", font=("Calibri", 13), fg="#E8E8E8", bg="#384556")
                self.B_HELP.pack(side="bottom")
                self.B_HELP.bind("<ButtonPress>", self.docs)

                # buttons
                self.BUTTS = tk.Frame(self.MAIN, bg="#E8E8E8", padx=30, pady=10)
                self.BUTTS.pack(side="bottom", fill=tk.X)

                self.ENTER = tk.Button(self.BUTTS, image=self.BH_ENTER, bg="#E8E8E8", bd=0, activebackground="#E8E8E8",
                                       command=self.log_in)
                self.ENTER.pack(side="left")

                self.EXIT = tk.Button(self.BUTTS, image=self.BH_EXIT, bg="#E8E8E8", bd=0, activebackground="#E8E8E8",
                                      command=self.close)
                self.EXIT.pack(side="right")

        def server_page(self): # configuring page of server-mode
                self.PAGES[1].BODY["padx"]=0
                self.PAGES[1]["body"] = tk.Frame(self.PAGES[1].BODY, bg="#E8E8E8")

                self.PAGES[1]["info"] = tk.Label(self.PAGES[1]["body"], font=("Calibri", 13), bg="#E8E8E8",
                                                 text=u"Вы можете вести сетевой учет книг на сервере БД PostgreSQL.", height=3)
                self.PAGES[1]["info"].grid(row=0, column=0, columnspan=2)

                self.PAGES[1]["l_login"] = tk.Label(self.PAGES[1]["body"], font=("Calibri", 13), bg="#E8E8E8",
                                                    text=u"Логин пользователя:", width=23, anchor="w")
                self.PAGES[1]["l_pwd"]   = tk.Label(self.PAGES[1]["body"], font=("Calibri", 13), bg="#E8E8E8",
                                                    text=u"Пароль пользователя:", width=23, anchor="w")
                self.PAGES[1]["l_sock"]  = tk.Label(self.PAGES[1]["body"], font=("Calibri", 13), bg="#E8E8E8",
                                                    text=u"Сокет сервера:", width=23, anchor="w")
                self.PAGES[1]["l_db"]    = tk.Label(self.PAGES[1]["body"], font=("Calibri", 13), bg="#E8E8E8",
                                                    text=u"Имя БД на сервере:", width=23, anchor="w")
                self.PAGES[1]["var_db"]  = tk.BooleanVar()
                self.PAGES[1]["ch_db"]   = tk.Checkbutton(self.PAGES[1]["body"], font=("Calibri", 10), bg="#E8E8E8",
                                                          text=u"Создать новую БД с данным именем?", anchor="w",
                                                          onvalue=True, offvalue=False, variable=self.PAGES[1]["var_db"])

                self.PAGES[1]["e_login"] = tk.Entry(self.PAGES[1]["body"], font=("Calibri", 13), bg="#E8E8E8", width=30)
                self.PAGES[1]["e_pwd"]   = tk.Entry(self.PAGES[1]["body"], font=("Calibri", 13), bg="#E8E8E8", width=30, show="•")
                self.PAGES[1]["e_sock"]  = tk.Entry(self.PAGES[1]["body"], font=("Calibri", 13), bg="#E8E8E8", width=30)
                self.PAGES[1]["e_db"]    = tk.Entry(self.PAGES[1]["body"], font=("Calibri", 13), bg="#E8E8E8", width=30)

                self.PAGES[1]["e_login"].insert(tk.END, self.S["USER"])
                self.PAGES[1]["e_pwd"].insert(tk.END, self.S["PWD"])
                self.PAGES[1]["e_sock"].insert(tk.END, self.S["SOCK"])
                self.PAGES[1]["e_db"].insert(tk.END, self.S["DB_NAME"])

                self.PAGES[1]["l_login"].grid(row=1, column=0, pady=3)
                self.PAGES[1]["l_pwd"].grid(row=2, column=0, pady=3)
                self.PAGES[1]["l_sock"].grid(row=3, column=0, pady=3)
                self.PAGES[1]["l_db"].grid(row=4, column=0, pady=3)
                self.PAGES[1]["ch_db"].grid(row=5, column=0, pady=5, columnspan=2)

                self.PAGES[1]["e_login"].grid(row=1, column=1, pady=3)
                self.PAGES[1]["e_pwd"].grid(row=2, column=1, pady=3)
                self.PAGES[1]["e_sock"].grid(row=3, column=1, pady=3)
                self.PAGES[1]["e_db"].grid(row=4, column=1, pady=3)

                self.PAGES[1]["body"].place(x=350, y=100, anchor="center")

        def offline_page(self): # configuring page of offline-mode
                self.PAGES[2]["body"] = tk.Frame(self.PAGES[2].BODY, bg="#E8E8E8")
                self.PAGES[2].BODY["padx"]=10

                self.PAGES[2]["info"] = tk.Label(self.PAGES[2]["body"], font=("Calibri", 13), bg="#E8E8E8",
                                                 text=u"Вы можете вести оффлайн-учет книг на собственном компьютере.\n"
                                                      u"Для этого Вам не нужно подключение к серверу.",
                                                 height=3)
                self.PAGES[2]["info"].grid(row=0, column=0, columnspan=2)

                self.PAGES[2]["body"].place(x=350, y=100, anchor="center")
