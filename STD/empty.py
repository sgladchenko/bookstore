# coding: utf-8

import Tkinter as tk
import PIL.Image, PIL.ImageTk

class Empty:
        # this is the class of image in Table. This is will be packed in the Table in the center if the Table is empty
        def __init__(self, parent, img, bg="#E8E8E8"):
                self.PAR = parent # variable of parent widget (frame or Tk-object)
                self.LAB = tk.Label(self.PAR, image=img, bd=0, bg=bg) # label of image
                self.PAR.bind("<Configure>", self.conf) # if the parent was configured, label must be replaced too

        def conf(self, event): # replacing widget
                self.LAB.place(anchor="center", x=int(self.PAR.winfo_width()/2), y=int(self.PAR.winfo_height()/2))

        def pack_center(self): # packing widget
                self.conf(0)

        def destroy(self): # destroying widget
                self.LAB.destroy()