from pygame import Surface, Rect, font

class RiverOptionButton():
	def __init__(self, option, size, hover, pos):
		self.option = option
		self.size = size
		self.hover = hover
		self.surface = Surface(self.size).convert()
		self.pos = pos
		if (self.hover):
			self.surface.fill((200, 200, 200))
		else:
			self.surface.fill((255, 255, 255))
		self.rect = Rect(self.pos, self.size)
		self.buttonFont = font.Font(None, 25)
		self.surface.blit(self.buttonFont.render(self.option, 1, (0, 0, 0))
						 (5, self.size[1] / 2 - self.buttonFont.size("Lorem Ipsum")[1] / 2))
						 
	def update(self, hover):
		if (hover):
			self.surface.fill((200, 200, 200))
		else:
			self.surface.fill((255, 255, 255))
			
		self.rect = Rect(self.pos, self.size)
		self.buttonFont = font.Font(None, 25)
		self.surface.blit(self.buttonFont.render(self.option, 1, (0, 0, 0)),
						 (5, self.size[1] / 2 - self.buttonFont.size("Lorem Ipsum")[1] / 2))