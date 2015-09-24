from pygame import Rect

class Tombstone():
	def __init__(self, position, status, passenger, causeOfDeath, tombWidth, tombHeight):
		self.position = position
		self.status = status
		self.passenger = passenger
		self.causeOfDeath = causeOfDeath
		self.xPos = (-self.position * 40) + 1280
		self.yPos = 500
		self.tombWidth = tombWidth
		self.tombHeight = tombHeight
		self.tombRect = Rect((self.xPos, self.yPos), (self.tombWidth, self.tombHeight))
		self.tombRectCenterX = self.xPos
		self.tombRectCenterY = self.yPos + self.tombHeight / 2
		
	def update(self, moveValue):
		self.xPos += 2 * moveValue
		self.tombRectCenterX += 2 * moveValue