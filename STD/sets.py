# coding: utf-8

class Sets:
	# using and editing settings of bookstore

	def __init__(self, path):
		self.PATH = path # pathname of files with settings (.conf)

		# data dictionary
		self.DATA = {"SOCK":None, "USER":None, "EXC_DIR":None, "PWD":None, "DB_NAME":None}

		# initialization
		for self.e in self.DATA.keys():
			self.DATA[self.e] = self.get_file(self.e)

	def __getitem__(self, key):
		return self.DATA[key]

	def __setitem__(self, key, value):
		self.set_file(key, value) # upadte file

	def set_file(self, mode, value):
		if mode == "SOCK": # default address of db-host
			# write new version of socket
                        print self.PATH + "socket.conf"
			self.FILE = open(self.PATH + "socket.conf", "w")
			self.FILE.write(value)
			self.FILE.close()

		elif mode == "USER":
			# write file with default username
			self.FILE = open(self.PATH + "user.conf", "w")
			self.FILE.write(value)
			self.FILE.close()

		elif mode == "EXC_DIR":
			# write file with default pathname of xlsx-files
			self.FILE = open(self.PATH + "exc_dir.conf", "w")
			self.FILE.write(value)
			self.FILE.close()

		elif mode == "PWD":
			# write file with default password of db
			self.FILE = open(self.PATH + "pwd.conf", "w")
			self.FILE.write(value)
			self.FILE.close()

		elif mode == "DB_NAME":
			# write file with default name of db
			self.FILE = open(self.PATH + "dbname.conf", "w")
			self.FILE.write(value)
			self.FILE.close()

		if mode in self.DATA.keys(): # update interpreting of class
			self.DATA[mode] = value

	def get_file(self, mode):
		if mode == "SOCK": # default address of db-host
			# reading file with default socket
			self.FILE = open(self.PATH + "socket.conf")
			self.TEMP = self.FILE.read()
			self.FILE.close()

		elif mode == "USER":
			# reading file with default user
			self.FILE = open(self.PATH + "user.conf")
			self.TEMP = self.FILE.read() # username
			self.FILE.close()

		elif mode == "EXC_DIR":
			# reading file with default path of generating xlsx-files
			self.FILE = open(self.PATH + "exc_dir.conf")
			self.TEMP = self.FILE.read() # pathname
			self.FILE.close()

		elif mode == "PWD":
			# reading file with default path of generating xlsx-files
			self.FILE = open(self.PATH + "pwd.conf")
			self.TEMP = self.FILE.read() # password
			self.FILE.close()

		elif mode == "DB_NAME":
			# reading file with default path of generating xlsx-files
			self.FILE = open(self.PATH + "dbname.conf")
			self.TEMP = self.FILE.read() # name of db
			self.FILE.close()

		else:
			self.TEMP = None # if an error

		return self.TEMP




