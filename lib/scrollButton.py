from pygame import image, Rect

class ScrollButton():
	def __init__(self, direction, resourcePath):
		self.direction = direction
		if (self.direction == "up"):
			self.image = image.load(resourcePath + "img/uparrow.png")
		elif (self.direction == "down"):
			self.image = image.load(resourcePath + "img/downarrow.png")
		self.rect = Rect((0, 0), self.image.get_size())
		
	def update(self, position):
		self.rect = Rect(position, self.image.get_size())