# coding: utf-8

import xlsxwriter as xls
import os, datetime

class Excel:
	# generating xlsx-files of tables

	def __init__(self, db, path):
		self.DB = db # Database object
		self.PATH = path

	def generate(self, main=True, ctrl=True, class_report=True, publish_report=True):
		self.NM = self.time_name()      # generate name of file
		self.WB = xls.Workbook(self.PATH + "\\" + self.NM) # generate Workbook object of xlsx-file

		self.HEAD_FORMAT = self.WB.add_format()    # format of table's head
		self.HEAD_FORMAT.set_bg_color("#DFE6E0")   # background
		self.HEAD_FORMAT.set_border(2)             # border width
		self.HEAD_FORMAT.set_font_size(8)          # size of text
		self.HEAD_FORMAT.set_font_name("Calibri")  # font of text
		self.HEAD_FORMAT.set_align("center")       # align of text
		self.HEAD_FORMAT.set_border_color("black") # border color
		self.HEAD_FORMAT.set_align("vcenter")      # vertical align

		self.BODY_FORMAT = self.WB.add_format()    # format of main data in table
		self.BODY_FORMAT.set_bg_color("#F2F2F2")   # background
		self.BODY_FORMAT.set_border(2)             # size of text
		self.BODY_FORMAT.set_font_size(8)          # size of text
		self.BODY_FORMAT.set_font_name("Calibri")  # font of text
		self.BODY_FORMAT.set_align("center")       # align of text
		self.BODY_FORMAT.set_border_color("black") # border color

		self.CTRL_FORMAT = self.WB.add_format()    # format of main data in table
		self.CTRL_FORMAT.set_bg_color("#E1E1E1")   # background
		self.CTRL_FORMAT.set_border(2)             # size of text
		self.CTRL_FORMAT.set_font_size(8)          # size of text
		self.CTRL_FORMAT.set_font_name("Calibri")  # font of text
		self.CTRL_FORMAT.set_align("center")       # align of text
		self.CTRL_FORMAT.set_border_color("black") # border color

		self.GET_YEARS = self.DB.years("get") # years of gettings
		self.OFF_YEARS = self.DB.years("off") # years of offings

		if main:
			self.main_sheet() # main sheet of xlsx-file

		if ctrl and self.GET_YEARS: # create control sheet?
			self.ctrl_sheet()

		if class_report:   # create report by classes and subjects?
			self.class_report_sheet()

		if publish_report: # create report by publish?
			self.publish_report_sheet()

		self.WB.close() # close xlsx-file
		os.startfile(self.PATH + "\\" + self.NM) # start this table

	def main_sheet(self):
		self.ROW = 0 # row
		self.COL = 0 # column

		self.Main_sheet = self.WB.add_worksheet(u"Главная") # new sheet of data in xlsx-file

		# tuple of table's header
		self.HEAD = (u"Класс", u"Предмет", u"Наименование", u"Автор", u"Издательство", u"Экземпляров", u"Списано", u"Стоимость")

		self.Main_sheet.set_column(0, 7, 15)

		# write header of table
		for self.h in self.HEAD:
			self.Main_sheet.merge_range(self.ROW, self.COL, self.ROW+1, self.COL, self.h, self.HEAD_FORMAT)
			self.COL += 1

		self.COL = 0 # column
		self.ROW = 2 # row

		for self.classname in self.DB.classes(): # for each class
                        self.inc, self.amount, self.off, self.cost = self.DB.class_report(self.classname)

			for self.book in self.DB.crt_books(CLASS=self.classname)[0]: # for each book in class
				self.LINE = ( # line of book
					self.book["CLASS"],
					self.book["SUBJECT"],
					self.book["NAME"],
					self.book["AUTHOR"],
					self.book["PUBLISH"],
					self.book["AMOUNT"],
					self.book["OFFED"],
					self.book["COST"]
				)
				self.Main_sheet.write_row(self.ROW, self.COL, self.LINE, self.BODY_FORMAT)
				self.ROW += 1

			self.LINE = (self.amount, self.off, self.cost) # control line for class
			self.Main_sheet.write(self.ROW, self.COL, self.inc, self.CTRL_FORMAT)
			self.Main_sheet.write_row(self.ROW, self.COL+5, self.LINE, self.CTRL_FORMAT)
			self.ROW += 2

	def ctrl_sheet(self):
		self.ROW = 0 # row
		self.COL = 0 # column

		self.Control_sheet = self.WB.add_worksheet(u"Контрольная") # new sheet

		if not self.OFF_YEARS: self.OFF_YEARS = self.GET_YEARS

		self.Control_sheet.set_column(0, 4, 15)

		# tuple of table's header
		self.HEAD = (u"Класс", u"Предмет", u"Наименование", u"Автор", u"Издательство")
		self.CTRL = ((u"Получено", self.GET_YEARS), (u"Списано", self.OFF_YEARS))

		# write header of table
		for self.h in self.HEAD:
			self.Control_sheet.merge_range(self.ROW, self.COL, self.ROW+1, self.COL, self.h, self.HEAD_FORMAT)
			self.COL += 1

		for self.header, self.years in self.CTRL: # write 2'st part of header with years
                        if len(self.years) == 1:
                                self.Control_sheet.write(self.ROW, self.COL, self.header, self.HEAD_FORMAT)
                                self.Control_sheet.write(self.ROW+1, self.COL, self.years[0], self.HEAD_FORMAT)
                                self.COL += 1
                                continue
                        if len(self.years) == 0:
                                continue

			self.Control_sheet.merge_range(self.ROW, self.COL, self.ROW, self.COL+len(self.years)-1, self.header, self.HEAD_FORMAT)
			self.Control_sheet.write_row(self.ROW+1, self.COL, self.years, self.HEAD_FORMAT)

			self.COL += len(self.years)

		self.COL = 0 # column
		self.ROW = 2 # row

		for self.classname in self.DB.classes(): # for each class
			for self.book in self.DB.crt_fullbooks(CLASS=self.classname)[0]: # for each book in class
				self.LINE = [ # line of book
					self.book["CLASS"],
					self.book["SUBJECT"],
					self.book["NAME"],
					self.book["AUTHOR"],
					self.book["PUBLISH"],
				]

				for self.gyear in self.GET_YEARS: # gettings by years
					self.LINE.append(self.book("AMOUNT_YEAR", self.gyear))

				for self.oyear in self.OFF_YEARS: # offings by years
					self.LINE.append(self.book("OFFED_YEAR", self.oyear))

				self.Control_sheet.write_row(self.ROW, self.COL, self.LINE, self.BODY_FORMAT)
				self.ROW += 1

			self.ROW += 1

	def class_report_sheet(self):
		self.ROW = 0 # row
		self.COL = 0 # column

		self.Classes_sheet = self.WB.add_worksheet(u"Сводка (предметы)") # new sheet

		# tuple of table's header
		self.HEAD = (u"Класс", u"Предмет", u"Количество", u"Экземпляров", u"Списано", u"Стоимость")

		self.Classes_sheet.set_column(0, 5, 15)

		# write header of table
		for self.h in self.HEAD:
			self.Classes_sheet.merge_range(self.ROW, self.COL, self.ROW+1, self.COL, self.h, self.HEAD_FORMAT)
			self.COL += 1

		self.COL = 0 # column
		self.ROW = 2 # row

		for self.pair in self.DB.class_subject():
			self.LINE = [self.pair[0], self.pair[1]] + self.DB.class_subject_report(self.pair)
			self.Classes_sheet.write_row(self.ROW, self.COL, self.LINE, self.BODY_FORMAT)

			self.ROW += 1

	def publish_report_sheet(self):
		self.ROW = 0 # row
		self.COL = 0 # column

		self.Publish_sheet = self.WB.add_worksheet(u"Сводка (издательства)") # new sheet

		# tuple of table's header
		self.HEAD = (u"Издательство", u"Количество", u"Экземпляров", u"Списано", u"Стоимость")

		self.Publish_sheet.set_column(0, 4, 15)

		# write header of table
		for self.h in self.HEAD:
			self.Publish_sheet.merge_range(self.ROW, self.COL, self.ROW+1, self.COL, self.h, self.HEAD_FORMAT)
			self.COL += 1

		self.COL = 0 # column
		self.ROW = 2 # row

		for self.p in self.DB.publishes():
			self.LINE = [self.p] + self.DB.publish_report(self.p)
			self.Publish_sheet.write_row(self.ROW, self.COL, self.LINE, self.BODY_FORMAT)

			self.ROW += 1

	def time_name(self):
		self.d = datetime.datetime.today()
		self.time = self.d.strftime("%y-%m-%d %H-%M-%S")
		self.time = self.time + ".xlsx"

		return self.time




