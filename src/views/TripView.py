from src.validator.Validator import Validator


class TripView():
	def __init__(self):
		pass

	def add_new_trip(self):
		print('''Please add the new trip.
You'll be required an airplane company, a price and a destination''')
		return self.interpret_results(['Airplane Company: ', 'Price: ', 'Destination: '],
		            [Validator.validate_string, Validator.validate_number, Validator.validate_string])


	def show_flights_ascending_price(self):
		print('''Flights ordered by price in an ascending order''')


	def show_average_per_airplane_company(self):
		print('''This is the average price per flight for all the airplane companies''')


	def remove_destination(self):
		print('''You'll be required a destination name, and you'll remove all flights to it''')
		return self.interpret_results(['Destination: '], [Validator.validate_string])


	def low_cost_flights_per_destinations(self):
		print('''This is the list with all low cost flights for destinations''')


	def search_flight(self):
		print('''You want to search for a flight. You'll be required a price.''')
		return self.interpret_results(['Price: '], [Validator.validate_number])


	def interpret_results(self, input_texts, funcs):
		valid, results, errors = self.matcher(input_texts, funcs)

		if not valid:
			self.show_errors(errors)
			return None

		return results


	def show_errors(self, errors):
		for i in errors:
			print(i)


	def matcher(self, input_texts, funcs):
		valid = True
		results = []
		errors = []
		for i, j in zip(input_texts, funcs):
			valid, result = j(input(i))
			if not valid:
				errors.append(result)
				break
			else:
				results.append(result)
		return valid, results, errors

	def display_list(self, lst, header):
		print(header)
		for i in lst: print(i)