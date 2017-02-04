class Validator():
	def __init__(self):
		pass

	@staticmethod
	def validate_number(value):
		try:
			number = int(value)
			return True, number
		except ValueError:
			return False, 'Value is not a number'

	@staticmethod
	def validate_string(value):
		return False, 'String is empty or None' if value == '' or value == None else True, value


	@staticmethod
	def not_none(value, print_error=False):
		result = value is not None
		if not result and print_error:
			print('Invalid value provided. It is none')

		return result