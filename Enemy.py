import pygame

class Skeleton(pygame.sprite.Sprite):

    #Ruch
    walk_right = [pygame.image.load('skeleton_walk/tile000.png'),pygame.image.load('skeleton_walk/tile001.png'),pygame.image.load('skeleton_walk/tile002.png'),pygame.image.load('skeleton_walk/tile003.png'),pygame.image.load('skeleton_walk/tile004.png'),pygame.image.load('skeleton_walk/tile005.png'),pygame.image.load('skeleton_walk/tile006.png'),
                  pygame.image.load('skeleton_walk/tile007.png'),pygame.image.load('skeleton_walk/tile008.png'),pygame.image.load('skeleton_walk/tile009.png'),pygame.image.load('skeleton_walk/tile010.png'),pygame.image.load('skeleton_walk/tile011.png'),pygame.image.load('skeleton_walk/tile012.png')]

    walk_left = []
    for i in walk_right:
        i = pygame.transform.flip(i, True, False)
        walk_left.append(i)

    #Atack
    attack_right = [pygame.image.load('skeleton_attack/skeleton_atack000.png'),pygame.image.load('skeleton_attack/skeleton_atack001.png'),pygame.image.load('skeleton_attack/skeleton_atack002.png'),pygame.image.load('skeleton_attack/skeleton_atack003.png'),pygame.image.load('skeleton_attack/skeleton_atack004.png'),pygame.image.load('skeleton_attack/skeleton_atack005.png'),
                    pygame.image.load('skeleton_attack/skeleton_atack006.png'),pygame.image.load('skeleton_attack/skeleton_atack007.png'),pygame.image.load('skeleton_attack/skeleton_atack008.png'),pygame.image.load('skeleton_attack/skeleton_atack009.png'),pygame.image.load('skeleton_attack/skeleton_atack10.png'),pygame.image.load('skeleton_attack/skeleton_atack011.png'),
                    pygame.image.load('skeleton_attack/skeleton_atack012.png'),pygame.image.load('skeleton_attack/skeleton_atack013.png'),pygame.image.load('skeleton_attack/skeleton_atack014.png'),pygame.image.load('skeleton_attack/skeleton_atack015.png'),pygame.image.load('skeleton_attack/skeleton_atack016.png'),pygame.image.load('skeleton_attack/skeleton_atack017.png')]

    attack_left = []
    for i in attack_right:
        i = pygame.transform.flip(i, True, False)
        attack_left.append(i)


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
        self.health = 20

        #Sterowanie animacją
        self.attack = False
        self.hit = False #zadawanie obrażeń w odpowiednim momencie
        self.attackCount = 0

    def draw(self):

        if self.attack:

            if self.attackCount + 1 >=36:
                self.attackCount = 0
                self.attack = False

            if self.right:

                self.image = Skeleton.attack_right[self.attackCount // 2]
                self.attackCount += 1

            elif self.left:

                self.image = Skeleton.attack_left[self.attackCount // 2]
                self.attackCount += 1

        else:

            if self.walkCount + 1 >=39:
                self.walkCount = 0

            if self.left:
                self.image = Skeleton.walk_left[self.walkCount // 3]  # obrazków animacja, zmiana animacji co 3 odtworzenia pętli 3*9 = 27
                self.walkCount += 1

            elif self.right:
                self.image = Skeleton.walk_right[self.walkCount // 3]
                self.walkCount += 1

        #Tworzenie maski obiektu
        self.mask = pygame.mask.from_surface(self.image)

        self.screen.blit(self.image, (self.rect.x, self.rect.y))

        #Pasek życia
        self.health_bar()

    def health_bar(self):

        pygame.draw.rect(self.screen, (0, 255, 255), (self.rect.x, self.rect.y - 20, (50 * self.health / 20), 5))

    def update(self):

        if self.health <= 0:
            self.kill()

        #Zmiana kierunku ruchu po osiągnięciu brzegu platformy
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

        #Zadanie obrażeń w odpowiednim momencie
        if self.attackCount >= 12 and self.attackCount <=16:
            self.hit = True




        #self.vel += self.acc
        #self.rect.y += self.vel[1] + 0.5 * self.acc[1]