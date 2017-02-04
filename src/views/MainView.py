class MainView():
	def __init__(self):
		pass


	def main_menu(self):
		print('''Menu
1. Add flights
2. Search flight by price
3. Sort flights ascending by price
4. Remove all flights to a specific destination
5. Show all low cost flights for each destination
6. Show Available destinations
7. Show Available Airplane Companies
8. Show flights
menu prints the menu
q quits''')


	def get_input(self):
		return input('~: ')


	def invalid_command(self, value):
		''' Needs python 3.6 to be able to use fStrings '''
		print(f'Unrecognized command. {value} is not a valid menu entry.')