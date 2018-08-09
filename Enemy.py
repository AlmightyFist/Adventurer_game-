import pygame

class Skeleton(pygame.sprite.Sprite):

    def __init__(self,x, y,  screen):
        super().__init__()

        #Wymiary animacji
        self.height = 33
        self.width = 22

        #Obrazek bazowy
        self.image = pygame.image.load('skeleton_walk/tile000.png')

        #Pozycja postacji
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.screen = screen

    def draw(self):


        self.screen.blit(self.image, (self.x, self.y))