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
		