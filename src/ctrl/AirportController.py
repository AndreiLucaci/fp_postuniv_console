from src.repo.db_repo import DbRepository
from src.validator.Validator import Validator
from src.views.TripView import TripView


class AirportController():
	def __init__(self):
		self.db = DbRepository()
		self.view = TripView()


	def add_flight(self):
		result = self.view.add_new_trip()

		if Validator.not_none(result):
			self._add_flight(result)


	def search_flight(self):
		result = next(iter(self.view.search_flight() or []), None)

		if Validator.not_none(result):
			flights = self.db.find_flight(result)
			self.view.display_list(flights, 'The flights are: ')


	def sort_flights(self):
		self.view.show_flights_ascending_price()
		result = self.db.sort_flights()
		self.view.display_list(result, 'The flights are: ')


	def average_price_per_company(self):
		self.view.show_average_per_airplane_company()
		result = self.db.average_company()
		self.view.display_list(result, 'The companies are: ')


	def remove_all_flights_to_destination(self):
		result = self.view.remove_destination()

		if Validator.not_none(result):
			self.db.remove_flights_by_destination_name(result)

		self.display_flights()


	def low_cost_for_destination(self):
		self.view.low_cost_flights_per_destinations()

		result = self.db.low_cost_flight()

		self.view.display_list(result, 'The low cost flights: ')


	def display_destinations(self):
		self.view.display_list(self.db.Destinations, 'Destinations: ')


	def display_airplane_companies(self):
		self.view.display_list(self.db.Companies, 'Airplane Companies: ')


	def display_flights(self):
		self.view.display_list(self.db.Flights, 'Flights: ')


	def _add_flight(self, results):
		company = results.pop(0)
		price = results.pop(0)
		destination = results.pop(0)
		self.db.add_flight(company, destination, price)






