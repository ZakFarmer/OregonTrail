from pygame.transform import scale
from pygame import image, font, Surface, Rect

class Buffalo():
	def __init__(self, posX, posY, picture, size, resourcePath):
		self.picture = picture
		self.size = size
		self.resourcePath = resourcePath
		self.maxHealth = 100 * self.size
		self.health = self.maxHealth
		self.preimage = image.load(self.resourcePath + "img/" + self.picture + "_buffalo.png")
		self.image = scale(self.preimage, (int(self.preimage.get_width() * self.size),
										   int(self.preimage.get_height() * self.size)))
		self.healthFont = font.Font(None, 20)
		self.healthBarContainer = Surface((int(75 * self.size), int(12 * self.size))).convert()
		self.healthBarShader = Surface((self.healthBarContainer.get_width() + 6,
										self.healthBarContainer.get_height() + 6)).convert()
		self.healthNumber = self.healthFont.render(str(self.health), 1, (0, 0, 0))
		self.healthBarShader.fill((175, 175, 175))
		self.healthBar = Surface(self.healthBarContainer.get_size()).convert()
		self.healthColour = ()
		if (self.health >= 50):
			self.healthColour = (float((self.maxHealth - self.health) * 2 / self.maxHealth * 255), 255, 0)
		else:
			self.healthColour = (255, float(self.health * 2 / self.maxHealth * 255), 0)
		try:
			self.healthBar.fill(self.healthColour)
		except TypeError:
			self.healthBar.fill((0, 0, 0))
		self.healthBarContainer.blit(self.healthBar, (0, 0))
		self.value = 20 * self.size
		self.rect = Rect((0, 0), self.image.get_size())
		self.rect.x = posX
		self.rect.y = posY
		self.status = "alive"
		self.targetY = posY
		
	def update(self):
		self.preimage = image.load(self.resourcePath + "img/" + self.status + "_buffalo.png")
		self.image = scale(self.preimage, (int(self.preimage.get_width() * self.size),
										   int(self.preimage.get_height() * self.size)))
										   
		self.healthBarContainer = Surface((int(75 * self.size), int(12 * self.size))).convert()
		self.healthNumber = self.healthFont.render(str(int(self.health)), 1, (255, 255, 255))
		self.healthBarShader = Surface((self.healthBarContainer.get_width() + 6,
										self.healthBarContainer.get_height() + 6)).convert()
		self.healthBarShader.fill((175, 175, 175))
		if (self.health <= 0):
			self.healthBar = Surface((0, 0)).convert()
		else:
			self.healthBar = Surface((int(self.healthBarContainer.get_width() / self.maxHealth * self.health),
											self.healthBarContainer.get_height())).convert()
											
			if (self.health >= 50):
				self.healthColour = (float((self.maxHealth - self.health) * 2 / self.maxHealth * 255), 255, 0)
			else:
				self.healthColour = (255, float(self.health * 2 / self.maxHealth * 255), 0)
				
			try:
				self.healthBar.fill(self.healthColour)
			except TypeError:
				self.healthBar.fill((0, 0, 0))
			self.healthBarContainer.blit(self.healthBar, (0, 0))
		self.healthBarContainer.blit(self.healthNumber, (self.healthBarContainer.get_width() / 2 -
														 self.healthNumber.get_width() / 2,
														 self.healthBarContainer.get_height() / 2 -
														 self.healthNumber.get_height() / 2))
		self.healthBarShader.blit(self.healthBarContainer, (3, 3))
		
		if (self.status == "alive"):
			self.rect.x += float(3 - self.size)
			if (self.rect.y != self.targetY):
				if (self.rect.y < self.targetY):
					self.rect.y += float(3 - self.size)
				elif (self.rect.y > self.targetY):
					self.rect.y -= float(3 - self.size)
			return self.rect.center