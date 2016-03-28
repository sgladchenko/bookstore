# coding: utf-8

import Tkinter as tk
import ttk
import empty, page

import PIL.ImageTk as ImageTk
import PIL.Image as Image

class Area:
        # this is the class of widget of action-panels

        def __init__(self, path, parent, root, actions, bg="#E8E8E8", bg_panel="#384556"):

                ######################################
                # PART OF SCROLLING AREA FOR PANELS  #
                ######################################

		self.GFRAME = tk.Frame(parent, bg=bg, bd=0)
		self.CANVAS = tk.Canvas(self.GFRAME, bg=bg)
		self.FRAME  = tk.Frame(self.CANVAS, bg=bg, bd=0)

		self.SCROLL = tk.Scrollbar(self.GFRAME, orient="vertical", command=self.CANVAS.yview) # scrollbar
		self.CANVAS.configure(yscrollcommand=self.SCROLL.set)                                 # configuring scrollbar for canvas

		self.SCROLL.pack(side="right", fill=tk.Y)                        # packing scrollbar
		self.CANVAS.pack(side="left", fill=tk.BOTH, expand=1)            # packing
		self.CANVAS.create_window(0,0, window=self.FRAME, anchor='nw') # insert content to canvas
		self.FRAME.bind("<Configure>", self.conf) # resizing scrollregion after resizing main frame of widgets

                self.CANVAS["border"]=-2

                self.PH_SETS = ImageTk.PhotoImage(Image.open(path + "GUI\\Actions\\Settings.png"))
                self.PH_NEW  = ImageTk.PhotoImage(Image.open(path + "GUI\\Actions\\New.png"))
                self.PH_CONN  = ImageTk.PhotoImage(Image.open(path + "GUI\\Actions\\Connection.png"))
                self.PH_ADD  = ImageTk.PhotoImage(Image.open(path + "GUI\\Actions\\Add.png"))
                self.PH_OFF  = ImageTk.PhotoImage(Image.open(path + "GUI\\Actions\\Off.png"))
                self.PH_EXP  = ImageTk.PhotoImage(Image.open(path + "GUI\\Actions\\Export.png"))

                self.ACTIONS = actions # tuple of actions

                ######################################
                # PANELS OF ACTIONS                  #
                ######################################

                self.ACT1 = tk.Frame(self.FRAME, bg=bg_panel, pady=4)
                self.ACT2 = tk.Frame(self.FRAME, bg=bg_panel, pady=4)
                self.ACT3 = tk.Frame(self.FRAME, bg=bg_panel, pady=4)
                self.ACT4 = tk.Frame(self.FRAME, bg=bg_panel, pady=4)
                self.ACT5 = tk.Frame(self.FRAME, bg=bg_panel, pady=4)
                self.ACT6 = tk.Frame(self.FRAME, bg=bg_panel, pady=4)

                self.HELP = tk.Label(self.FRAME, text=u"Добро пожаловать в BookStore 3!", bg="#E8E8E8",
                                     font=("Calibri", 20), anchor="w")

                self.HELP_L = tk.Label(self.FRAME, text=u"Для перехода между страницами нажмите кнопку стрелки. Для вызова справки нажмите кнопку \"?\".", bg="#E8E8E8",
                                     font=("Calibri", 12), anchor="w")

                #####################################
                #  TEXT-LABELS OF ACTIONS           #
                #####################################

                self.ACT1_TEXT = tk.Label(self.ACT1, text=u"Новая книга", font=("Calibri", 15), bg="#A4A8AF", fg="#E8E8E8")
                self.ACT1_TEXT.pack(side="bottom", fill=tk.X)

                self.ACT2_TEXT = tk.Label(self.ACT2, text=u"Пополнить книги", font=("Calibri", 15), bg="#A4A8AF", fg="#E8E8E8")
                self.ACT2_TEXT.pack(side="bottom", fill=tk.X)

                self.ACT3_TEXT = tk.Label(self.ACT3, text=u"Списать книги", font=("Calibri", 15), bg="#A4A8AF", fg="#E8E8E8")
                self.ACT3_TEXT.pack(side="bottom", fill=tk.X)

                self.ACT4_TEXT = tk.Label(self.ACT4, text=u"Экспорт таблиц", font=("Calibri", 15), bg="#A4A8AF", fg="#E8E8E8")
                self.ACT4_TEXT.pack(side="bottom", fill=tk.X)

                self.ACT5_TEXT = tk.Label(self.ACT5, text=u"Подключение", font=("Calibri", 15), bg="#A4A8AF", fg="#E8E8E8")
                self.ACT5_TEXT.pack(side="bottom", fill=tk.X)

                self.ACT6_TEXT = tk.Label(self.ACT6, text=u"Настройки BookStore", font=("Calibri", 15), bg="#A4A8AF", fg="#E8E8E8")
                self.ACT6_TEXT.pack(side="bottom", fill=tk.X)

                ####################################
                # FRAMES OF ICONS                  #
                ####################################

                self.ACT_F1  = tk.Frame(self.ACT1, bg="#A4A8AF")
                self.ACT_F1.pack(fill=tk.BOTH, expand=1)

                self.ACT_F2  = tk.Frame(self.ACT2, bg="#A4A8AF")
                self.ACT_F2.pack(fill=tk.BOTH, expand=1)

                self.ACT_F3  = tk.Frame(self.ACT3, bg="#A4A8AF")
                self.ACT_F3.pack(fill=tk.BOTH, expand=1)

                self.ACT_F4  = tk.Frame(self.ACT4, bg="#A4A8AF")
                self.ACT_F4.pack(fill=tk.BOTH, expand=1)

                self.ACT_F5  = tk.Frame(self.ACT5, bg="#A4A8AF")
                self.ACT_F5.pack(fill=tk.BOTH, expand=1)

                self.ACT_F6  = tk.Frame(self.ACT6, bg="#A4A8AF")
                self.ACT_F6.pack(fill=tk.BOTH, expand=1)

                #####################################
                # ICONS OF ACTIONS                  #
                #####################################

                self.ACT_L1  = empty.Empty(self.ACT_F1, img=self.PH_NEW, bg="#A4A8AF")
                self.ACT_L1.pack_center()
                self.ACT_L1.LAB.bind("<ButtonPress>", self.ACTIONS[0])

                self.ACT_L2  = empty.Empty(self.ACT_F2, img=self.PH_ADD, bg="#A4A8AF")
                self.ACT_L2.pack_center()
                self.ACT_L2.LAB.bind("<ButtonPress>", self.ACTIONS[1])

                self.ACT_L3  = empty.Empty(self.ACT_F3, img=self.PH_OFF, bg="#A4A8AF")
                self.ACT_L3.pack_center()
                self.ACT_L3.LAB.bind("<ButtonPress>", self.ACTIONS[2])

                self.ACT_L4  = empty.Empty(self.ACT_F4, img=self.PH_EXP, bg="#A4A8AF")
                self.ACT_L4.pack_center()
                self.ACT_L4.LAB.bind("<ButtonPress>", self.ACTIONS[3])

                self.ACT_L5  = empty.Empty(self.ACT_F5, img=self.PH_CONN, bg="#A4A8AF")
                self.ACT_L5.pack_center()
                self.ACT_L5.LAB.bind("<ButtonPress>", self.ACTIONS[4])

                self.ACT_L6  = empty.Empty(self.ACT_F6, img=self.PH_SETS, bg="#A4A8AF")
                self.ACT_L6.pack_center()
                self.ACT_L6.LAB.bind("<ButtonPress>", self.ACTIONS[5])

                self.PARENT = parent
                self.ROOT = root

                self.CANVAS.bind_all("<MouseWheel>", self.wheel)

                self.T = False
                self.GFRAME.bind("<Configure>", self.x_gen)

	def conf(self, event):
		self.CANVAS.configure(scrollregion=self.CANVAS.bbox("all")) # replacing

        def remove(self, event): # delete all panels
                self.ACT1.grid_forget()
                self.ACT2.grid_forget()
                self.ACT3.grid_forget()
                self.ACT4.grid_forget()
                self.ACT5.grid_forget()
                self.ACT6.grid_forget()
                self.HELP.grid_forget()
                self.HELP_L.grid_forget()

        def x_gen(self, event): # resize and replace by x-variable
                self.x = self.ROOT.winfo_width()/1000.0

                self.ACT1["width"] = int(self.x*270)
                self.ACT2["width"] = int(self.x*270)
                self.ACT3["width"] = int(self.x*270)
                self.ACT4["width"] = int(self.x*270)
                self.ACT5["width"] = int(self.x*270)
                self.ACT6["width"] = int(self.x*270)

                self.ACT1["height"] = int(self.x*240)
                self.ACT2["height"] = int(self.x*240)
                self.ACT3["height"] = int(self.x*240)
                self.ACT4["height"] = int(self.x*240)
                self.ACT5["height"] = int(self.x*240)
                self.ACT6["height"] = int(self.x*240)

                if self.T: self.remove(0) # erase panels
                self.T = True

                self.FRAME["padx"] = int(self.x*40)
                self.FRAME["pady"] = int(self.x*20)

                # replace panels
                self.ACT1.grid(row=2, column=0, padx=int(18*self.x), pady=int(self.x*18))
                self.ACT2.grid(row=2, column=1, padx=int(18*self.x), pady=int(self.x*18))
                self.ACT3.grid(row=2, column=2, padx=int(18*self.x), pady=int(self.x*18))

                self.ACT4.grid(row=3, column=0, padx=int(18*self.x), pady=int(self.x*18))
                self.ACT5.grid(row=3, column=1, padx=int(18*self.x), pady=int(self.x*18))
                self.ACT6.grid(row=3, column=2, padx=int(18*self.x), pady=int(self.x*18))

                self.HELP.grid(row=0, column=0, columnspan=3, pady=10*self.x, sticky="w", padx=self.x*18)
                self.HELP_L.grid(row=1, column=0, columnspan=3, sticky="w", padx=self.x*18)

                # forbid sizable
                self.ACT1.pack_propagate(False)
                self.ACT2.pack_propagate(False)
                self.ACT3.pack_propagate(False)
                self.ACT4.pack_propagate(False)
                self.ACT5.pack_propagate(False)
                self.ACT6.pack_propagate(False)

        def wheel(self, event): # mouse wheeling
                self.CANVAS.yview_scroll(-1*(event.delta/120),"units")

        def pack(self):
                self.GFRAME.pack(fill=tk.BOTH, expand=1)


