from pygame import Rect

class AfflictionBox():
	def __init__(self, affliction, font, rectPosition = (0, 0)):
		self.affliction = affliction
		self.rectPosition = rectPosition
		self.name = self.affliction.name
		self.font = font
		self.textSize = self.font.size(self.name)
		self.textRect = Rect(self.rectPosition, self.textSize)
		
	def update(self, rectPosition):
		self.rectPosition = rectPosition
		self.textRect.center.x = rectPosition[0] + self.textSize[0]
		self.textRect.center.y = rectPosition[1] + self.textSize[1]