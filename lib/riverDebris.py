from pygame import sprite, image, transform
from random import randint

class RiverDebris(sprite.Sprite):
	def __init__(self, size, posX, posY, randomGen, picture, riverPos, resourcePath):
		sprite.Sprite.__init__(self)
		self.picture = picture
		self.size = size
		self.riverPos = riverPos
		self.randomGen = randomGen
		self.preimage = image.load(resourcePath + "img/" + self.picture + ".png")
		self.image = transform.scale(self.preimage, (int(self.preimage.get_width() * self.size),
									 int(self.preimage.get_height() * self.size)))
		self.rect = self.image.get_rect()
		self.rect.x = posX
		self.rect.y = posY
		
	def update(self, riverres):
		self.rect.y += 1
		if (self.rect.top > riverres[1]):
			self.rect.y = -self.image.get_height()
			self.rect.x = randint(self.randomGen[0], self.randomGen[1])