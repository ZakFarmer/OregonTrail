import pygame.sprite

class Road(pygame.sprite.Sprite):
    def __init__(self, imageFile, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(imageFile)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location