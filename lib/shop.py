from pygame import Surface, font
from copy import copy
from random import randint, choice
from string import capitalize

from transactionButton import TransactionButton

SHOP_PREFIX = ["archer", "baker", "fisher", "miller", "rancher", "robber"]
SHOP_SUFFIX = ["cave", "creek", "desert", "farm", "field", "forest", "hill", "lake", "mountain", "pass", "valley", "woods"]

class Shop():
	def __init__(self, name, inventory, priceModifier, groupInventory, groupMoney, itemPrices, position, blitPosition, money, resourcePath):
		self.yValue = 40
		self.groupInventory = groupInventory
		self.groupMoney = groupMoney
		self.priceModifier = priceModifier
		self.itemPrices = itemPrices
		self.inventory = inventory
		self.position = position
		self.blitPosition = blitPosition
		self.resourcePath = resourcePath
		self.buyButtonList = []
		self.sellButtonList = []
		self.posX = (-self.position * 40) + 1280
		
		self.shopSurface = Surface((500, 300)).convert()
		self.sepLine = Surface((self.shopSurface.get_width(), 10)).convert()
		self.sepLine.fill((0, 0, 0))
		
		self.invContainer = Surface((self.shopSurface.get_width() - 20,
									 self.shopSurface.get_height() / 2 - 35)).convert()
		self.invContainer.fill((255, 255, 255))
		self.titleFont = font.Font(None, 30)
		self.textFont = font.Font(None, 20)
		
		if (name == ""):
			self.name = capitalize(choice(SHOP_PREFIX) + "'s " + choice(SHOP_SUFFIX))
		else:
			self.name = name
			
		if (self.inventory == {}):
			inventoryRandom = copy(self.groupInventory)
			for key in list(inventoryRandom.keys()):
				inventoryRandom[key] = randint(0, 10)
				
			inventoryRandom["Food"] *= 20
			self.inventory = inventoryRandom
			
		if (money is None):
			self.money = randint(200, 500)
		else:
			self.name = name
		self.render()
		
	def get_surface(self):
		self.render()
		return self.shopSurface
		
	def update(self, groupInv, groupMoney):
		self.groupInventory = groupInv
		self.groupMoney = groupMoney
		self.render()
		
	def move(self, moveValue):
		self.posX += (2 * moveValue)
		self.render()
		
	def render(self):
		self.yValue = 40
		self.shopSurface.fill((133, 94, 66))
		self.shopSurface.blit(self.titleFont.render(self.name + " - $" + str(self.money), 1, (0, 0, 255)), (10, 5))
		self.shopSurface.blit(self.invContainer, (10, 25))
		self.shopSurface.blit(self.invContainer, (10, self.shopSurface.get_height() / 2 + 30))
		self.shopSurface.blit(self.textFont.render("Inventory", 1, (255, 0, 0)), (10, 25))
		self.shopSurface.blit(self.textFont.render("Amount", 1, (255, 0, 0)), (130, 25))
		self.shopSurface.blit(self.textFont.render("Price", 1, (255, 0, 0)), (200, 25))
		
		for key in list(self.inventory.keys()):
			self.shopSurface.blit(self.textFont.render(key + ":", 1, (0, 0, 0)), (10, self.yValue))
			self.shopSurface.blit(self.textFont.render(str(self.inventory[key]), 1,
													   (0, 0, 0)), (150, self.yValue))
			self.shopSurface.blit(self.textFont.render("$"+str(self.itemPrices[key] * self.priceModifier), 1, 
													   (0, 0, 0)), (200, self.yValue))
			if (len(self.buyButtonList) < len(self.inventory.keys())):
				buttonPos = tuple(map(sum, zip(self.blitPosition, (250, self.yValue))))
				self.buyButtonList.append(TransactionButton(transaction = "buy",
															item = key,
															imagePosition = (250, self.yValue),
															rectPosition = buttonPos,
															resourcePath = self.resourcePath))
			self.yValue += 30
			
		for button in self.buyButtonList:
			self.shopSurface.blit(button.image, button.imagePosition)
			
		self.shopSurface.blit(self.sepLine, (0, float(self.shopSurface.get_height()) / 2))
		self.shopSurface.blit(self.titleFont.render("You - $" + str(self.groupMoney), 1, (0, 0, 255)),
												    (10, float(self.shopSurface.get_height()) / 2 + 10))
		self.shopSurface.blit(self.titleFont.render("Inventory", 1, (255, 0, 0)),
													(10, float(self.shopSurface.get_height()) / 2 + 30))
		self.shopSurface.blit(self.titleFont.render("Amount", 1, (255, 0, 0)),
													(130, float(self.shopSurface.get_height()) / 2 + 30))
		self.shopSurface.blit(self.titleFont.render("Price", 1, (255, 0, 0)),
													(200, float(self.shopSurface.get_height()) / 2 + 30))
													
		self.yValue = (float(self.shopSurface.get_height()) / 2) + 45
		
		
		for key in list(self.groupInventory.keys()):
			self.shopSurface.blit(self.textFont.render(key + ":", 1, (0, 0, 0)), (10, self.yValue))
			self.shopSurface.blit(self.textFont.render(str(self.groupInventory[key]), 1,
													  (0, 0, 0)), (150, self.yValue))
			self.shopSurface.blit(self.textFont.render("$" + str(self.itemPrices[key] * self.priceModifier), 1,
													  (0, 0, 0)), (200, self.yValue))
			if (len(self.sellButtonList) < len(self.inventory.keys())):
				buttonPos = tuple(map(sum, zip(self.blitPosition, (250, self.yValue))))
				self.sellButtonList.append(TransactionButton(transaction = "sell",
															 item = key,
															 imagePosition = (250, self.yValue),
															 rectPosition = buttonPos,
															 resourcePath = self.rresourcePath))
			self.yValue += 30
			
		for button in self.sellButtonList:
			self.shopSurface.blit(button.image, button.imagePosition)
													
													