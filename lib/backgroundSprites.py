from pygame import sprite, image
from random import randint

class BackgroundSprites(sprite.Sprite):
	def __init__(self, size, colour, posX, posY, picture, resourcePath):
		sprite.Sprite.__init__(self)
		self.picture = picture
		self.image = image.load(resourcePath + "img/" + self.picture + ".png")
		self.rect = self.image.get_rect()
		self.rect.centerX = posX
		self.rect.centerY = posY
		self.size = size
		self.colour = colour
	
	def update(self, game):
		if (self.rect.right > game.game_window.get_width() + 100):
			self.rect.left = randint(-150, -100)
			if (self.picture == "cloud"):
				randomY = randint(0, 100)
			elif (self.picture == "tree"):
				randomY = randint(game.game_window.get_height() - game.game_window.get_height() / 3 - 45,
								  game.game_window.get_height() - game.game_window.get_height() / 3 - 5)
			else:
				randomY = 0
			self.rect.centerY = randomY
		self.rect.centerX += 2 * game.moveValue