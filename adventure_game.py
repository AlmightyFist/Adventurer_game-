import random

import pygame
from Enemy import Skeleton
from adventurer import Adventurer
from platforms import Platform


class Game(object):

    def __init__(self):
        pygame.init()

        #Obsługa głównej petli
        self.run = True

        #Ustawienia ekranu gry
        self.SCREEN_WIDTH = 500
        self.SCREEN_HEIGHT = 500
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        #Ustawienia gry
        self.PLATFORM_NUMBER = 5
        self.SKELETON_NUMBER = 4

        #Zegar
        self.clock = pygame.time.Clock()

        #Tworzenie instancji gracza
        self.player = Adventurer(250,250, self.screen,self.SCREEN_WIDTH, self.SCREEN_HEIGHT )

        #Zmienna do obsługi kolizji gracza z wrogiem
        self.hit_delay = 0

        #Tworzenie grup sprite
        self.all_sprites = pygame.sprite.Group()
        self.all_platforms = pygame.sprite.Group()
        self.all_enemies = pygame.sprite.Group()

        #Platformy startowe
        self.PLATFORM_LIST = [(0,self.SCREEN_HEIGHT - 40,self.SCREEN_WIDTH, 40),
                         (300, 430, 100, 10),
                         (100, 400, 100, 10),
                         (430,350,100,10),
                         (150, 270,100,10),
                         (200,200,100,10),
                         (250, 130, 100,10),
                         (50,50,200,20)]


        #Dodawanie spritów do grup
        self.all_sprites.add(self.player)
        for plat in self.PLATFORM_LIST:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.all_platforms.add(p)

    #Obsługa eventów
    def events(self):

        # Obsługa wydarzeń
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                self.run = False


    # Aktualizacja położeń i akcji
    def update(self):

        #Platformy
        self.all_platforms.update()

        # Utrzymanie odpowiedniej ilosci wrogów na ekranie
        self.create_enemy()

        # Wrogowie
        self.all_enemies.update()

        #Sprawdzenie kolizji player-platform
        platform_hits = pygame.sprite.spritecollide(self.player,self.all_platforms, False )
        if platform_hits:
            self.player.y = platform_hits[0].rect.top - self.player.height #ustawienie gracza na platformie w przypadku kolizji
            self.player.vel[1] = 0 #usunięcie przemieszczenia pionowego

        # Przesuwanie "ekranu" w góre jeżeli gracz osiagnie 3/4 wysokości ekranu
        if self.player.rect.y <= self.SCREEN_HEIGHT /4:
            self.player.y += abs(self.player.vel[1])
            for plat in self.all_platforms:
                plat.rect.y += abs(self.player.vel[1])
                #Usunięcie platform poniżej dolnej granicy ekranu
                if plat.rect.top >= self.SCREEN_HEIGHT:
                    plat.kill()
                    self.player.score += 10 #Zwiekszenie punktacji wraz z każdą pokonaną platformą

            #Powtórzenie operacji w przypadku wrogów
            for enemy in self.all_enemies:
                enemy.rect.y += abs(self.player.vel[1])
                if enemy.rect.top >= self.SCREEN_HEIGHT:
                    enemy.kill()


        #Utrzymanie odpowieniej ilosci platform na ekranie
        while len(self.all_platforms) < self.PLATFORM_NUMBER:
            width = random.randrange(100,300)
            height = random.randrange(5,30)
            p = Platform(random.randrange(0,self.SCREEN_WIDTH - width),random.randrange(-30,-10),width,height)
            self.all_platforms.add(p)
            self.all_sprites.add(p)

        #Gracz
        self.player.update(self.all_platforms)

        #Sprawdzanie czy gracz ciagle pozostaje na ekranie "GAME OVER CONDITION"
        if self.player.rect.bottom >= self.SCREEN_HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel[1],10) #efekt spadania gracza oraz platform
                if sprite.rect.bottom < 0:
                    sprite.kill() #usuwanie obiektów opuszczających ekran
        if len(self.all_platforms) == 0:
            self.game_over_screen()

        #Sprawdzenie poziomu zycia gracza
        if self.player.health <= 0:
            self.game_over_screen()

        #Sprawdzenie kolizji gracz-wrog
        self.collision_check()

    # Tworzenie obiektów na ekranie
    def redrawGameWindow(self):

        self.screen.fill((0,0,0))
        self.all_platforms.draw(self.screen)
        self.player.draw()

        #Rysowanie przeciwników na podstawie stworzonej metody
        for enemy in self.all_enemies.sprites():
            enemy.draw()

        self.draw_text(str(self.player.score), 30, (255,0,0), self.SCREEN_WIDTH/2, 20)
        pygame.display.update()

    # Wyświetlanie tekstu
    def draw_text(self, text, size, color, x, y):
        font = pygame.font.SysFont('comicsans', size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)

    #Ekran startowy gry
    def start_screen(self):
        self.screen.fill((0,255,0))
        self.draw_text("Brave Adventurer!", 50, (0,0,255), self.SCREEN_WIDTH/2, self.SCREEN_HEIGHT/4)
        self.draw_text("Arrows to move and jump.", 40, (0,0,255),self.SCREEN_WIDTH/2,self.SCREEN_HEIGHT/2 )
        self.draw_text("Press a key to play.", 40, (0, 0, 255), self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT *3/4)
        pygame.display.flip()
        self.key_wait()


    #Oczekiwanie na wciśniecie przycisku przez gracza
    def key_wait(self):
        waiting = True
        while waiting:
            self.clock.tick(25)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.run = False
                if event.type == pygame.KEYUP:
                    waiting = False

    #Ekran końcowy rozgrywki
    def game_over_screen(self):
        self.screen.fill((255,0,0))
        self.draw_text("GAME OVER!", 100, (0,0,0),self.SCREEN_WIDTH/2,self.SCREEN_HEIGHT/2)
        pygame.display.flip()
        self.key_wait()
        self.run = False

    #Tworzenie przeciwników na planszy
    def create_enemy(self):

        #dodawanie przeciwniak jeśli jest ich mniej niż 3 na planszy
        if len(self.all_enemies) <= self.SKELETON_NUMBER - 1 :

            top_platforms = [] # lista zawierające platformy znajdujące się powyżej górnej granicy ekranu

            for plat in self.all_platforms.sprites():
                if plat.rect.y < 0 and plat.is_skeleton_on == False: #Tworzenie szkielete tylko na platformach powyżej granicy ekranu i bez szkieleta na niej
                    top_platforms.append(plat)

            if top_platforms:
                plat = random.choice(top_platforms)  #wybór losowej platformy do umieszczenia wroga



                #Pozycja wroga na planszy
                x = random.randint(plat.rect.x, plat.rect.x + plat.width)
                y = plat.rect.top - 33


                enemy = Skeleton(x, y, self.screen, plat)
                self.all_sprites.add(enemy)
                self.all_enemies.add(enemy)

                #Platforma może posiadać tylko 1 szkieleta
                plat.is_skeleton_on = True

    # Metoda sprawdzająca kolizje gracza z przeciwnikami oraz wystrzelonymi przez nich pociskami
    def collision_check(self):

        kill = False
        if pygame.sprite.spritecollide(self.player, self.all_enemies,kill):
            self.hit_delay += 1
            if self.hit_delay >= 10:
                self.player.health -= 10
                self.hit_delay = 0

