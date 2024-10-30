# Inicia o jogo
import pygame
pygame.init()
window = pygame.display.set_mode((600, 300))
pygame.display.set_caption('Pokémon Bet em Up')
# Loop de jogo
game = True
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYUP:
            game = False
  window.fill((255, 255, 255))
  pygame.display.update()


# Fecha o jogo
pygame.quit()
