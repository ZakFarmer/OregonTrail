from pygame import Rect

class MenuButton():
	def __init__(self, image, imageSize = (0, 0), rectPosition = (0, 0), name = None):
		self.image = image
		self.rectPosition = rectPosition
		self.imageSize = imageSize
		self.name = name
		self.rect = Rect(self.rectPosition, self.imageSize)
		
	def update(self, rectPosition, imageSize):
		self.rectPosition = rectPosition
		self.imageSize = imageSize
		self.rect = Rect(self.rectPosition, self.imageSize)