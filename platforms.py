import pygame


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()

        #Parametry graficzne/fizyczne platformy
        self.width = width
        self.height = height
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        #Ustawienia platformy w grze
        self.is_skeleton_on = False


    def update(self):
        pass


