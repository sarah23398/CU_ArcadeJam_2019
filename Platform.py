import pygame
import os
from pygame.rect import Rect


class Platform(pygame.sprite.Sprite):
    # Represents a window with a Platform that Player can jump on
    def __init__(self, left, top):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(os.path.dirname(__file__),
                                                               "resources/images/sill.png")).convert()
        self.image = pygame.transform.scale(self.image, (170, 28))
        self.rect = self.image.get_rect()
        self.rect.x = left
        self.rect.y = top


