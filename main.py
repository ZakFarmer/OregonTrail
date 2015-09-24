import pygame
import random
import string
import copy
import colorsys
import pickle
import time

from lib.afflictions import Afflictions
from lib.backgroundSprites import BackgroundSprites
from lib.riverDebris import RiverDebris
from lib.passenger import Passenger
from lib.passengerTab import PassengerTab
from lib.optionButton import OptionButton
from lib.showFaces import ShowFaces
from lib.tombstone import Tombstone
from lib.shop import Shop
from lib.afflictionBox import AfflictionBox
from lib.menuButton import MenuButton
from lib.buffalo import Buffalo
from lib.event import Event
from lib.riverOptionButton import RiverOptionButton

import lib.eztext as eztext


pygame.init()
clock = pygame.time.Clock()

resourcePath = "res/"

# (Infectivity Chance, Spread, Season, Health Change, (min recovery, max recovery))}
afflictionsDict = {"Dysentry": (0.7, 6, "winter", 7, (4, 6)), # 'You have died of dysentry!'
                    "Cholera": (0.4, 3, "summer", 6, (3, 4)),
                    "The Common Cold":  (0.5, 5, "winter", -2.5, (4, 10)),
                    "The Flu": (0.2, 10, "winter", -5.5, (9, 15)),
                    "Hunger": (0, 0, "none", -2, -1),
                    "Well Fed": (0, 0, "none", 2, -1)
                    }

passengerList = [Passenger(name = "Rare Pepe", age = 56, gender = "male", image = resourcePath + "img/passengers/passenger1.png"),
                 Passenger(name = "Ainsley Harriott", age = 14, gender = "male", image = resourcePath + "img/passengers/passenger2.png"),
                 Passenger(name = "Michael Rosen", age = 56, gender = "male", image = resourcePath + "img/passengers/passenger3.png")]
afflictionsList = []
deceasedList = []
groupAfflictions = []

male_picture_list = ["maleface1", "maleface2", "maleface3", "maleface4", "maleface5"]
female_picture_list = []

class Game():
    def __init__(self):
        flags = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.FULLSCREEN
        self.gameWindow = pygame.display.set_mode((1280, 800)) # Add ', flags' to set mode for fullscreen
        self.game_surface = pygame.Surface((self.gameWindow.get_size())).convert()
        self.game_surface.fill((255, 255, 255))
        self.gameWindow.blit(self.game_surface,  (0, 0))
        self.shape_group = pygame.sprite.Group()
        self.turn_menu_surface_offsetx = self.gameWindow.get_width() * (100./1280)
        self.turn_menu_surface_offsety = self.gameWindow.get_height() * (100./720)
        self.turn_menu_surface = pygame.Surface((0, 0)).convert()
        self.exit_button = pygame.image.load(resourcePath+"img/exit.png")
        self.exit_button_rect = self.exit_button.get_rect()
        self.exit_button_rect.centerx = self.gameWindow.get_width() - self.exit_button.get_width() / 2
        self.exit_button_rect.centery = self.exit_button.get_height()/2
        self.tombImage = pygame.image.load(resourcePath+"img/tombstone.png")
        self.town_image = pygame.image.load(resourcePath+"img/town.png")
        self.road = pygame.Surface((self.gameWindow.get_width(), self.gameWindow.get_height() / 3)).convert()
        self.road.fill((139, 69, 19))
        self.shop_blitPosition = (self.gameWindow.get_width() - self.gameWindow.get_width()*(2./5),
                                   self.gameWindow.get_height()*(1./8))
        self.info_menu_blitPosition = (200, 200)
        self.menu_bar = pygame.Surface((0, 0)).convert()
        self.logbook_render_pos = (200, 200)
        self.logbook_up_rect = pygame.Rect(0, 0, 0, 0)
        self.logbook_down_rect = pygame.Rect(0, 0, 0, 0)
        self.food_menu_up_rect = pygame.Rect(0, 0, 0, 0)
        self.food_menu_down_rect = pygame.Rect(0, 0, 0, 0)
        self.food_menu_blit_pos = (400, 200)
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
        self.currencySymbol = "$"
        self.turn_passengerList = []
        self.change_list = []
        self.num_passengers = 3
        self.num_events = 10
        self.gameLength = 100
        self.groupPos = 0
        self.groupInventory = {"Horses": 1,
                                "Spare Wheels": 2,
                                "Food": 52*self.num_passengers}
        self.moveValue = self.groupInventory["Horses"]
        self.groupMoney = 200
        self.itemPrices = {"Horses": 150,
                            "Spare Wheels": 40,
                            "Food": 1}
        self.optionList = ["Kill", "Info", "Food"]
        self.option_button_list = []
        self.logbook = []
        self.logbook_dict = {}
        self.menu_list = ["logbook", "settings"]
        self.menuButtonList = []
        self.inTown = None
        self.output_text = []
        self.painting = False
        self.town_list = [Shop(name="Starting Town", inventory={}, priceModifier=1,
                               groupInventory=self.groupInventory,
                               groupMoney=self.groupMoney,
                               itemPrices=self.itemPrices,
                               position=1,
                               blitPosition=self.shop_blitPosition,
                               money=None,
                               resourcePath=resourcePath)]
        self.affliction_button_list = []
        for _ in range(2):
            random_mod = round(random.uniform(0.1, 2.0), 3)
            calculate_pos = True
            while calculate_pos:
                random_pos = random.randint(6, 100)
                print(random_pos)
                for town in self.town_list:
                    if abs(random_pos - town.position) >= 0:
                        self.town_list.append(Shop(name="", inventory={}, priceModifier=random_mod,
                                                   groupInventory=self.groupInventory,
                                                   groupMoney=self.groupMoney,
                                                   itemPrices=self.itemPrices,
                                                   position=random_pos,
                                                   blitPosition=self.shop_blitPosition,
                                                   money=None,
                                                   resourcePath=resourcePath))
                        print("Town created at "+str(random_pos))
                        calculate_pos = False
                        break

        try:
            with open("data/tombstones.dat", "rb") as file_name:
                self.tombstone_list = pickle.load(file_name)
                for tomb in self.tombstone_list:
                    tomb.status = "Old"
        except (EOFError, IOError):
            print("Error opening tombstones.dat, pickling an empty list..")
            with open("data/tombstones.dat", "wb") as file_name:
                self.tombstone_list = []
                pickle.dump([], file_name)

        for x in range(self.num_events):
            valid_pos = False
            loop_counter = 0
            while not valid_pos:
                rand_pos = random.randint(1, self.gameLength)

                if loop_counter >= 100:
                    self.randomBlit.append(Event(xPos=rand_pos, resourcePath=resourcePath))
                    valid_pos = True

                for xPos in [x.xPos for x in self.randomBlit]:
                    if abs(rand_pos - xPos) <= 20:
                        break
                else:
                    self.randomBlit.append(Event(xPos=rand_pos, resourcePath=resourcePath))
                    valid_pos = True
                loop_counter += 1

        for event in self.randomBlit:
            print("["+str(event.goodOrBad)+"] Event " + str(event.eventName) + " created at: " + str(event.eventPos))

    def begin_play(self):
        while True:
            clock.tick(30)
            self.run_background()
            self.calculations()
            self.turn_menu()

    def turn_menu(self):
        xValue = 20
        yValue = 45
        in_turn_menu = True
        pygame.font.init()
        self.turn_passengerList = []
        next_day = pygame.image.load(resourcePath+"img/nextday.png")
        self.turn_menu_surface = pygame.Surface((500, 75 * len(passengerList) + next_day.get_height()+75)).convert()
        self.turn_menu_surface.fill((175.5, 175.5, 175.5))
        next_day_rect = pygame.Rect((0, 0), next_day.get_size())
        next_day_rect.centerx = (self.turn_menu_surface.get_width() + self.turn_menu_surface_offsetx
                                 - next_day.get_width()/2)
        next_day_rect.centery = (self.turn_menu_surface.get_height() + self.turn_menu_surface_offsety
                                 - next_day.get_height()/2)
        font = pygame.font.Font(None, 28)
        status_font = pygame.font.Font(None, 24)
        log_range = [0, 45]
        times_hunted = 0

        for passenger in passengerList:
            self.turn_passengerList.append(PassengerTab(position=(xValue+5, yValue+5), size=(450, 75),
                                                         passenger=passenger, resourcePath=resourcePath))
            yValue += 80

        selected_option_menu = None
        option_hover = None
        mouse_rect = pygame.Rect(0, 0, 0, 0)
        tombstone_hover = None
        selected_info_menu = None
        show_logbook = False
        show_food_menu = None
        event_result = None

        for event in self.randomBlit:
            if event.eventName == "river":
                if self.groupPos == event.eventPos - 1:
                    event_result = self.river
            elif event.eventName == "house":
                if self.groupPos == event.eventPos:
                    event_result = self.house(event)
        self.mini_event()

        while in_turn_menu:
            clock.tick(30)
            events = pygame.event.get()
            for surface in self.turn_passengerList:
                surface.fill((255, 255, 255))
                status_colour = (0, 255, 0)

                health_bar_container = pygame.Surface((75, 25)).convert()
                health_bar_container.fill((0, 0, 0))
                surface.blit(health_bar_container, (surface.get_width() - health_bar_container.get_width() - 5,
                                                    surface.get_height() - health_bar_container.get_height() - 5))
                health_bar = pygame.Surface((int(surface.passenger.health/100.*health_bar_container.get_width()), 25)).convert()

                pass_pic_container = pygame.Surface((75, 75)).convert()
                pass_pic_container.fill((255, 255, 255))
                pass_pic = pygame.image.load(surface.passenger.image)
                pass_pic = pygame.transform.scale(pass_pic, (70, 70))

                if surface.passenger.health >= 50:
                    health_colour = (float((100-surface.passenger.health)*2/100.*255), 255, 0)
                else:
                    health_colour = (255, float(surface.passenger.health*2/100.*255), 0)
                health_bar.fill(health_colour)
                health_text_hls = colorsys.rgb_to_hls(health_colour[0]/255, health_colour[1]/255, health_colour[2]/255)
                health_text_rgb = colorsys.hls_to_rgb(float(((health_text_hls[0]*360)+180) % 360)/360,
                                                      health_text_hls[1],
                                                      health_text_hls[2])
                health_text_colour = tuple([e*255 for e in health_text_rgb[0:3]])

                pass_pic_container.blit(pass_pic, (2.5, 2.5))
                surface.blit(pass_pic_container, (0, 0))
                surface.blit(font.render(surface.passenger.name, 0, (0, 0, 255)), (75, 10))
                surface.blit(health_bar, (surface.get_width() - health_bar_container.get_width() - 5,
                                          surface.get_height() - health_bar_container.get_height() - 5))

                surface.blit(font.render(str(surface.passenger.health), 1, health_text_colour),
                             (surface.get_width() - (health_bar_container.get_width()) + 12,
                              surface.get_height() - (health_bar_container.get_height()) - 3))
                surface.blit(status_font.render("Status: ", 1, (0, 0, 0)),
                             (75, surface.get_height() - 25))

                if surface.passenger.status == "Unhealthy":
                    status_colour = (255, 0, 0)
                surface.blit(status_font.render(str(surface.passenger.status), 1, status_colour),
                             (140, surface.get_height() - 25))
                surface.blit(surface.optionImage, (surface.passengerSurface.get_width() -
                                                    surface.optionImage.get_width(), 0))
                surface.optionRect.x = surface.passengerSurface.get_width() + self.turn_menu_surface_offsetx
                surface.optionRect.y = self.turn_menu_surface_offsety + \
                    surface.position[1] - surface.optionImage.get_height()/2
                self.turn_menu_surface.blit(surface, surface.position)

            self.game_surface.fill((135, 206, 250))
            self.gameWindow.blit(self.game_surface, (0, 0))
            self.gameWindow.blit(self.road, (0, float(self.gameWindow.get_height()) -
                                              float(self.gameWindow.get_height()) / 3))
            for event in self.randomBlit:
                if event.eventName == "river":
                    self.gameWindow.blit(event.surface, (event.xPos, (float(self.gameWindow.get_height()) -
                                                                        float(self.gameWindow.get_height()) / 3)))
            self.shape_group.draw(self.gameWindow)
            self.turn_menu_surface.blit(next_day, (self.turn_menu_surface.get_width() - next_day.get_width(),
                                                   self.turn_menu_surface.get_height() - next_day.get_height()))

            self.turn_menu_surface.blit(font.render(str("Day: "+str(self.daysSinceStart)), 0, (0, 0, 0)),
                                                   (5, 5))
            self.turn_menu_surface.blit(font.render("Position: "+str(self.groupPos), 1, (0, 0, 0)),
                                                   (5, 5 + font.size("Day")[1]))
            self.turn_menu_surface.blit(font.render("Food: "+str(self.groupInventory["Food"]), 0, (0, 0, 0)),
                                                   (5, self.turn_menu_surface.get_height() - font.size('Food')[1]*2))
            self.turn_menu_surface.blit(font.render("Go Hunting", 0, (0, 0, 0)),
                                                   (5, self.turn_menu_surface.get_height()-font.size("Go Hunting")[1]))
            hunting_rect = pygame.Rect((self.turn_menu_surface_offsetx, (self.turn_menu_surface.get_height() +
                                                                         self.turn_menu_surface_offsety -
                                                                         font.size("Go Hunting")[1]*2)),
                                                                         font.size("Go Hunting"))
            for event in self.randomBlit:
                if event.eventName == "house":
                    self.gameWindow.blit(event.surface, (event.xPos, 500))

            for town in self.town_list:
                if self.groupPos == town.position:
                    self.gameWindow.blit(town.get_surface(), self.shop_blitPosition)
                    self.inTown = town
                town.blitPosition = self.shop_blitPosition
                self.gameWindow.blit(self.town_image, (town.xPos - self.town_image.get_width() / 2,
                                                        self.gameWindow.get_height()/2 +
                                                        self.town_image.get_height()/2))
                self.gameWindow.blit(font.render(town.name, 1, (0, 0, 255)),
                                      (town.xPos - self.town_image.get_width() / 2,
                                       (self.gameWindow.get_height()/2 + self.town_image.get_height()/2)+40))

            for tombstone in self.tombstone_list:
                if tombstone.status == "Old":
                    self.gameWindow.blit(self.tombImage, (tombstone.xPos - self.tombImage.get_width() / 2,
                                                            tombstone.yPos))
            for event in events:
                if event.type == pygame.MOUSEMOTION:
                    self.mouseX, self.mouseY = event.pos
                    mouse_rect = pygame.Rect(self.mouseX, self.mouseY, 1, 1)
                if event.type == pygame.MOUSEBUTTONDOWN and self.exit_button_rect.collidepoint(
                        self.mouseX, self.mouseY):
                    pygame.quit()
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN and next_day_rect.collidepoint(self.mouseX, self.mouseY):
                    in_turn_menu = False
                    break

                if mouse_rect.collidelist([x.tombRect for x in self.tombstone_list]) != -1:
                    if not mouse_rect.colliderect(self.turn_menu_surface.get_rect()):
                        tombstone_hover = self.tombstone_list[mouse_rect.collidelist(
                            [x.tombRect for x in self.tombstone_list])]
                    break
                else:
                    tombstone_hover = None

                if mouse_rect.collidelist([x.optionRect for x in self.turn_passengerList]) != -1 and \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    if selected_option_menu is None:
                        selected_option_menu = self.turn_passengerList[mouse_rect.collidelist(
                            [x.optionRect for x in self.turn_passengerList])]
                        break
                    else:
                        selected_option_menu = None
                        self.option_button_list = []

                if mouse_rect.collidelist([button.rect for button in self.option_button_list]) != -1:
                    option_hover = self.option_button_list[mouse_rect.collidelist(
                        [button.rect for button in self.option_button_list])]
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if option_hover.option == "Kill":
                            self.killPassenger(option_hover.passengerTab.passenger)
                            option_hover = None
                            selected_option_menu = None
                            self.option_button_list = []
                            in_turn_menu = False
                            self.turn_menu()
                        elif option_hover.option == "Info":
                            if selected_info_menu is None:
                                selected_info_menu = self.passenger_info(option_hover.passengerTab.passenger,
                                                                         self.info_menu_blitPosition)
                                break
                            else:
                                selected_info_menu = None
                        elif option_hover.option == "Food":
                            if show_food_menu is None:
                                show_food_menu = option_hover.passengerTab.passenger
                            else:
                                show_food_menu = None
                else:
                    option_hover = None

                if self.inTown is not None:
                    if mouse_rect.collidelist([button.imageRect for button in self.inTown.buyButtonList]) != -1:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            the_button = self.inTown.buyButtonList[
                                mouse_rect.collidelist([button.imageRect for button in self.inTown.buyButtonList])]
                            if self.inTown.inventory[the_button.item] > 0:
                                if self.groupMoney > self.inTown.itemPrices[the_button.item]:
                                    self.groupMoney -= self.inTown.itemPrices[the_button.item]
                                    self.inTown.money += self.inTown.itemPrices[the_button.item]
                                    self.groupInventory[the_button.item] += 1
                                    self.inTown.inventory[the_button.item] -= 1
                                else:
                                    self.output_text.append("You don't have enough money for [" + the_button.item + "]")
                            else:
                                self.output_text.append(self.inTown.name + " is out of [" + the_button.item + "]")
                    elif mouse_rect.collidelist([button.imageRect for button in self.inTown.sellButtonList]) != -1:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            the_button = self.inTown.sellButtonList[
                                mouse_rect.collidelist([button.imageRect for button in self.inTown.sellButtonList])]
                            if self.inTown.money > self.inTown.itemPrices[the_button.item]:
                                if self.groupInventory[the_button.item] > 0:
                                    self.groupMoney += self.inTown.itemPrices[the_button.item]
                                    self.inTown.money -= self.inTown.itemPrices[the_button.item]
                                    self.groupInventory[the_button.item] -= 1
                                    self.inTown.inventory[the_button.item] += 1
                                else:
                                    self.output_text.append("You are out of [" + the_button.item + "]")
                            else:
                                self.output_text.append(self.inTown.name + " can't afford [" + the_button.item + "]")
                    self.moveValue = self.groupInventory["Horses"]
                    self.inTown.update(self.groupInventory, self.groupMoney)
                    self.inTown.render()

                if event.type == pygame.MOUSEBUTTONDOWN and mouse_rect.collidelist(
                        [menu_button.rect for menu_button in self.menuButtonList]) != -1:
                    clicked_menu_button = self.menuButtonList[mouse_rect.collidelist(
                        [menu_button.rect for menu_button in self.menuButtonList])]
                    if clicked_menu_button.name == "logbook":
                        show_logbook = not show_logbook
                    elif clicked_menu_button.name == "settings":
                        self.output_text.append("There are no settings.")

                if show_logbook:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.logbook_up_rect.collidepoint((self.mouseX, self.mouseY)):
                            if log_range[0] > 0:
                                list(map(lambda lr: lr-1, log_range[0:2]))
                        elif self.logbook_down_rect.collidepoint((self.mouseX, self.mouseY)):
                            list(map(lambda lr: lr+1, log_range[0:2]))

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            if log_range[0] > 0:
                                    list(map(lambda lr: lr-1, log_range[0:2]))
                        elif event.key == pygame.K_DOWN:
                            list(map(lambda lr: lr+1, log_range[0:2]))

                if show_food_menu is not None and event.type == pygame.MOUSEBUTTONDOWN:
                    if self.food_menu_down_rect.collidepoint((self.mouseX, self.mouseY)):
                        if show_food_menu.foodDivisions > 0:
                            show_food_menu.foodDivisions -= 1
                        else:
                            self.output_text.append("You can't have less than 0 food!")
                    elif self.food_menu_up_rect.collidepoint((self.mouseX, self.mouseY)):
                        if show_food_menu.foodDivisions < 5:
                            show_food_menu.foodDivisions += 1
                        else:
                            self.output_text.append("You can't have more than 5 food!")

                if hunting_rect.collidepoint((self.mouseX, self.mouseY)) and event.type == pygame.MOUSEBUTTONDOWN:
                    self.confirmWindow(self.goHunting(times_hunted), "okay")
                    times_hunted += 1

            if tombstone_hover is not None:
                self.tombstone_info(tombstone_hover)

            self.gameWindow.blit(self.turn_menu_surface, (100, 100))

            if selected_option_menu is not None:
                self.option_button_list = []
                the_option_menu = self.option_menu(selected_option_menu, option_hover)
                self.gameWindow.blit(the_option_menu,
                                      (selected_option_menu.position[0] + selected_option_menu.size[0] +
                                       the_option_menu.get_width(),
                                       selected_option_menu.position[1]+the_option_menu.get_height()))
            if selected_info_menu is not None:
                self.gameWindow.blit(selected_info_menu, self.info_menu_blitPosition)

            if show_food_menu is not None:
                self.gameWindow.blit(self.show_food_menu(show_food_menu), self.info_menu_blitPosition)

            if show_logbook:
                self.gameWindow.blit(self.show_logbook(list(range(log_range[0], log_range[1])), self.logbook_render_pos),
                                      self.logbook_render_pos)

            self.turn_menu_surface.fill((175, 175, 175))
            output_box = self.show_output_box()
            self.gameWindow.blit(output_box, (self.gameWindow.get_width() - output_box.get_width(),
                                               self.gameWindow.get_height() - output_box.get_height() - 200))
            self.gameWindow.blit(self.build_menu_bar(), (0, 0))
            self.gameWindow.blit(self.exit_button, (self.gameWindow.get_width()-self.exit_button.get_width(), 0))
            if event_result is not None:
                self.output_text.append(event_result)
                event_result = None
            pygame.display.flip()

    def run_background(self):
        keep_moving = True
        move_counter = 0
        font = pygame.font.Font(None, 28)
        self.output_text = []
        while keep_moving:
            clock.tick(30)
            if move_counter > 20:
                keep_moving = False
            self.game_surface.fill((135, 206, 250))
            self.gameWindow.blit(self.game_surface, (0, 0))
            self.gameWindow.blit(self.road, (0, float(self.gameWindow.get_height()) -
                                              float(self.gameWindow.get_height()) / 3))

            for event in self.randomBlit:
                event.update(self.moveValue)
                if event.eventName == "river":
                    self.gameWindow.blit(event.surface, (event.xPos, (float(self.gameWindow.get_height()) -
                                                                        float(self.gameWindow.get_height()) / 3)))

            self.shape_group.update(self)
            self.shape_group.draw(self.gameWindow)
            for event in self.randomBlit:
                if event.eventName == "house":
                    self.gameWindow.blit(event.surface, (event.xPos, 500))

            for town in self.town_list:
                town.move(self.moveValue)
                self.gameWindow.blit(self.town_image, (town.xPos - self.town_image.get_width() / 2,
                                                        self.gameWindow.get_height()/2 +
                                                        self.town_image.get_height()/2))
                self.gameWindow.blit(font.render(town.name, 1, (0, 0, 255)),
                                      (town.xPos - self.town_image.get_width() / 2,
                                       (self.gameWindow.get_height()/2 + self.town_image.get_height()/2)+40))
                town.update(self.groupInventory, self.groupMoney)

            for tombstone in self.tombstone_list:
                tombstone.update(self.moveValue)
                if tombstone.status == "Old":
                    self.gameWindow.blit(self.tombImage, (tombstone.xPos - self.tombImage.get_width() / 2,
                                                            tombstone.yPos))

            self.gameWindow.blit(self.build_menu_bar(), (0, 0))
            pygame.display.flip()
            move_counter += self.moveValue
        pygame.display.flip()

    def calculations(self):
        self.day += 1
        self.daysSinceStart += 1
        self.groupPos += self.moveValue
        self.change_list = []
        self.logbook = []

        if self.day == 365:
            self.year += 1
            self.day = 1

        if 1 <= self.day <= 80 or 356 <= self.day <= 365:
            self.season = "Winter"
        elif 81 <= self.day <= 171:
            self.season = "Spring"
        elif 172 <= self.day <= 262:
            self.season = "Summer"
        elif 263 <= self.day <= 355:
            self.season = "Autumn"

        for town in self.town_list:
            if self.groupPos == town.position:
                self.change_list.append("You've arrived at "+town.name)

        for passenger in passengerList:
            total_hp_change = 0.5
            passenger.status = "Healthy"

            if self.groupInventory["Food"] >= passenger.foodDivisions:
                self.groupInventory["Food"] -= passenger.foodDivisions
            else:
                passenger.foodDivisions = 0

            for x in ("Hunger", "Well Fed"):
                for y in passenger.afflictions:
                    if x == y.name:
                        passenger.afflictions.remove(y)

            if passenger.foodDivisions < 2:
                for affliction in afflictionsList:
                    if affliction.name == "Hunger":
                        copy_aff = copy.copy(affliction)
                        copy_aff.healthChange = -3 + (1.5*passenger.foodDivisions)
                        passenger.afflictions.append(copy_aff)
                        self.change_list.append(passenger.name + " is hungry!")
                        break
            elif passenger.foodDivisions > 2:
                for affliction in afflictionsList:
                    if affliction.name == "Well Fed":
                        copy_aff = copy.copy(affliction)
                        copy_aff.healthChange = -3 + (1.5*passenger.foodDivisions)
                        passenger.afflictions.append(copy_aff)
                        break

            for affliction in passenger.afflictions:
                affliction.recoveryTime -= 1
                if affliction.name != "Well Fed":
                    passenger.status = "Unhealthy"
                if affliction.recoveryTime == 0:
                    passenger.afflictions.remove(affliction)
                    groupAfflictions.remove(affliction)
                    self.change_list.append(passenger.name + " has recovered from " + str(affliction.name))
                else:
                    total_hp_change += affliction.healthChange

            if total_hp_change != 0:
                gain_or_loss = "lost "
                if total_hp_change > 0:
                    gain_or_loss = "gained "
                passenger.health += total_hp_change

                if passenger.health < 0:
                    passenger.health = 0
                elif passenger.health > 100:
                    passenger.health = 100

                if passenger.health != 100:
                    format_args = (passengerName, gain_or_loss,
                                   str(abs(total_hp_change)),
                                   str(passenger.health))
                    change_string = "{} has {} {} health for a total of {}".format(*format_args)
                    self.change_list.append(change_string)

            if passenger.health <= 0:
                self.killPassenger(passenger)
                print(passenger, "has died!")
                break

            for affliction in afflictionsList:
                modifier = 0
                if affliction in groupAfflictions and affliction not in passenger.afflictions:
                    modifier += affliction.infectivity
                if affliction not in passenger.afflictions:
                    rand_chance = round(random.uniform(0, 100), 2)
                    if rand_chance <= affliction.infectivityChance + modifier:
                        rand_duration = random.randint(affliction.recoveryTime[0],  affliction.recoveryTime[1])
                        copy_affliction = copy.copy(affliction)
                        passenger.afflictions.append(copy_affliction)
                        for x in passenger.afflictions:
                            if x.name == affliction.name:
                                x.recoveryTime = rand_duration
                                format_args = (passenger.name, affliction.name, rand_duration)
                                change_string = "{} has contracted {} for {} days.".format(*format_args)
                                self.change_list.append(change_string)
                        groupAfflictions.append(affliction)

        if len(passengerList) != 0:
            t = "-"*50
            self.logbook.append(t)
            format_args = (self.daysSinceStart, self.season, self.year)
            change_string = "Day: {}, {} of {}".format(*format_args)
            self.logbook.append(change_string)

            if len(self.change_list) == 0:
                self.logbook.append("Nothing happened.")
            else:
                for change in self.change_list:
                    self.logbook.append(change)
            self.logbook.append(t)
        self.logbook_dict[self.daysSinceStart] = self.logbook

    def title_screen(self):
        play_button_col = (255, 255, 255)
        in_title_screen = True
        title = True
        while in_title_screen:
            self.game_surface.fill((0, 0, 0))
            title_font = pygame.font.Font(resourcePath + "fonts/oldwestern.ttf", 100)
            title_text = title_font.render("OREGON TRAIL", 1, (255, 255, 255))
            title_text_pos = title_text.get_rect()
            title_text_pos.centerx = self.gameWindow.get_rect().centerx
            title_text_pos.centery = self.gameWindow.get_rect().centery - 40
            play_font = pygame.font.Font(resourcePath + "fonts/oldwestern.ttf",  36)
            play_text = play_font.render("Play",  1,  (10,  10,  10))
            play_text_pos = play_text.get_rect()
            play_text_pos.centerx = self.gameWindow.get_rect().centerx
            play_text_pos.centery = self.gameWindow.get_rect().centery + 50
            if title:
                play_button = pygame.draw.rect(self.game_surface,  play_button_col,
                                               (self.gameWindow.get_width()/2-100,
                                                self.gameWindow.get_height()/2-25+50, 200, 50))

            self.gameWindow.blit(self.game_surface, (0, 0))
            self.gameWindow.blit(self.exit_button,  (self.gameWindow.get_width()-self.exit_button.get_width(), 0))
            self.gameWindow.blit(play_text,  play_text_pos)
            self.gameWindow.blit(title_text, title_text_pos)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.MOUSEMOTION:
                    self.mouseX, self.mouseY = event.pos

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if title and play_button.collidepoint(self.mouseX, self.mouseY):
                        play_button_col = (0, 0, 175)
                    if self.exit_button_rect.collidepoint(self.mouseX, self.mouseY):
                        pygame.quit()
                        quit()

                if event.type == pygame.MOUSEBUTTONUP:
                    play_button_col = (0, 0, 255)
                    if title and play_button.collidepoint(self.mouseX, self.mouseY):
                        self.game_surface.fill((135, 206, 250))
                        self.gameWindow.blit(self.game_surface, (0, 0))
                        title = False
                        in_title_screen = False
            pygame.display.flip()
        self.begin_play()

    def tombstone_info(self, tombstone):
        tombSurface = pygame.Surface((200, 300)).convert()
        tombSurface.fill((175, 175, 175))
        font = pygame.font.Font(None, 18)
        blit_x = 0
        face_image = pygame.image.load(resourcePath + "img/Faces/" + tombstone.passenger.picture + ".png")
        tombSurface.blit(face_image, (tombSurface.get_width()/2 - face_image.get_width()/2, 10))
        tombSurface.blit(font.render("Name: %s" % tombstone.passenger.name, 1, (0, 0, 0)), (5, 110))
        tombSurface.blit(font.render("Age : %s" % tombstone.passenger.age, 1, (0, 0, 0)), (5, 120))
        tombSurface.blit(font.render("Cause of Death: %s" % tombstone.causeOfDeath, 1, (0, 0, 0)), (5, 130))
        tombSurface.blit(font.render("Position: %s" % tombstone.position, 1, (0, 0, 0)), (5, 140))

        if tombstone.xPos + tombstone.tombWidth <= self.gameWindow.get_width() - tombSurface.get_width():
            blit_x = tombstone.xPos + tombstone.tombWidth
        elif tombstone.xPos + tombstone.tombWidth >= self.gameWindow.get_width() - tombSurface.get_width():
            blit_x = tombstone.xPos - tombSurface.get_width()
        self.gameWindow.blit(tombSurface, (blit_x, tombstone.yPos - tombstone.tombHeight))

    def mini_event(self):

        events = {"lose_wheel": 1, "find_food": 5}
        the_event = None
        for event in events:
            if round(random.randint(1, 100), 1) <= events[event]:
                the_event = event
                break

        if the_event == "lose_wheel":
            if self.groupInventory["Spare Wheels"] > 0:
                self.confirmWindow("The wagon hit a large hole and lost a wheel!", "okay")
                self.groupInventory["Spare Wheels"] -= 1

        elif the_event == "find_food":
            rand_amount = random.randint(1, 50)
            prompts = ["You come across an abandoned wagon and find " + str(rand_amount) + " Food.",
                       "You find an unattended crop of corn. You're able to harvest [" + str(rand_amount) + "] Food."]
            self.confirmWindow(random.choice(prompts), "okay")
            self.groupInventory["Food"] += rand_amount

    def build_menu_bar(self):
        self.menu_bar = pygame.Surface((35*len(self.menu_list) + 10, 34)).convert()
        self.menu_bar.fill((175, 175, 175))
        self.menu_bar.set_alpha(200)
        self.menuButtonList = []
        xValue = 5

        for path in self.menu_list:
            self.menuButtonList.append(MenuButton(image=resourcePath+"img/"+path+".png",
                                                    name=path))
        for button in self.menuButtonList:
            button_image = pygame.transform.scale(pygame.image.load(button.image), (32, 32))
            position = xValue, (self.menu_bar.get_height() - button_image.get_height())/2
            self.menu_bar.blit(button_image, position)
            button.update(position, button_image.get_size())
            xValue += button_image.get_width() + 5
        return self.menu_bar

    def killPassenger(self, passenger):
        passengerList.remove(passenger)
        deceasedList.append(passenger)
        death_cause = "Unknown Causes" # If the death cause is not defined, display default cause (Unknown Causes)

        for affliction in passenger.afflictions:
            if affliction.healthChange < 0:
                death_cause = affliction.name
                break
        append_tomb = Tombstone(position=self.groupPos, status="New",
                                passenger=passenger, causeOfDeath=death_cause,
                                tombWidth=self.tombImage.get_width(),
                                tombHeight=self.tombImage.get_height())
        self.tombstone_list.append(append_tomb)
        print("Creating tombstone at position: " + str(self.groupPos))

        try:
            with open("data/tombstones.dat", "rb") as file_name:
                temp_list = pickle.load(file_name)
                temp_list.append(append_tomb)

            with open("data/tombstones.dat", "wb") as file_name:
                pickle.dump(temp_list, file_name)

        except (EOFError, IOError) as error:
            print("Error occurred when saving to tombstones.dat. No tombstones will be saved.")
            print("Error: "+error)

        self.change_list.append(passenger.name+" has died.")
        self.confirmWindow(passenger.name+" has died.", "okay")

        if len(passengerList) == 0:
            print("It's game over, man! Game over!")
            self.game_over()

    def option_menu(self, passengerTab, hover):
        pygame.font.init()
        option_offset = 20./6.5
        option_menu_surface = pygame.Surface((100+option_offset*2,
                                              option_offset + (20 + option_offset)*len(self.optionList))).convert()
        option_menu_surface.fill((100, 100, 100))
        yValue = option_offset

        if len(self.option_button_list) != len(self.optionList):
            for option in self.optionList:
                self.option_button_list.append(OptionButton(passengerTab=passengerTab,
                                                            option=option,
                                                            size=(100, 20),
                                                            hover=hover))

        for button in self.option_button_list:
            option_menu_surface.blit(button.buttonSurface, (option_offset, yValue))
            button.rect = pygame.Rect((passengerTab.position[0] +
                                       passengerTab.size[0] + option_menu_surface.get_width() + option_offset,
                                       passengerTab.position[1] + yValue + option_menu_surface.get_height()),
                                      button.size)
            yValue += button.size[1] + option_offset
        return option_menu_surface

    def passenger_info(self, passenger, blit_pos):
        border_offset = float(15)
        info_font = pygame.font.Font(None, 30)
        xValue = 0
        self.affliction_button_list = []
        for affliction in passenger.afflictions:
            self.affliction_button_list.append(AfflictionBox(affliction=affliction,
                                                             font=info_font))
        passenger_info_filler_surface = pygame.Surface((400 + border_offset, 200 + border_offset)).convert()
        passenger_info_filler_surface.fill((0, 255, 0))
        passenger_info_surface = pygame.Surface((400, 200)).convert()
        passenger_info_surface.fill((255, 255, 255))
        passengerPicture = pygame.image.load(passenger.image)
        passenger_info_surface.blit(passengerPicture, (0, 0))

        passenger_info_surface.blit(info_font.render("Name: ", 1, (255, 0, 0)),
                                    (passengerPicture.get_width() + 5, float(passengerPicture.get_height())/10))
        passenger_info_surface.blit(info_font.render(passenger.name, 1, (0, 0, 255)),
                                    (passengerPicture.get_width() + 5 + info_font.size("Name: ")[0],
                                     float(passengerPicture.get_height())/10))
        passenger_info_surface.blit(info_font.render("Age: "+str(passenger.age), 1, (255, 0, 0)),
                                    (passengerPicture.get_width() + 5, float(passengerPicture.get_height())/2))
        passenger_info_surface.blit(info_font.render(str(passenger.age), 1, (0, 0, 255)),
                                    (passengerPicture.get_width() + 5 + info_font.size("Age: ")[0],
                                     float(passengerPicture.get_height())/2))
        passenger_info_surface.blit(info_font.render("Gender: ", 1, (255, 0, 0)),
                                    (passengerPicture.get_width()*2, float(passengerPicture.get_height()/2)))
        passenger_info_surface.blit(info_font.render(passenger.gender, 1, (0, 0, 255)),
                                    ((passengerPicture.get_width()*2) + info_font.size("Gender: ")[0],
                                     float(passengerPicture.get_height()/2)))
        passenger_info_surface.blit(info_font.render("Afflictions: ", 1, (255, 0, 0)),
                                    (0, passengerPicture.get_height() + passengerPicture.get_height()/10))
        xValue += info_font.size("Afflictions: ")[0]

        if len(self.affliction_button_list) == 0:
            passenger_info_surface.blit(info_font.render("None", 1, (0, 0, 255)),
                                        (xValue, passengerPicture.get_height() + passengerPicture.get_height()/10))

        else:
            for affliction_button in self.affliction_button_list:
                if xValue + affliction_button.text_size[0] < passenger_info_surface.get_width():
                    passenger_info_surface.blit(info_font.render(affliction_button.name, 1, (0, 0, 255)),
                                                (xValue,
                                                 passengerPicture.get_height() +
                                                 passengerPicture.get_height()/10))
                    affliction_button.update((xValue + blit_pos[0],
                                              blit_pos[1] + passengerPicture.get_height() +
                                              passengerPicture.get_height()/10))
                    xValue += affliction_button.text_size[0]
                else:
                    break

        passenger_info_filler_surface.blit(passenger_info_surface, (border_offset/2, border_offset/2))
        return passenger_info_filler_surface

    def show_logbook(self, line_range, render_pos):
        offset = 5
        logbook_border = pygame.Surface((410, 510)).convert()
        logbook_surface = pygame.Surface((400, 500)).convert()
        logbook_surface.fill((255, 255, 255))
        text = pygame.font.Font(None, 15)
        char_height = text.size("LOREM IPSUM")[1]
        yValue = char_height + 1
        cur_line = 0

        for key in list(self.logbook_dict.keys()):
            for line in self.logbook_dict[key]:
                if cur_line in line_range:
                    logbook_surface.blit(text.render(line, 1, (0, 0, 255)), (1, yValue))
                    yValue += char_height + 1
                cur_line += 1

        up_image = pygame.image.load(resourcePath+"img/uparrow.png")
        down_image = pygame.image.load(resourcePath+"img/downarrow.png")
        logbook_surface.blit(up_image, (logbook_surface.get_width() - up_image.get_width(), 0))
        self.logbook_up_rect = pygame.Rect((render_pos[0] + logbook_surface.get_width() - up_image.get_width(),
                                            render_pos[1]), up_image.get_size())

        logbook_surface.blit(down_image, (logbook_surface.get_width() - down_image.get_width(),
                                          logbook_surface.get_height() - down_image.get_height()))

        self.logbook_down_rect = pygame.Rect((render_pos[0] + logbook_surface.get_width() - down_image.get_width(),
                                              render_pos[1] + logbook_surface.get_height() - down_image.get_height()),
                                             down_image.get_size())
        logbook_border.blit(logbook_surface, (offset, offset))
        return logbook_border

    def confirmWindow(self, message, selection):
        pygame.key.set_repeat(0, 0)
        in_confirm_window = True
        confirm_outline = pygame.Surface((210, 110)).convert()
        confirm_window = pygame.Surface((200, 100)).convert()
        confirm_window.fill((255, 255, 255))

        okay_button_rect = pygame.Rect((0, 0), (0, 0))
        yes_button_rect = pygame.Rect((0, 0), (0, 0))
        no_button_rect = pygame.Rect((0, 0), (0, 0))

        pos = (self.gameWindow.get_width()/2 - confirm_window.get_width()/2,
               self.gameWindow.get_height()/2 - confirm_window.get_height()/2)
        font = pygame.font.Font(None, 20)
        text = []

        pixel_selection = ([pos[0], pos[0]+confirm_outline.get_width()],
                           [pos[1], pos[1]+confirm_outline.get_height()])

        saved_state = pygame.PixelArray(self.gameWindow)[int(pixel_selection[0][0]):int(pixel_selection[0][1]),
                                                          int(pixel_selection[1][0]):int(pixel_selection[1][1])].make_surface()

        if selection == "okay" or selection == "text_entry":
            okay_button = pygame.transform.scale(pygame.image.load(resourcePath + "img/okay_button.png"), (50, 25))
            okay_button_pos = (self.gameWindow.get_width()/2 - okay_button.get_width()/2,
                               self.gameWindow.get_height()/2 + okay_button.get_height())
            okay_button_rect = pygame.Rect(okay_button_pos, (okay_button.get_size()))

            confirm_window.blit(okay_button, (confirm_window.get_width()/2 - okay_button.get_width()/2,
                                              confirm_window.get_height() - okay_button.get_height()))

            if selection == "text_entry":
                entry_box = pygame.Surface((confirm_window.get_width())).convert()
                entry_box.fill((255, 255, 255))
                confirm_window.blit(entry_box, (self.gameWindow.get_height() / 2, self.gameWindow.get_width() / 2))

        elif selection == "yesno":
            yes_button = pygame.transform.scale(pygame.image.load(resourcePath + "img/yes_button.png"), (50, 25))
            yes_button_pos = (self.gameWindow.get_width()/2 - yes_button.get_width() + 5,
                              self.gameWindow.get_height()/2 + yes_button.get_height() + 5)
            yes_button_rect = pygame.Rect(yes_button_pos, (yes_button.get_size()))

            no_button = pygame.transform.scale(pygame.image.load(resourcePath + "img/no_button.png"), (50, 25))
            no_button_pos = (self.gameWindow.get_width()/2 + 5,
                             self.gameWindow.get_height()/2 + no_button.get_height() + 5)
            no_button_rect = pygame.Rect(no_button_pos, (no_button.get_size()))

            confirm_window.blit(yes_button, (confirm_window.get_width()/2 - yes_button.get_width() + 5,
                                             confirm_window.get_height() - yes_button.get_height()))
            confirm_window.blit(no_button, (confirm_window.get_width()/2 + 5,
                                            confirm_window.get_height() - no_button.get_height()))

        yValue = 0
        for l in self.length_splitter(font, message, confirm_window.get_width()):
            confirm_window.blit(font.render(l, 1, (255, 0, 0)), (0, yValue))
            yValue += font.size(l)[1]

        confirm_outline.blit(confirm_window, (5, 5))
        self.gameWindow.blit(confirm_outline, pos)
        pygame.display.flip()
        is_shift = False

        while in_confirm_window:
            if selection == "text_entry":
                entry_box.fill((255, 255, 255))

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.MOUSEMOTION:
                    self.mouseX, self.mouseY = event.pos
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.exit_button_rect.collidepoint(self.mouseX, self.mouseY):
                        in_confirm_window = False
                        pygame.quit()
                        break
                    if okay_button_rect.collidepoint(self.mouseX, self.mouseY):
                        if selection == "text_entry":
                            return "".join(text), saved_state, pos
                        return True

                    if yes_button_rect.collidepoint(self.mouseX, self.mouseY):
                        return True
                    elif no_button_rect.collidepoint(self.mouseX, self.mouseY):
                        return False

                if event.type == pygame.KEYDOWN and selection == "text_entry":
                    if event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
                        is_shift = True
                    if event.key == pygame.K_BACKSPACE:
                        if len(text) > 0:
                            text.pop()
                    else:
                        try:
                            if is_shift:
                                text.append(chr(event.key).upper())
                            else:
                                text.append(chr(event.key))
                        except ValueError:
                            print("Error: [" + str(event.key) + "] out of chr() range.")
                if event.type == pygame.KEYUP and selection == "text_entry":
                    if event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
                        is_shift = False

            if selection == "text_entry":
                entry_box.blit(font.render("".join(text), 1, (255, 0, 0)), (0, 0))
                confirm_window.blit(entry_box, (5, confirm_window.get_height()/2 - entry_box.get_height()+10))
            confirm_outline.blit(confirm_window, (5, 5))
            self.gameWindow.blit(confirm_outline, pos)
            pygame.display.flip()

    @staticmethod
    def length_splitter(font, text, maxlength):
        ret_list = []
        explode = text.split()
        t_str = ""
        while len(explode) > 0:
            if font.size(t_str + explode[0])[0] > maxlength:
                ret_list.append(t_str)
                t_str = ""
            else:
                t_str += explode.pop(0) + " "
                if len(explode) == 0:
                    ret_list.append(t_str)
        return ret_list

    def show_output_box(self):
        offset = 5
        output_border = pygame.Surface((310, 160)).convert()
        output_box = pygame.Surface((300, 150)).convert()
        output_box.fill((255, 255, 255))
        text = pygame.font.Font(None, 15)
        char_height = text.size("LOREM IPSUM")[1]
        yValue = -char_height

        if len(self.output_text) < len(self.logbook_dict[self.daysSinceStart]):
            t_lst = [x for x in self.logbook_dict[self.daysSinceStart]]
            for e in t_lst:
                for l in self.length_splitter(text, e, 300):
                    self.output_text.append(l)

        for output in self.output_text:
            out_y = output_box.get_height()-(char_height*len(self.output_text))+yValue
            output_box.blit(text.render(output, 1, (0, 0, 255)), (0, out_y))
            yValue += char_height
        output_border.blit(output_box, (offset, offset))
        return output_border

    def show_food_menu(self, passenger):
        offset = 5
        food_menu_surface_border = pygame.Surface((310, 110)).convert()
        food_menu_surface = pygame.Surface((300, 100)).convert()
        food_menu_surface.fill((255, 255, 255))
        text = pygame.font.Font(None, 20)
        up_image = pygame.transform.scale(pygame.image.load(resourcePath+"img/uparrow.png"), (25, 25))
        down_image = pygame.transform.scale(pygame.image.load(resourcePath+"img/downarrow.png"), (25, 25))
        food_menu_surface.blit(text.render(passenger.name, 1, (0, 0, 255)), (10, food_menu_surface.get_height()/4))
        food_menu_surface.blit(text.render("Food Division: ", 1, (255, 0, 0)), (10, food_menu_surface.get_height()/2))
        food_menu_surface.blit(text.render(str(passenger.foodDivisions), 1, (0, 0, 255)),
                               (10 + text.size("Food Division: ")[0], food_menu_surface.get_height()/2))
        food_menu_surface.blit(text.render("Change from food: ", 1, (255, 0, 0)),
                               (10, food_menu_surface.get_height() * 3/4))
        food_menu_surface.blit(text.render(str(-3 + (1.5 * passenger.foodDivisions)), 1, (0, 0, 255)),
                               (10 + text.size("Change from food: ")[0], food_menu_surface.get_height() * 3/4))

        food_menu_surface.blit(up_image, (food_menu_surface.get_width() - up_image.get_width(), 0))
        self.food_menu_up_rect = pygame.Rect((food_menu_surface.get_width() - up_image.get_width() +
                                              self.info_menu_blitPosition[0], self.info_menu_blitPosition[1]),
                                             up_image.get_size())

        food_menu_surface.blit(down_image, (food_menu_surface.get_width() - down_image.get_width(),
                                            food_menu_surface.get_height() - down_image.get_height()))
        self.food_menu_down_rect = pygame.Rect((food_menu_surface.get_width() - down_image.get_width() +
                                                self.info_menu_blitPosition[0], self.info_menu_blitPosition[1] +
                                                food_menu_surface.get_height() - down_image.get_height()),
                                               down_image.get_size())
        food_menu_surface_border.blit(food_menu_surface, (offset, offset))
        return food_menu_surface_border

    def goHunting(self, times):
        buffalo_list = []
        hunting = True
        shoot_countdown = 0
        food_yield = 0
        self.game_surface.fill((0, 255, 0))
        self.gameWindow.blit(self.game_surface, (0, 0))
        countdown_text = pygame.font.Font(None, 35)
        counter_text = pygame.font.Font(None, 50)
        cooldown_background = pygame.Surface((300, 50)).convert()
        cooldown_bar = pygame.Surface((300, 50)).convert()
        cooldown_bar.fill((255, 0, 0))
        crosshair = pygame.image.load(resourcePath + "img/crosshair.png")
        gun_shot = pygame.transform.scale(pygame.image.load(resourcePath + "img/bloodsplatter.png"), (20, 20))
        ref_buffalo = pygame.image.load(resourcePath + "img/alive_buffalo.png")
        gun_shot_group = {}
        pygame.mouse.set_visible(False)

        val_funct = 20.46096855 / (1+0.0011517959*2.71828**(2.996546379*times))
        the_max = min(20, max(0, int(val_funct)))

        for _ in range(random.randint(0, the_max)):
            random_size = random.uniform(0.5, 1.5)
            random_y = random.randint(ref_buffalo.get_height(), (self.gameWindow.get_height() * 3/4))
            random_x = random.randint(-self.gameWindow.get_width()/2, self.gameWindow.get_width()/2)
            buffalo_list.append(Buffalo(posX=random_x, posY=random_y,
                                        picture="alive", size=random_size, resourcePath=resourcePath))

        for b in buffalo_list:
            gun_shot_group[b] = []

        while hunting:
            clock.tick(60)
            events = pygame.event.get()
            cooldown_bar = pygame.Surface((shoot_countdown*2, 50)).convert()
            cooldown_background.fill((0, 0, 0))
            cooldown_bar.fill((255, 0, 0))
            cooldown_background.blit(cooldown_bar, (0, 0))
            background_colour = (0, 255, 0)
            self.game_surface.fill(background_colour)
            self.gameWindow.blit(self.game_surface, (0, 0))

            counter = 0
            for check in buffalo_list:
                if check.status == "dead":
                    counter += 1
            hunting = not len(buffalo_list) == counter

            for buffalo in buffalo_list:
                buffalo.update()
                self.gameWindow.blit(buffalo.image, (buffalo.rect.x,
                                                      buffalo.rect.y))
                self.gameWindow.blit(buffalo.healthBarShader, ((buffalo.rect.x + buffalo.image.get_width()/2) -
                                                                  buffalo.healthBarShader.get_width()/2,
                                                                  buffalo.rect.y))
                for g in gun_shot_group[buffalo]:
                    self.gameWindow.blit(gun_shot, (buffalo.rect.x + g[0], buffalo.rect.y + g[1]))

                if buffalo.rect.left > self.gameWindow.get_width():
                    buffalo_list.remove(buffalo)

                if buffalo.rect.y == buffalo.targetY:
                    if random.randint(1, 200) == 1:
                        buffalo.target_y = int(random.randint(ref_buffalo.get_height(),
                                                              (self.gameWindow.get_height() * 3/4)))

                for event in events:
                    if event.type == pygame.MOUSEMOTION:
                        self.mouseX, self.mouseY = event.pos
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.exit_button_rect.collidepoint(self.mouseX, self.mouseY):
                            hunting = False
                        if shoot_countdown <= 0:
                            if buffalo.rect.collidepoint(self.mouseX, self.mouseY):
                                if buffalo.image.get_at((self.mouseX - buffalo.rect.x,
                                                         self.mouseY - buffalo.rect.y)) != (0, 0, 0, 0):
                                    print(buffalo.image.get_at((self.mouseX - buffalo.rect.x,
                                                                self.mouseY - buffalo.rect.y)))
                                    if buffalo.status != "dead":
                                        buffalo.health -= random.randint(40, 130)
                                        if buffalo.health <= 0:
                                            buffalo.health = 0
                                            buffalo.status = "dead"
                                            food_yield += buffalo.value
                                    shoot_countdown = 150
                                    gun_shot_group[buffalo].append(((self.mouseX -
                                                                     gun_shot.get_width()/2) - buffalo.rect.x,
                                                                    (self.mouseY -
                                                                     gun_shot.get_height()/2) - buffalo.rect.y))
                        break

            self.gameWindow.blit(cooldown_background, (self.gameWindow.get_width()/2 -
                                                        cooldown_background.get_width()/2,
                                                        self.gameWindow.get_height() - 100))
            self.gameWindow.blit(self.exit_button, (self.gameWindow.get_width() -
                                                     self.exit_button.get_width(), 0))
            self.gameWindow.blit(countdown_text.render(str(round(float(shoot_countdown) / clock.get_fps(), 1)), 1, (0, 0, 255)),
                                  (self.gameWindow.get_width()/2 - countdown_text.size(str(shoot_countdown))[0],
                                   self.gameWindow.get_height() - 100))
            self.gameWindow.blit(counter_text.render(str(counter), 1, (0, 0, 255)), (0, 0))
            self.gameWindow.blit(crosshair, (self.mouseX - crosshair.get_width()/2,
                                              self.mouseY - crosshair.get_height()/2))
            if shoot_countdown > 0:
                crosshair = pygame.image.load(resourcePath + "img/crosshair_cooldown.png")
                shoot_countdown -= 1
            else:
                crosshair = pygame.image.load(resourcePath + "img/crosshair.png")
            pygame.display.flip()

        pygame.mouse.set_visible(True)
        self.groupInventory["Food"] += int(food_yield)
        return "You brought back " + str(int(food_yield)) + " food!"

    @property
    def river(self):
        font = pygame.font.Font(None, 25)
        options = ["Attempt to wade through the river.",
                   "Attempt to float across the river."]

        is_ferry = random.randint(0, 10) >= 4
        ferry_price = None
        if is_ferry:
            ferry_price = random.randint(50, 250)
            options.append("Purchase a ferry ride across the river for " + self.currencySymbol + str(ferry_price))

        in_menu = True
        font_height = font.size("LOREM IPSUM")[1]
        mouse_rect = pygame.Rect((0, 0), (0, 0))
        box_hover = None
        option = None
        random_risk = random.randint(1, 10000)
        while in_menu:
            yValue = font_height
            object_list = []
            option_box = pygame.Surface((400, 300)).convert()
            option_box.fill((255, 255, 255))
            option_box_container = pygame.Surface((option_box.get_width() + 10, option_box.get_height() + 10)).convert()
            global_offset = (self.gameWindow.get_width() -
                             option_box_container.get_width())/2, \
                            (self.gameWindow.get_height() -
                             option_box_container.get_height())/2
            for opt in options:
                opt_pos = (global_offset[0] + 3, global_offset[1] + yValue)
                create_bool = box_hover is not None and box_hover.option == opt
                object_list.append(RiverOptionButton(option=opt, size=(option_box.get_width(), font_height*3),
                                                     hover=create_bool, pos=opt_pos))
                yValue += font_height*3

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.MOUSEMOTION:
                    self.mouseX, self.mouseY = event.pos
                    mouse_rect = pygame.Rect((self.mouseX, self.mouseY), (1, 1))

                if self.exit_button_rect.collidepoint(self.mouseX, self.mouseY):
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        in_menu = False
                        break

                if mouse_rect.collidelist([x.rect for x in object_list]) != -1:
                    box_hover = object_list[mouse_rect.collidelist([x.rect for x in object_list])]

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if box_hover.option in options:
                            if box_hover.option == "Attempt to wade through the river.":
                                option = "wade"
                                print("You want to wade through the river.")
                            elif box_hover.option == "Attempt to float across the river.":
                                option = "float"
                                print("You want to float across the river.")
                            elif box_hover.option == "Purchase a ferry ride across the river. [$"+str(ferry_price)+"]":
                                option = "ferry"
                                print("You want to purchase a ride.")
                            in_menu = False
                        else:
                            print("Somehow an invalid argument.")
                else:
                    box_hover = None

            if box_hover is not None:
                box_hover.update(True)

            for obj in object_list:
                obj_pos = (obj.pos[0] - global_offset[0], obj.pos[1] - global_offset[1])
                option_box.blit(obj.surface, obj_pos)

            option_box_container.blit(option_box, (5, 5))
            self.game_surface.fill((175, 175, 175))
            self.gameWindow.blit(self.game_surface, (0, 0))
            self.gameWindow.blit(option_box_container, ((self.gameWindow.get_width() -
                                                         option_box_container.get_width())/2,
                                                         (self.gameWindow.get_height() -
                                                         option_box_container.get_height())/2))
            self.gameWindow.blit(self.exit_button, (self.gameWindow.get_width() - self.exit_button.get_width(), 0))
            pygame.display.flip()

        river_surface = pygame.Surface((self.gameWindow.get_width() * 5/8, self.gameWindow.get_height())).convert()
        river_surface.fill((30, 144, 255))
        river_pos = (self.gameWindow.get_width() * 1.5/8, 0)

        wagon = pygame.image.load(resourcePath + "img/wagon.png")
        wagonPos = [self.gameWindow.get_width() * 6.5/8, self.gameWindow.get_height()/2]

        river_random = (self.gameWindow.get_width() * 1.5/8, (self.gameWindow.get_width() * 6.5/8)-wagon.get_width())

        pygame.key.set_repeat(10, 10)
        river_debris_group = []

        for _ in range(random.randint(1, 10)):
            random_x = random.randint(river_random[0], river_random[1])
            random_y = random.randint(0, self.gameWindow.get_height())
            random_size = round(random.uniform(0.5, 1.5), 1)
            river_debris_group.append(RiverDebris(size=random_size,
                                                  posX=random_x,
                                                  posY=random_y,
                                                  randomGen=river_random,
                                                  picture="river_debris",
                                                  riverPos=river_pos[0],
                                                  resourcePath=resourcePath))

        while option == "wade":
            if wagonPos[0] < (self.gameWindow.get_width() * 1.5/8) - wagon.get_width() or \
               wagonPos[1] > self.gameWindow.get_height() + wagon.get_height():
                self.confirmWindow("You made it across safely!", "okay")
                return "You made it across safely!"
            if random.randint(1, random_risk) == 1:
                self.confirmWindow("You were inundated with water!", "okay")
                return "You were inundated with water!"

            wagonPos[0] -= 1
            self.game_surface.fill((139, 69, 19))
            self.gameWindow.blit(self.game_surface, (0, 0))
            self.gameWindow.blit(river_surface, river_pos)
            self.gameWindow.blit(wagon, tuple(wagonPos))
            self.gameWindow.blit(self.exit_button, (self.gameWindow.get_width() - self.exit_button.get_width(), 0))
            pygame.display.flip()

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.MOUSEMOTION:
                    self.mouseX, self.mouseY = event.pos
                if self.exit_button_rect.collidepoint((self.mouseX, self.mouseY)):
                    option = None

        pygame.key.set_repeat(12, 12)
        while option == "float":
            wagon_rect = pygame.Rect(tuple(wagonPos), wagon.get_size())
            if wagonPos[0] < (self.gameWindow.get_width() * 1.5/8) - wagon.get_width() or \
               wagonPos[1] > self.gameWindow.get_height() + wagon.get_height():
                self.confirmWindow("You made it across safely!", "okay")
                pygame.key.set_repeat()
                return "You made it across safely!"

            if wagon_rect.collidelist([x.rect for x in river_debris_group]) != -1:
                self.confirmWindow("You Crashed!", "okay")
                pygame.key.set_repeat()
                return "You Crashed!"

            self.game_surface.fill((139, 69, 19))
            self.gameWindow.blit(self.game_surface, (0, 0))
            river_surface.fill((30, 144, 255))
            self.gameWindow.blit(river_surface, river_pos)

            for deb in river_debris_group:
                self.gameWindow.blit(deb.image, (deb.rect.x, deb.rect.y))
                deb.update(river_surface.get_size())

            self.gameWindow.blit(wagon, tuple(wagonPos))
            self.gameWindow.blit(self.exit_button, (self.gameWindow.get_width() - self.exit_button.get_width(), 0))
            wagonPos[1] += 0.1
            pygame.display.flip()
            events = pygame.event.get()
            keys = pygame.key.get_pressed()
            for event in events:
                if event.type == pygame.MOUSEMOTION:
                    self.mouseX, self.mouseY = event.pos
                if self.exit_button_rect.collidepoint((self.mouseX, self.mouseY)):
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        option = None
                if event.type == pygame.KEYDOWN:
                    if keys[pygame.K_a]:
                        wagonPos[0] -= 1
                    if keys[pygame.K_s]:
                        wagonPos[1] += 1
                    if keys[pygame.K_w]:
                        wagonPos[1] -= 1

        if option == "ferry":
            if self.groupMoney >= ferry_price:
                self.groupMoney -= ferry_price
                self.confirmWindow("You purchased a ride across for $" + str(ferry_price), "okay")
                return "You purchased a ride across for $" + str(ferry_price)
            else:
                self.confirmWindow("You don't have enough money to hire a ferry.", "okay")

    def house(self, event):
        approach_prompt = "You come across a house by the side of the road. Do you investigate?"
        if self.confirmWindow(approach_prompt, "yesno"):
            item_changed = {}
            gain_loss_phrases = [{"You found": " in the house.",
                                  "You scavenged": " from the house",
                                  "Found": " in the house.",
                                  "You came across": " near the house."},
                                 {"Bandits stole": " from the wagon.",
                                  "You were ambushed by bandits and lost": ".",
                                  "You were attacked by thieves who stole": " from you.",
                                  "You came back to the wagon to find": "missing."}]
            rand_phrase = random.choice(list(gain_loss_phrases[event.goodOrBad].keys()))
            change_report = rand_phrase
            amount_items = random.randint(1, len(self.groupInventory))
            for n in range(amount_items):
                the_item = list(self.groupInventory.keys())[n]
                amount_changed = random.randint(0, self.groupInventory[the_item])
                item_changed[the_item] = amount_changed * event.goodOrBad

            for i in list(item_changed.keys()):
                self.groupInventory[i] += item_changed[i]
                change_report += (str(", ["+str(abs(item_changed[i]))+" "+str(i)+"]"))
            change_report += " " + str(gain_loss_phrases[event.goodOrBad][rand_phrase])
            self.confirmWindow(change_report, "okay")
            return change_report
        return "You decide to continue on the road."

    def get_neighbors(self, pixel):
        neighbors = []
        if pixel[0] > 2:
            neighbors.append((pixel[0] - 2, pixel[1]))
        if pixel[0] < self.canvas.get_width() - 2:
            neighbors.append((pixel[0] + 2, pixel[1]))
        if pixel[1] > 2:
            neighbors.append((pixel[0], pixel[1] - 2))
        if pixel[1] < self.canvas.get_height() - 2:
            neighbors.append((pixel[0], pixel[1] + 2))
        return neighbors

    def paint_bucket(self, pixel, colour, fill_colour, g_pos):
        show_steps = False
        checked = [pixel]
        array = pygame.PixelArray(self.canvas)
        while len(checked) > 0:
            pix = checked.pop(0)
            if show_steps:
                array = pygame.PixelArray(self.canvas)
            if array[pix] == self.canvas.map_rgb(colour):
                array[pix[0]-1:pix[0]+2, pix[1]-1:pix[1]+2].replace(colour, fill_colour)
                for n in self.get_neighbors(pix):
                    if n not in checked:
                        checked.append(n)
            if show_steps:
                del array
                self.gameWindow.blit(self.canvas, g_pos)
                pygame.display.flip()

    @staticmethod
    def compare_surface(s1, s2):
        s1pa = pygame.PixelArray(s1)
        s2pa = pygame.PixelArray(s2)
        for x, y in zip(s1pa, s2pa):
            for a, b in zip(x, y):
                if a != b:
                    return False
        return True

    @staticmethod
    def game_over():
        pygame.quit()
        quit()

def main():
    mainGame = Game()
    random_y = 0

    for counter in range(201):
        randChoice = random.choice(["cloud", "tree"])
        if randChoice == "cloud":
            random_y = random.randint(0, 100)
        elif randChoice == "tree":
            random_y = random.uniform((mainGame.gameWindow.get_height() - mainGame.gameWindow.get_height() / 3 - 45),
                                      (mainGame.gameWindow.get_height() - mainGame.gameWindow.get_height() / 3 - 5))

        random_x = random.uniform(-100, mainGame.gameWindow.get_width()-11)
        mainGame.shape_group.add(BackgroundSprites(size=10,  colour=(255, 0, 0),
                                                   posX=random_x, posY=random_y,
                                                   picture=randChoice, resourcePath="res//"))

    for affliction in afflictionsDict:
        stats = afflictionsDict[affliction]
        afflictionsList.append(Afflictions(name=affliction, infectivityChance=stats[0], infectivity=stats[1],
                                            primeSeason=stats[2], healthChange=stats[3], recoveryTime=stats[4]))

    mainGame.title_screen()

if __name__ == "__main__":
    main()
