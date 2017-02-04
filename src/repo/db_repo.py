import sqlite3
from operator import attrgetter

from src.models.AirplaneCompany import AirplaneCompany
from src.models.Flight import Flight
from src.models.Destination import Destination
from src.validator.Validator import Validator
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
		return self.get_first([i for i in self.Companies if i.name.lower() == name.lower()])

	def get_destination_by_name(self, name):
		return self.get_first([i for i in self.Destinations if i.name.lower() == name.lower()])

	def get_first(self, lst):
		return next(iter(lst or []), None)

	def _add_flight(self, Company, Destination, price):
		flight = Flight(0, Company, Destination, price)
		self.Flights.append(flight)
		stmt = Statement("INSERT INTO Flights(company, destination, price) VALUES (?, ?, ?)",
		                 (flight.company.id, flight.destination.id, flight.price))
		self.execute_into_db(stmt)
		self.reload_flights()

	def add_flight(self, company_name, destination_name, price):
		company = self.get_company_by_name(company_name)
		destination = self.get_destination_by_name(destination_name)
		if Validator.is_none(destination):
			self.add_new_destination(destination_name)
			destination = self.get_destination_by_name(destination_name)

		self._add_flight(company, destination, price)

	def add_new_destination(self, destination_name):
		stmt = Statement('INSERT INTO Destinations(name) VALUES (?)', (destination_name,))
		self.execute_into_db(stmt)
		self.load_destinations(self.get_conn(), True)

	def reload_flights(self):
		conn = self.get_conn()
		self.load_flights(conn, True)

	def execute_into_db(self, stmt):
		conn = self.get_conn()
		curr = conn.cursor()
		try:
			curr.execute(stmt.query, stmt.params)
		except sqlite3.Error as ex:
			print (ex)
		conn.commit()
		conn.close()

	def find_flight(self, price):
		return [i for i in self.Flights if i.price <= price]

	def sort_flights(self):
		return sorted(self.Flights, key=lambda x: x.price)

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

	def remove_flights_by_destination_id(self, destination_id):
		flights = [i for i in self.Flights if i.destination.id == destination_id]
		self._remove_flights(flights)

	def remove_flights_by_destination_name(self, destination_name):
		flights = [i for i in self.Flights if i.destination.name == destination_name]
		self._remove_flights(flights)

	def _remove_flights(self, flights):
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
