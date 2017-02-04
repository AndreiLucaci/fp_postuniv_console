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
		answer = value != '' and Validator.not_none(value)
		val = value if answer else 'String is empty or None'
		return answer, val


	@staticmethod
	def not_none(value, print_error=False):
		result = value is not None
		if not result and print_error:
			print('Invalid value provided. It is none')

		return result


	@staticmethod
	def is_none(value):
		return value is None