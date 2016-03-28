# coding: utf-8

from book import Book, Fullbook
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, mapper, clear_mappers
from sqlalchemy import create_engine, Table, Column, ForeignKey, Integer, Numeric, Float, String, or_
import datetime

# TABLES

Base = declarative_base() # metadata base of table classes

class books(Base):
        __tablename__ = "books"

        id = Column(Integer, primary_key=True)

        classname = Column(String)
        name      = Column(String)

        subject   = Column(String)
        author    = Column(String)
        publish   = Column(String)

        amount    = Column(Integer)
        offed     = Column(Integer)
        cost      = Column(Float)

class gettings(Base):
        __tablename__ = "gettings"

        get_id = Column(Integer, primary_key=True)

        id     = Column(Integer, ForeignKey("books.id"))
        year   = Column(Integer)
        num    = Column(Integer)
        price  = Column(Float)

class offings(Base):
        __tablename__ = "offings"

        off_id = Column(Integer, primary_key=True)

        id     = Column(Integer, ForeignKey("books.id"))
        year   = Column(Integer)
        num    = Column(Integer)

class statics(Base):
        __tablename__ = "statics"

        amount_books  = Column(Integer, primary_key=True)
        amount_copies = Column(Integer)
        amount_cost   = Column(Float)

class Database:
	# working with PostgreSQL DB and SQLite

	def __init__(self, db, path, address=None, port=None, db_name=None, username=None, password=None):
                # create engine object
                self.ENGINE = create_engine(self.create_url(db,path,address,port,db_name,username,password))

                # create session object
                self.MakeSession = sessionmaker(bind=self.ENGINE)
                self.SESSION = self.MakeSession()

                # variable of queries to session
                self.QUERY = None

                # variables of connection
                if address:
                        self.SOCK  = address + ":" + str(port)
                        self.PORT  = port
                        self.DB    = db_name
                        self.LOGIN = username

                # filename of database (for offline)
                self.FILE  = path + "SET\\data.db"
                self.FILE  = self.FILE.replace("BookStoreSET","BookStore\\SET")
                if len(self.FILE) > 40:
                        self.FILE = self.FILE[1:38] + "..."

                # modding url for using (erasing password)
                if address: self.URL = self.URL.replace(":" + password, "")

                # timing of current login
                self.time_login()

        def create_url(self, db, path=None, address=None, port=None, db_name=None, username=None, password=None):
                # create url for connection to database
                if db == "sqlite":
                        self.URL = "sqlite:///" + path.replace("\\", "/") + "SET/data.db"
                        self.URL = self.URL.replace("BookStoreSET", "BookStore/SET")
                else:
                        print username, password
                        self.URL = "postgres://%s:%s@%s:%s/%s" %\
                                   (username, password, address, port, db_name)
                        print self.URL

                return self.URL

        def time_login(self):
	        self.d = datetime.datetime.today()
	        self.TIME = self.d.strftime("%d.%m.%y %H:%M:%S")

	def close(self):
		self.SESSION.commit()
                self.SESSION.close()

	####################################
	# SELECTS FROM                     #
	# DATABASE                         #
	####################################

        def compress(self, books_obj):
                return [books_obj.id,
                        books_obj.classname,
                        books_obj.name,
                        books_obj.subject,
                        books_obj.author,
                        books_obj.publish,
                        books_obj.amount,
                        books_obj.offed,
                        books_obj.cost]

	def all_books(self): # returning list of all books in Book objects (rare usable)
		self.RESP = [] # response

                for self.book in self.SESSION.query(books).order_by(books.classname, books.subject).all():
			self.RESP.append(Book(self.compress(self.book))) # compress Book objects by id

		return self.RESP

	def crt_books(self, CLASS=None, NAME=None, SUBJECT=None, AUTHOR=None, PUBLISH=None):
	        # return Book objects by criterions, their num and num of copies

		self.RESP = [] # response
                self.QUERY = self.SESSION.query(books)
                self.COP = 0
                self.COST = 0.0

                if CLASS:
                        self.QUERY = self.QUERY.filter_by(classname = CLASS)
                if NAME:
                        self.QUERY = self.QUERY.filter_by(name = NAME)
                if SUBJECT:
                        self.QUERY = self.QUERY.filter_by(subject = SUBJECT)
                if AUTHOR:
                        self.QUERY = self.QUERY.filter_by(author = AUTHOR)
                if PUBLISH:
                        self.QUERY = self.QUERY.filter_by(publish = PUBLISH)

		for self.book in self.QUERY.order_by(books.classname, books.subject).all():
			self.RESP.append(Book(self.compress(self.book)))
                        self.COP += self.book.amount
                        self.COST += self.book.cost

		return self.RESP, len(self.RESP), self.COP, self.COST

	def crt_fullbooks(self, CLASS=None, NAME=None, SUBJECT=None, AUTHOR=None, PUBLISH=None):
	        # return Book objects by criterions, their num and num of copies

		self.RESP =  [] # response
                self.QUERY = self.SESSION.query(books)
                self.COP = 0
                self.COST = 0.0

                if CLASS:
                        self.QUERY = self.QUERY.filter_by(classname = CLASS)
                if NAME:
                        self.QUERY = self.QUERY.filter_by(name = NAME)
                if SUBJECT:
                        self.QUERY = self.QUERY.filter_by(subject = SUBJECT)
                if AUTHOR:
                        self.QUERY = self.QUERY.filter_by(author = AUTHOR)
                if PUBLISH:
                        self.QUERY = self.QUERY.filter_by(publish = PUBLISH)

		for self.book in self.QUERY.order_by(books.classname, books.subject).all():
                        # lists of history
                        self.gets = self.SESSION.query(gettings.year, gettings.num, gettings.price).filter_by(id = self.book.id).all()
                        self.offs = self.SESSION.query(offings.year, offings.num).filter_by(id = self.book.id).all()

			self.RESP.append(Fullbook(self.compress(self.book), self.gets, self.offs))
                        self.COP += self.book.amount
                        self.COST += self.book.cost

		return self.RESP, len(self.RESP), self.COP, self.COST

	def how_all_books(self):
		return self.SESSION.query(statics.amount_books).first()[0] # how many all books

	def how_all_inst(self):
                return self.SESSION.query(statics.amount_copies).first()[0]

	def cost_all_books(self):
                return self.SESSION.query(statics.amount_cost).first()[0]

	def subjects(self):
                return [self.x[0] for self.x in self.SESSION.query(books.subject).distinct().all()]

	def classes(self):
                return [self.x[0] for self.x in self.SESSION.query(books.classname).distinct().all()]

	def authors(self):
                return [self.x[0] for self.x in self.SESSION.query(books.author).distinct().all()]

	def publishes(self):
                return [self.x[0] for self.x in self.SESSION.query(books.publish).distinct().all()]

	def years(self, mode):
                if mode == "get":
                        return [self.x[0] for self.x in self.SESSION.query(gettings.year).order_by(gettings.year).distinct().all()]
                else:
                        return [self.x[0] for self.x in self.SESSION.query(offings.year).order_by(offings.year).distinct().all()]

	def class_subject(self):
                return self.SESSION.query(books.classname, books.subject).distinct().all()

        def class_subject_report(self, crt):
                self.RESP = [0,0,0,0.0]
                for self.book in self.SESSION.query(books).filter_by(classname=crt[0],subject=crt[1]).all():
                        self.RESP[0] += 1
                        self.RESP[1] += self.book.amount
                        self.RESP[2] += self.book.offed
                        self.RESP[3] += self.book.cost
                return self.RESP

	def publish_report(self, crt):
                self.RESP = [0,0,0,0.0]
                for self.book in self.SESSION.query(books).filter_by(publish=crt).all():
                        self.RESP[0] += 1
                        self.RESP[1] += self.book.amount
                        self.RESP[2] += self.book.offed
                        self.RESP[3] += self.book.cost
                return self.RESP

	def class_report(self, crt):
                self.RESP = [0,0,0,0.0]
                for self.book in self.SESSION.query(books).filter_by(classname=crt).all():
                        self.RESP[0] += 1
                        self.RESP[1] += self.book.amount
                        self.RESP[2] += self.book.offed
                        self.RESP[3] += self.book.cost
                return tuple(self.RESP)

	def one_book(self, ID):
                self.MAIN = self.compress(self.SESSION.query(books).filter_by(id=ID).first())
                self.GET  = self.SESSION.query(gettings.year, gettings.num, gettings.price).filter_by(id=ID)
                self.OFF  = self.SESSION.query(offings.year, offings.num).filter_by(id=ID)

                return Fullbook(self.MAIN, self.GET, self.OFF)

        def search(self, searching): # searching books by search-strings
                self.RESP = []

                # parsing
                self.SEARCH = searching.replace(",", " ")
                self.SEARCH = self.SEARCH.replace(".", " ")
                self.SEARCH = self.SEARCH.replace("  ", " ")
                self.SEARCH = self.SEARCH.split(" ")

                self.QUERY = self.SESSION.query(books)

                # generating query
                for self.detail in self.SEARCH:
                        self.QUERY = self.QUERY.filter(or_(books.classname.like("%%" + self.detail + "%%"),
                                                           books.name.like("%%" + self.detail + "%%"),
                                                           books.subject.like("%%" + self.detail + "%%"),
                                                           books.author.like("%%" + self.detail + "%%"),
                                                           books.publish.like("%%" + self.detail + "%%")))

                self.QUERY = self.QUERY.order_by(books.classname, books.subject)

                for self.book in self.QUERY.all():
                        self.RESP.append(Book(self.compress(self.book)))

                return self.RESP

        def search_report(self, searching): # searching books by search-strings
                self.RESP = []

                # parsing
                self.SEARCH = searching.replace(",", " ")
                self.SEARCH = self.SEARCH.replace(".", " ")
                self.SEARCH = self.SEARCH.replace("  ", " ")
                self.SEARCH = self.SEARCH.split(" ")

                self.QUERY = self.SESSION.query(books)

                # generating query
                for self.detail in self.SEARCH:
                        self.QUERY = self.QUERY.filter(or_(books.classname.like("%%" + self.detail + "%%"),
                                                           books.name.like("%%" + self.detail + "%%"),
                                                           books.subject.like("%%" + self.detail + "%%"),
                                                           books.author.like("%%" + self.detail + "%%"),
                                                           books.publish.like("%%" + self.detail + "%%")))

                self.QUERY = self.QUERY.order_by(books.classname, books.subject)

                self.COP = 0
                self.COST = 0.0

                for self.book in self.QUERY.all():
                        self.RESP.append(Book(self.compress(self.book)))
                        self.COP += self.book.amount
                        self.COST += self.book.cost

                return self.RESP, len(self.RESP), self.COP, self.COST

	####################################
	# UPDATES OF                       #
	# DATABASE                         #
	####################################

	def update_class(self, ID, CLASS):
		self.SESSION.query(books).filter_by(id=ID).update({"classname":CLASS})
		self.SESSION.commit() # committing database

	def update_name(self, ID, NAME):
		self.SESSION.query(books).filter_by(id=ID).update({"name":NAME})
		self.SESSION.commit() # committing database

	def update_subject(self, ID, SUBJECT):
		self.SESSION.query(books).filter_by(id=ID).update({"subject":SUBJECT})
		self.SESSION.commit() # committing database

	def update_author(self, ID, AUTHOR):
		self.SESSION.query(books).filter_by(id=ID).update({"author":AUTHOR})
		self.SESSION.commit() # committing database

	def update_publish(self, ID, PUBLISH):
		self.SESSION.query(books).filter_by(id=ID).update({"publish":PUBLISH})
		self.SESSION.commit() # committing database

	####################################
	# DELETES FROM                     #
	# DATABASE                         #
	####################################

	def delete_book(self, ID): # delete all info about book with ID
                # delete data of history
		try: self.SESSION.delete(self.SESSION.query(gettings).filter_by(id=ID).first())
		except: pass
		else: self.SESSION.commit()

		try: self.SESSION.delete(self.SESSION.query(offings).filter_by(id=ID).first())
		except: pass
		else: self.SESSION.commit()

                # sync data in statics and history data of this book with ID

                self.SESSION.execute("update statics set amount_books=((select amount_books from statics)-1)")
                self.SESSION.execute("update statics set amount_copies=((select amount_copies from statics)-(select amount from books where id=:id));",
                                     {"id":ID})
                self.SESSION.execute("update statics set amount_cost=((select amount_cost from statics)-(select cost from books where id=:id));",
                                     {"id":ID})

                # delete data of book
                self.SESSION.delete(self.SESSION.query(books).filter_by(id=ID).first())
		self.SESSION.commit() # committing database

	def delete_get(self, ID, YEAR, NUM, PRICE): # delete getting
                # sync data in history with statics data and data in books

                self.SESSION.execute("update statics set amount_copies=((select amount_copies from statics)-:num);",
                                     {"num":NUM})
                self.SESSION.execute("update statics set amount_cost=((select amount_cost from statics)-:cost);",
                                     {"cost":NUM*PRICE})

                self.SESSION.execute("update books set amount=((select amount from books where id=:id)-:num) where id=:id;",
                                     {"id":ID,"num":NUM})
                self.SESSION.execute("update books set cost=((select cost from books where id=:id)-:cost) where id=:id;",
                                     {"id":ID,"cost":NUM*PRICE})

                self.SESSION.delete(self.SESSION.query(gettings).filter_by(id=ID, year=YEAR, num=NUM, price=PRICE).first())
                self.SESSION.commit() # committing database

	def delete_off(self, ID, YEAR, NUM): # delete offing
                # sync data in history with statics data and data in books

                self.SESSION.execute("update statics set amount_copies=((select amount_copies from statics)+:num);",
                                     {"num":NUM})
                self.SESSION.execute("update books set amount=((select amount from books where id=:id)+:num) where id=:id;",
                                     {"id":ID,"num":NUM})
                self.SESSION.execute("update books set offed=((select offed from books where id=:id)-:num) where id=:id;",
                                     {"id":ID,"num":NUM})

                self.SESSION.delete(self.SESSION.query(offings).filter_by(id=ID, year=YEAR, num=NUM).first())
                self.SESSION.commit() # committing database

	####################################
	# INSERTS TO                       #
	# DATABASE                         #
	####################################

	def new_book(self, CLASS, NAME, SUBJECT, AUTHOR, PUBLISH): # new book
		if len(self.SESSION.query(books).filter_by(classname=CLASS,name=NAME,subject=SUBJECT,
                                                           author=AUTHOR,publish=PUBLISH).all()) == 0:
                        # if parameters is unique

                        self.SESSION.add(books(classname=CLASS,name=NAME,
                                              subject=SUBJECT, author=AUTHOR, publish=PUBLISH,
                                              amount=0, offed=0, cost=0.0))

                        # sync data in statics with data in books
                        self.SESSION.execute("update statics set amount_books=((select amount_books from statics)+1);")

		        self.SESSION.commit() # committing database


			return True

		else:
			return False

	def new_get(self, ID, YEAR, NUM, PRICE):
                # sync data of amounts and new values in history
                self.SESSION.execute("update statics set amount_copies=((select amount_copies from statics) + :num);",
                                     {"num":NUM})
                self.SESSION.execute("update statics set amount_cost=((select amount_cost from statics) + :cost);",
                                     {"cost":NUM*PRICE})

                self.SESSION.execute("update books set amount=((select amount from books where id=:id) + :num) where id=:id;",
                                     {"id":ID,"num":NUM})
                self.SESSION.execute("update books set cost=((select cost from books where id=:id) + :cost) where id=:id;",
                                     {"id":ID,"cost":NUM*PRICE})

                # new data in history
                self.SESSION.add(gettings(id=ID, year=YEAR, num=NUM, price=PRICE))
                self.SESSION.commit() # committing database


	def new_off(self, ID, YEAR, NUM):
                # sync data of amounts and new values in history
                self.SESSION.execute("update statics set amount_copies=((select amount_copies from statics) - :num);",
                                     {"num":NUM})

                self.SESSION.execute("update books set amount=((select amount from books where id=:id) - :num) where id=:id;",
                                     {"id":ID,"num":NUM})

                self.SESSION.execute("update books set offed=((select offed from books where id=:id)+:num) where id=:id;",
                                     {"id":ID,"num":NUM})

                self.SESSION.add(offings(id=ID, year=YEAR, num=NUM))
                self.SESSION.commit() # committing database




