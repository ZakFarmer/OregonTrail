from pygame import Rect

class Tombstone():
	def __init__(self, position, status, passenger, causeOfDeath, tombWidth, tombHeight):
		self.position = position
		self.status = status
		self.passenger = passenger
		self.causeOfDeath = causeOfDeath
		self.posX = (-self.position * 40) + 1280
		self.posY = 500
		self.tombWidth = tombWidth
		self.tombHeight = tombHeight
		self.tombRect = Rect((self.posX, self.posY), (self.tombWidth, self.tombHeight))
		self.tombRectCenterX = self.posX
		self.tombRectCenterY = self.posY + self.tombHeight / 2
		
	def update(self, moveValue):
		self.posX += 2 * moveValue
		self.tombRectCenterX += 2 * moveValue