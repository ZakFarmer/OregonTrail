from pygame import transform, image, Rect

class TransactionButton():
	def __init__(self, transaction, item, imagePosition, rectPosition, resourcePath):
		self.transaction = transaction
		self.item = item
		self.imagePosition = imagePosition
		self.rectPosition = rectPosition
		self.filename = "buybutton.png"
		if (self.transaction == "sell"):
			self.filename = "sellbutton.png"
		self.image = transform.scale(image.load(resourcePath + "img/" + self.filename), (25, 25))
		self.imageRect = Rect(self.rectPosition, self.image.get_size())