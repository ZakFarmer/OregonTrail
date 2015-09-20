class Passenger():
	def __init__(self, name, age, gender, image):
		self.name = name
		self.age = age
		self.gender = gender
		self.image = image
		self.afflictions = []
		self.health = 100
		self.foodDivisions = 2
		self.status = "healthy"
	def __str__(self):
		return(self.name) # Return passenger name.