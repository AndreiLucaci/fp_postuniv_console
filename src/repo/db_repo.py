import sqlite3
from operator import attrgetter

from src.models.AirplaneCompany import AirplaneCompany
from src.models.Flight import Flight
from src.models.Destination import Destination
from .Statement import Statement


class DbRepository():
	def __init__(self):
		conn = self.get_conn()
		self.load_destinations(conn)
		self.load_companies(conn)
		self.load_flights(conn, True)

	def get_conn(self):
		return sqlite3.connect("db.db3")

	def load_destinations(self, conn, close=False):
		curr = conn.cursor()
		curr.execute("SELECT * FROM Destinations")
		self.Destinations = [Destination(i[0], i[1]) for i in curr.fetchall()]
		if (close):
			conn.close()

	def load_companies(self, conn, close=False):
		curr = conn.cursor()
		curr.execute("SELECT * FROM Companies")
		self.Companies = [AirplaneCompany(i[0], i[1]) for i in curr.fetchall()]
		if (close):
			conn.close()

	def get_company_by_id(self, id):
		return self.get_first([i for i in self.Companies if i.id == id])

	def get_destination_by_id(self, id):
		return self.get_first([i for i in self.Destinations if i.id == id])

	def get_flight_by_id(self, id):
		return self.get_first([i for i in self.Flights if i.id == id] or [])

	def get_company_by_name(self, name):
		return self.get_first([i for i in self.Companies if i.name == name])

	def get_destination_by_name(self, name):
		return self.get_first([i for i in self.Destinations if i.name == name])

	def get_first(self, lst):
		return next(iter(lst or []), None)

	def add_flight(self, Company, Destination, price):
		flight = Flight(0, Company, Destination, price)
		self.Flights.append(flight)
		stmt = Statement("INSERT INTO Flights VALUES ($next_id, ?, ?, ?)",
		                 (flight.company.id, flight.destination.id, flight.price))
		self.execute_into_db(stmt)
		self.reload_flights()

	def reload_flights(self):
		conn = self.get_conn()
		self.load_flights(conn, True)

	def execute_into_db(self, stmt):
		conn = self.get_conn()
		curr = conn.cursor()
		curr.execute(stmt.query, stmt.params)
		conn.close()

	def find_flight(self, price):
		return [i for i in self.Flights if i.price <= price]

	def sort_flights(self):
		return self.Flights[:].sort(lambda x: x.price)

	def average_company(self):
		companies = {}
		for i in self.Flights:
			if (i.company not in companies):
				companies[i.company] = []
			companies[i.company].append(i.price)
		return [(i, sum(companies[i]) / float(len(companies[i]))) for i in companies]

	def low_cost_flight(self):
		destinations = {}
		for i in self.Flights:
			if (i.destination not in destinations):
				destinations[i.destination] = []
			destinations[i.destination].append(i)
		return [min(destinations[i], key=attrgetter('price')) for i in destinations]

	def remove_flights(self, destinationId):
		flights = [i for i in self.Flights if i.destination.id == destinationId]
		for i in flights:
			self.Flights.remove(i)
		stmt = Statement('DELETE FROM Flights WHERE id in (' + ','.join(['?' for i in flights]) + ')', tuple(flights))
		self.execute_into_db(stmt)
		self.reload_flights()

	def load_flights(self, conn, close=False):
		curr = conn.cursor()
		curr.execute("SELECT * from Flights")
		self.Flights = [Flight(i[0], self.get_company_by_id(i[1]), self.get_destination_by_id(i[2]), i[3]) for i in
		                curr.fetchall()]
		if (close):
			conn.close()
