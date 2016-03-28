# coding: utf-8

class Book:
        # interpreting one book in program with short information of itself

        def __init__(self, data_list):
                # initialization of main information of book
                self.DATA = data_list

                # allowed keys of Book object
                self.KEYS    = ["ID","CLASS","NAME","SUBJECT","AUTHOR","PUBLISH","AMOUNT","OFFED","COST"]

        def __getitem__(self, key): # display information of book by keys
                if key in self.KEYS: # if key is allowed
                        if key == "ID":      return self.DATA[0]
                        if key == "CLASS":   return self.DATA[1]
                        if key == "NAME":    return self.DATA[2]
                        if key == "SUBJECT": return self.DATA[3]
                        if key == "AUTHOR":  return self.DATA[4]
                        if key == "PUBLISH": return self.DATA[5]
                        if key == "AMOUNT":  return self.DATA[6]
                        if key == "OFFED":   return self.DATA[7]
                        if key == "COST":    return self.DATA[8]
                else:
                        return None

class Fullbook(Book):
	# interpreting of one book with full information (main info and history data)

	def __init__(self, data_list, get_data, off_data):
                Book.__init__(self, data_list) # initialization of main information

                # history of gettings and offings
                self.GET = get_data
                self.OFF = off_data

                # allowed special commands
                self.COM = ["AMOUNT_YEAR","OFFED_YEAR","COST_YEAR"]

	def __call__(self, command, year):
                if command in self.COM:
                        if command == "AMOUNT_YEAR": return self.amount_year(year)
                        if command == "COST_YEAR":   return self.cost_year(year)
                        if command == "OFFED_YEAR":  return self.offed_year(year)
                else:
                        return None

        def amount_year(self, year): # got per year
                self.RESP = 0
                for self.g in self.GET:
                        if self.g[0] == year: self.RESP += self.g[1]
                return self.RESP

        def cost_year(self, year):
                self.RESP = 0.0
                for self.g in self.GET:
                        if self.g[0] == year: self.RESP += self.g[1]*self.g[2]
                return self.RESP

        def offed_year(self, year):
                self.RESP = 0
                for self.g in self.OFF:
                        if self.g[0] == year: self.RESP += self.g[1]
                return self.RESP




