from random import choice
from pygame import Surface, image

class Event():
	def __init__(self, pos, name = None, resourcePath = ""):
		self.goodOrBad = choie([-1, 1])
		self.surface = Surface((0, 0)).convert()
		self.randomEvents = [self.river, self.house]
		self.name = name
		self.resourcePath = resourcePath
		self.pos = pos
		self.eventTime = ""
		if (self.name is not None):
			if (self.name == "river"):
				self.river()
			elif (self.name == "house"):
				self.house()
		else:
			self.event = choice(self.randomEvents)()
		self.eventPos = self.pos
		self.posX = (-self.eventPos * 40) + 1280
		
	def river(self):
		self.surface = Surface((100, 400)).convert()
		self.surface.fill((30, 144, 255))
		self.eventName = "river"
		
	def house(self):
		self.surface = image.load(self.resourcePath + "img/house.png")
		self.eventName = "house"
		
	def update(self, moveValue):
		self.posX += 2 * moveValue