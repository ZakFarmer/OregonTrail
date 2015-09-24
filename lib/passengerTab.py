from pygame import Surface, Rect, transform, font, image

class PassengerTab(Surface):
	def __init__(self, position, size, passenger, resourcePath):
		Surface.__init__(self, size)
		self.position = position
		self.size = size
		self.passenger = passenger
		self.textFont = font.Font(None, 15)
		self.passengerSurface = Surface(self.size).convert()
		self.rect = Rect(self.position, self.size)
		self.optionImage = transform.scale(image.load(resourcePath + "img/optionIcon.png"), (20, 20))
		self.optionRect = self.optionImage.get_rect()
		
		
