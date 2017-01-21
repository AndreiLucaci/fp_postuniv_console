import sqlite3
from operator import attrgetter

from src.models.AirplaneCompany import AirplaneCompany
from src.models.Flight import Flight
from src.models.Destination import Destination
from .Statement import Statement


class DbRepository():
	def __init__(self):
		conn = self.getConn()
		self.loadDestinations(conn)
		self.loadCompanies(conn)
		self.loadFlights(conn, True)

	def getConn(self):
		return sqlite3.connect("db.db3")

	def loadDestinations(self, conn, close=False):
		curr = conn.cursor()
		curr.execute("SELECT * FROM Destinations")
		self.Destinations = [Destination(i[0], i[1]) for i in curr.fetchall()]
		if (close):
			conn.close()

	def loadCompanies(self, conn, close=False):
		curr = conn.cursor()
		curr.execute("SELECT * FROM Companies")
		self.Companies = [AirplaneCompany(i[0], i[1]) for i in curr.fetchall()]
		if (close):
			conn.close()

	def getCompanyById(self, id):
		return [i for i in self.Companies if i.id == id][0]

	def getDestinationById(self, id):
		return [i for i in self.Destinations if i.id == id][0]

	def getFlightById(self, id):
		return [i for i in self.Flights if i.id == id][0]

	def addFlight(self, Company, Destination, price):
		flight = Flight(0, Company, Destination, price)
		self.Flights.append(flight)
		stmt = Statement("INSERT INTO Flights VALUES ($next_id, ?, ?, ?)",
		                 (flight.company.id, flight.destination.id, flight.price))
		self.executeIntoDb(stmt)
		self.reloadFlights()

	def reloadFlights(self):
		conn = self.getConn()
		self.loadFlights(conn, True)

	def executeIntoDb(self, stmt):
		conn = self.getConn()
		curr = conn.cursor()
		curr.execute(stmt.query, stmt.params)
		conn.close()

	def findFlight(self, price):
		return [i for i in self.Flights if i.price <= price]

	def sortFlights(self):
		return self.Flights[:].sort(lambda x: x.price)

	def averageCompany(self):
		companies = {}
		for i in self.Flights:
			if (i.company not in companies):
				companies[i.company] = []
			companies[i.company].append(i.price)
		return [(i, sum(companies[i]) / float(len(companies[i]))) for i in companies]

	def lowCostFlight(self):
		destinations = {}
		for i in self.Flights:
			if (i.destination not in destinations):
				destinations[i.destination] = []
			destinations[i.destination].append(i)
		return [min(destinations[i], key=attrgetter('price')) for i in destinations]

	def removeFlights(self, destinationId):
		flights = [i for i in self.Flights if i.destination.id == destinationId]
		for i in flights:
			self.Flights.remove(i)
		stmt = Statement('DELETE FROM Flights WHERE id in (' + ','.join(['?' for i in flights]) + ')', tuple(flights))
		self.executeIntoDb(stmt)
		self.reloadFlights()

	def loadFlights(self, conn, close=False):
		curr = conn.cursor()
		curr.execute("SELECT * from Flights")
		self.Flights = [Flight(i[0], self.getCompanyById(i[1]), self.getDestinationById(i[2]), i[3]) for i in
		                curr.fetchall()]
		if (close):
			conn.close()
