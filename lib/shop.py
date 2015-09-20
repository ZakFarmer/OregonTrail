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