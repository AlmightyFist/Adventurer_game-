import pygame

class Adventurer(pygame.sprite.Sprite):

    #Ładowanie animacji

    run_right = [pygame.image.load('player_run/adventurer-run-00.png'),pygame.image.load('player_run/adventurer-run-01.png'),
                 pygame.image.load('player_run/adventurer-run-02.png'),pygame.image.load('player_run/adventurer-run-03.png'),
                 pygame.image.load('player_run/adventurer-run-04.png')]
    # Odwracanie ruchu w lewo
    run_left = []
    for i in run_right:
        i = pygame.transform.flip(i, True, False)
        run_left.append(i)

    # Stanie w miejscu

    stand_right = [pygame.image.load('player_stand/adventurer-idle-00.png'),pygame.image.load('player_stand/adventurer-idle-01.png'),pygame.image.load('player_stand/adventurer-idle-02.png')]
    # Odwracanie stania w lewo
    stand_left = []
    for i in stand_right:
        i = pygame.transform.flip(i, True, False)
        stand_left.append(i)

    # Skok
    jump_right = [pygame.image.load('player_jump/adventurer-jump-00.png'),pygame.image.load('player_jump/adventurer-jump-01.png'),pygame.image.load('player_jump/adventurer-jump-02.png'),pygame.image.load('player_jump/adventurer-jump-03.png'),
                  pygame.image.load('player_jump/adventurer-jump-04.png'),pygame.image.load('player_jump/adventurer-jump-05.png'),pygame.image.load('player_jump/adventurer-jump-06.png'),pygame.image.load('player_jump/adventurer-jump-07.png')]
    #Odwracanie skoku w lewo
    jump_left = []
    for i in jump_right:
        i = pygame.transform.flip(i, True, False)
        jump_left.append(i)

    #Atack nr 2

    attack2_right = [pygame.image.load('player_attack_2/adventurer-attack2-00.png'),pygame.image.load('player_attack_2/adventurer-attack2-01.png'),pygame.image.load('player_attack_2/adventurer-attack2-02.png'),
                     pygame.image.load('player_attack_2/adventurer-attack2-03.png'),pygame.image.load('player_attack_2/adventurer-attack2-04.png'),pygame.image.load('player_attack_2/adventurer-attack2-05.png')]

    attack2_left = []
    for i in attack2_right:
        i =  pygame.transform.flip(i, True, False)
        attack2_left.append(i)

    def __init__(self,x,y, screen, SCREEN_WIDTH, SCREEN_HEIGHT):

        super().__init__()
        #Reprezentacja klasy na ekranie
        self.image = pygame.image.load('player_stand/adventurer-idle-00.png')
        self.rect = self.image.get_rect()

        #Parametry obiektu na ekranie
        self.x = x
        self.y = y
        self.width = 50
        self.height = 37
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.SCREEN_WIDTH = SCREEN_WIDTH

        #Odniesienie do ekranu
        self.screen = screen

        # Parametry fizyczne postaci
        self.vel = pygame.math.Vector2(5,0) #velocity
        self.acc = pygame.math.Vector2(0,1) #acceleration
        self.jump_power = 20 #jump
        self.friction = -0.08 # Opór powietrza
        self.health = 100

        #Punkacja
        self.score = 0


        #Obsługa ruchu

        self.walkCount = 0
        self.standCount = 0
        self.left = False #lewa strona
        self.right = True # prawa strona
        self.standing = False #stanie
        self.isJump = False #skok
        self.JumpCount = 0 #skok
        self.Jumped = False #skok

    def draw(self):

        if not(self.isJump):# Animacja bez skoku

            if not(self.standing): #Animacja biegu, prawo, lewo

                if self.walkCount + 1 >= 15:  # 5 animacji, 3 * 5 = 15
                    self.walkCount = 0

                if self.left:
                    self.image = Adventurer.run_left[self.walkCount // 3] # obrazków animacja, zmiana animacji co 3 odtworzenia pętli 3*9 = 27
                    self.walkCount += 1
                elif self.right:
                    self.image = Adventurer.run_right[self.walkCount // 3]
                    self.walkCount += 1
            else: #Animacja stania, prawo, lewo

                if  self.standCount + 1 >= 21: # 3 obrazki animacji stania, po 5 pętli na 1
                    self.standCount = 0

                if self.right:
                    self.image = Adventurer.stand_right[self.standCount // 7]
                    self.standCount += 1

                elif self.left:
                    self.image = Adventurer.stand_left[self.standCount // 7]
                self.standCount += 1

        else: # Animacja ze skokiem

            if self.right:
                self.image = Adventurer.jump_right[self.JumpCount // 8]
                self.JumpCount +=1
            elif self.left:
                self.image = Adventurer.jump_left[self.JumpCount // 8]
                self.JumpCount += 1
            if self.JumpCount >= 64:
                self.JumpCount = 0
                self.isJump = False
                self.Jumped = False

        self.screen.blit(self.image,(self.x, self.y))

        #Wyświetlenie paska życia
        self.health_bar()

        #Update atrybutu rect gracza
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def Jump(self, all_platforms):


        self.rect.x += 1
        hits = pygame.sprite.spritecollide(self, all_platforms, False)
        self.rect.x -= 1

        if hits and self.isJump == False:
            self.isJump = True
            self.JumpCount = 0
        if self.isJump:
            #Przygotowanie animacji postaci do skoku
            if self.image in Adventurer.jump_right[0:2] or  self.image in Adventurer.jump_left[0:2]:
                self.vel[1] = 0
            #Wznoszenie, animacja skoku
            elif (self.image in Adventurer.jump_right[2:6] or self.image in Adventurer.jump_left[2:6]) and self.Jumped == False:
                self.vel[1] -= self.jump_power
                #Zmienna określa czy został wykonany skok - dodanie prędkości w pionie
                self.Jumped = True



    def update(self, all_platforms = []):

        # Obsługa sterowania
        keys = pygame.key.get_pressed()

        # Porusznia lewa, prawa
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.vel[0]
            self.left = True
            self.right = False
            self.standing = False
            self.standCount = 0

        elif keys[pygame.K_RIGHT] and self.x < (self.SCREEN_WIDTH - self.width):
            self.x += self.vel[0]
            self.left = False
            self.right = True
            self.standing = False
            self.standCount = 0
        else:
            self.standing = True
            self.walkCount = 0

        # Moduł skoku
        if keys[pygame.K_UP] or self.isJump:
            self.Jump(all_platforms)


        # Równania ruchu
        self.vel += self.acc
        self.y += self.vel[1] + 0.5 * self.acc[1]

    #Metoda wyświetlająca pasek życia bohatera. Pasek zmniejsza się wraz z ilością życia
    def health_bar(self):

        pygame.draw.rect(self.screen, (0,255,0), (self.rect.x, self.rect.y - 20, (50*self.health/100),5))

    #Obsługa przycisków gracza
    def player_events(self):




