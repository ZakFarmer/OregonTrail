from pygame import sprite, image
from random import randint

class BackgroundSprites(sprite.Sprite):
	def __init__(self, size, colour, posX, posY, picture, resourcePath):
		sprite.Sprite.__init__(self)
		self.picture = picture
		self.image = image.load(resourcePath + "img/" + self.picture + ".png")
		self.rect = self.image.get_rect()
		self.rect.centerx = posX
		self.rect.centery = posY
		self.size = size
		self.colour = colour
	
	def update(self, game):
		if (self.rect.right > game.gameWindow.get_width() + 100):
			self.rect.left = randint(-150, -100)
			if (self.picture == "cloud"):
				randomY = randint(0, 100)
			elif (self.picture == "tree"):
				randomY = randint(int(game.gameWindow.get_height() - game.gameWindow.get_height() / 3 - 80),
								  int(game.gameWindow.get_height() - game.gameWindow.get_height() / 3 - 5))
			else:
				randomY = 0
			self.rect.centerx = randomY
		self.rect.centerx += 2 * game.moveValue