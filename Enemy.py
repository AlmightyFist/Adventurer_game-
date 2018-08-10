import pygame

class Skeleton(pygame.sprite.Sprite):

    walk_right = [pygame.image.load('skeleton_walk/tile000.png'),pygame.image.load('skeleton_walk/tile001.png'),pygame.image.load('skeleton_walk/tile002.png'),pygame.image.load('skeleton_walk/tile003.png'),pygame.image.load('skeleton_walk/tile004.png'),pygame.image.load('skeleton_walk/tile005.png'),pygame.image.load('skeleton_walk/tile006.png'),
                  pygame.image.load('skeleton_walk/tile007.png'),pygame.image.load('skeleton_walk/tile008.png'),pygame.image.load('skeleton_walk/tile009.png'),pygame.image.load('skeleton_walk/tile010.png'),pygame.image.load('skeleton_walk/tile011.png'),pygame.image.load('skeleton_walk/tile012.png')]

    walk_left = []
    for i in walk_right:
        i = pygame.transform.flip(i, True, False)
        walk_left.append(i)


    def __init__(self,x, y,  screen, platform):
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

        #Zakres ruchu
        self.platform = platform
        self.right = True
        self.left = False
        self.walkCount = 0

        #Parametry fizyczne
        self.vel = pygame.math.Vector2(1, 0)  # velocity
        self.acc = pygame.math.Vector2(0, 1)  # acceleration

    def draw(self):
        if self.walkCount + 1 >=39:
            self.walkCount = 0

        if self.left:
            self.image = Skeleton.walk_left[self.walkCount // 3]  # obrazków animacja, zmiana animacji co 3 odtworzenia pętli 3*9 = 27
            self.walkCount += 1

        elif self.right:
            self.image = Skeleton.walk_right[self.walkCount // 3]
            self.walkCount += 1


        self.screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):

        if self.vel[0] >0:
            if self.rect.x + self.vel[0] <= (self.platform.rect.x + self.platform.width):
                self.rect.x += self.vel[0]
                self.right = True
                self.left = False
            else:
                self.vel[0] = self.vel[0] * -1
                self.walkCount = 0
                self.right = False
        else:
            if self.rect.x - self.vel[0] >= self.platform.rect.x:
                self.rect.x += self.vel[0]
                self.left = True
                self.right = False
            else:
                self.vel[0] = self.vel[0] * -1
                self.walkCount = 0
                self.Left = False




        #self.vel += self.acc
        #self.rect.y += self.vel[1] + 0.5 * self.acc[1]