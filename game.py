from adventure_game import Game
import pygame

game = Game()

game.start_screen()

while game.run:
    game.clock.tick(25)

    #Obsługa wydarzeń
    game.events()
    #Aktualizacja
    game.update()
    #Rysowanie
    game.redrawGameWindow()


pygame.quit()