# coding: utf-8

import Tkinter as tk
import wbase

class Form(wbase.WBase):
        # this is the class of help-windows in BookStore and their forms
        def __init__(self, height=300, width=300, title="BookStore", bg="#E8E8E8", head_bg="#384556",
                     head_fg="#E8E8E8", icon=None, protocol=None, padx=30, pady=30, tk_obj=None):

                wbase.WBase.__init__(self) # initialization WBase

                if tk_obj == None:
                        self.ROOT = tk.Toplevel(bg=bg) # object of toplevel-window of form
                        self.ROOT.title(title) # title of window
                else:
                        self.ROOT = tk_obj

                if protocol: # protocol of deleting window (when window was closed this function will be called)
                        self.ROOT.protocol("WM_DELETE_WINDOW", protocol)

                self.HEAD = tk.Frame(self.ROOT, bg=head_bg) # head of form
                if icon: # if we need icon of form in head
                        self.ICON = tk.Label(self.HEAD, bg=head_bg, image=icon)
                        self.ICON.pack(side="left")

                self.BODY = tk.Frame(self.ROOT, bg=bg, padx=padx, pady=pady) # body of form

        def start_form(self, x=None, y=None): # start packing head and body of form
                self.HEAD.pack(side="top", fill=tk.X)
                self.BODY.pack(fill=tk.BOTH, expand=1)

                self.ROOT.grab_set()

                if not x or not y: return None
                self.ROOT.minsize(y, x) # for/
                self.ROOT.maxsize(y, x) # static size

        def close_form(self): # closing form with closing toplevel window
                self.ROOT.destroy()
                del self.ROOT