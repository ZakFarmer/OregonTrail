from pygame import Surface, font

class OptionButton():
	def __init__(self, passengerTab, option, size, hover):
		self.passengerTab = passengerTab
		self.option = option
		self.size = size
		self.hover = hover
		self.passenger = passengerTab.passenger
		self.buttonSurface = Surface(self.size).convert()
		if (self.hover is not None and self.hover.option == self.option):
			self.buttonSurface.fill((200, 200, 200))
		else:
			self.buttonSurface.fill((255, 255, 255))
		self.buttonRect = self.buttonSurface.get_rect()
		self.buttonFont = font.Font(None, 12)
		self.buttonSurface.blit(self.buttonFont.render(option, 1, (0, 0, 0)),
							   (self.size[0] / 2, self.size[1] / 2))