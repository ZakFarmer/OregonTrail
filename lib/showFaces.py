from pygame import image

class ShowFaces():
	def __init__(self, filePath, colour = (0, 0, 0), posX = 0, posY = 100, resourcePath = ""):
		self.filePath = filePath
		self.colour = colour
		self.posX = posX
		self.posY = posY
		self.resourcePath = resourcePath
		self.image = image.load(self.resourcePath + "img/faces/" + self.filePath + ".png")
		self.faceRect = self.image.get_rect()
		
	def update(self):
		self.faceRect.centerX = self.posX + self.image.get_width() / 2
		self.faceRect.centerY = self.posY + self.image.get_height() / 2