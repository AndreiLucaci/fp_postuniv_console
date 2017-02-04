class Statement():
	def __init__(self, query, params):
		self.query = query
		self.params = params

	def __str__(self):
		times = self.query.count('?')
		query = self.query
		for i in range(times):
			query = query.replace('\?', self.params[i], 1)
		return query