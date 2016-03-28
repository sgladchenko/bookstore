# coding: utf-8

import Tkinter as tk

class WBase:
        # this is the base class of Form and Page which have get-data method and vars for widgets in this

        def __init__(self):
                self.WIDGETS = {} # {NAME:WIDGET, NAME:WIDGET}

        def __setitem__(self, name, widget): # for setting widget-objects of form
                self.WIDGETS[name] = widget

        def __getitem__(self, name): # for getting widget-objects in global program
                return self.WIDGETS[name]

        def clear(self): # clear all widgets in page
                for self.widget in self.WIDGETS.values():
                        if "widgetName" in dir(self.widget): # if it's really widget
                                self.widget.destroy()
                self.WIDGETS = {}

        def get(self): # get data from widgets which have get-method (entries, texts, checkboxes etc.)
                self.RESP = {} # response
                for self.widget in self.WIDGETS.keys(): # keys of widgets
                        if "get" in dir(self.WIDGETS[self.widget]): # if widget has get-method
                                if "widgetName" in dir(self.WIDGETS[self.widget]): # if this is really widget
                                        if self.WIDGETS[self.widget].widgetName == "listbox": # for listbox
                                                self.RESP[self.widget] = self.WIDGETS[self.widget].get(tk.ACTIVE)
                                        elif self.WIDGETS[self.widget].widgetName == "text": # for text
                                                self.RESP[self.widget] = self.WIDGETS[self.widget].get(0.0, tk.END)
                                        elif self.WIDGETS[self.widget].widgetName == "pagebook": # for pagebook
                                                pass
                                        else: # for other
                                                self.RESP[self.widget] = self.WIDGETS[self.widget].get()
                                else: # if this is a variable of GUI (StringVar, IntVar etc.)
                                        self.RESP[self.widget] = self.WIDGETS[self.widget].get()
                return self.RESP

