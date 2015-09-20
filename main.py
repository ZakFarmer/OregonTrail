import pygame
import random
import string
import copy
import colorsys
import pickle
import time
import eztext as eztext

from lib.afflictions import Afflictions
from lib.afflictionBox import AfflictionBox
from lib.tombstone import Tombstone
from lib.buffalo import buffalo
from lib.shop import Shop
from lib.passenger import Passenger
from lib.passengerTab import PassengerTab
from lib.riverDebris import RiverDebris
from lib.riverOptionButton import RiverOptionButton
from lib.menuButton import MenuButton
from lib.scrollButton import ScrollButton
from lib.backgroundSprites import BackgroundSprites
from lib.transactionButton import TransactionButton

pygame.init()
clock = pygame.time.Clock()

# "Disease": (Infection chance, infectivity, season, health change, (minimum recovery, maximum recovery))
afflictions = {"The Flu": (0.1, 10, "winter", -10, (9, 14)),
               "Fed": (0, 0, "none", 2, -1),
               "Common Cold": (0.5, 5, "winter", -2.5, (5, 10))
               }

passengerList = []
deceasedList = []
afflictionsList = []
groupAfflictions = []

resources = "res/"
malePictures = []
femalePictures = []

class mainGame():
    def __init__(self):
        flags = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.FULLSCREEN
        self.window = pygame.display.set_mode((1280, 800), flags)
        self.background = pygame.Surface((self.window.get_size())).convert()
        self.background.fill((135, 206, 250))
        self.window.blit(self.background, (0, 0))
        self.spriteGroup = pygame.sprite.Group()
        self.turnMenuSurfaceOffsetX = self.window.get_width() * (100./1280)
        self.turnMenuSurfaceOffsetY = self.window.get_height() * (100./720)
        self.turnMenuSurface = pygame.Surface((0, 0)).convert()
        self.exitButton = pygame.image.load(resources + "img/exitButton.png")
        self.exitButtonRect = self.exitButton.get_rect()
        self.exitButtonRectCenterX = self.window.get_width() - self.exitButton.get_width() / 2
        self.exitButtonRectCenterY = self.exitButton.get_height() / 2
        self.tombstoneImage = pygame.image.load(resources + "img/tombstone.png")
        self.townImage = pygame.image.load(resources + "img/town.png")
        self.road = pygame.Surface((self.window.get_width(), self.window.get_height() / 3)).convert()
        self.road.fill((139, 69, 19))
        self.shopBlitPosition = (self.window.get_width() - self.window.get_width() * (2./5),
                                 self.window.get_height() * (1./8))
        self.infoMenuBlitPosition = (200, 200)
        self.menuBar = pygame.Surface((0, 0)).convert()
        self.logbookRenderPosition = (200, 200)
        self.logbookUpRect = pygame.Rect(0, 0, 0, 0)
        self.logbookDownRect = pygame.Rect(0, 0, 0, 0)
        self.foodMenuUpRect = pygame.Rect(0, 0, 0, 0)
        self.foodMenuDownRect = pygame.Rect(0, 0, 0, 0)
        self.foodMenuBlitPos = (400, 200)
        self.randomBlit = []
        self.canvas = pygame.Surface((400, 300)).convert()
        self.undos = []
        self.redos = []
        
        self.daysSinceStart = 0
        self.day = 0
        self.year = 1850
        self.season = ""
        self.mouseX = 0
        self.mouseY = 0        
        self.turnPassengerList = []
        self.changeList = []
        self.passengerNum = 3
        self.eventNum = 10
        self.gameLength = 100 # 5% of original game length (miles)
        self.groupPos = 0
        self.groupInventory = {"Horses": 1,
                               "Spare Wheels": 2,
                               "Food": 52 * self.passengerNum}
        self.moveValue = self.groupInventory["Horses"]
        self.groupMoney = 200
        self.prices = {"Horses": 200,
                       "Spare Wheels": 50,
                       "Food": 1}
        self.options = ["Kill", "Info", "Food", "Paint"]
        self.optionButtonList = []
        self.logbook = []
        self.logbookDictionary = {}
        self.menu = ["logbook", "settings"]
        self.menuButtonList = []
        self.inTown = None
        self.outputText = []
        self.painting = False
        self.townList = [Shop(name = "Town 1", inventory = {}, priceModifier = 1,
                         groupInventory = self.groupInventory,
                         groupMoney = self.groupMoney,
                         itemPrices = self.itemPrices,
                         position = 1,
                         blitPosition = self.shopBlitPosition,
                         money = None,
                         resources = resources)]
        self.afflictionButtonList = []
        for _ in range(2):
                randomMod = round(random.uniform(0.1, 2.0), 3)
                calculatePos = True
                while calculatePos:
                        randomPos = random.randint(6, 100)
                        print(randomPos)
                        for town in self.townList:
                                if (abs(randomPos - town.position) >= 0):
                                        self.townList.append(Shop(name = "", inventory = {}, priceModifier = randomMod,
                                                             groupInventory = self.groupInventory,
                                                             groupMoney = self.groupMoney,
                                                             itemPrices = self.itemPrices,
                                                             position = randomPos,
                                                             blitPosition = self.shopBlitPosition,
                                                             money = None,
                                                             resources = resources))
                                         print("Town created at", str(randomPos))
                                         calculatePos = False
                                         break
                                        