class Flight():
	def __init__(self, id, company, destination, price):
		self.id = id
		self.company = company
		self.price = price
		self.destination = destination

	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return self.id == other.id
		return NotImplemented

	def __ne__(self, other):
		if isinstance(other, self.__class__):
			return not self.__eq__(other)
		return NotImplemented

	def __hash__(self):
		return hash(tuple(sorted(self.__dict__.items())))

