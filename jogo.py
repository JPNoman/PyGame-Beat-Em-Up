# Inicia o jogo

import pygame
pygame.init()

# Abre a janela

window = pygame.display.set_mode((600, 300))
pygame.display.set_caption('Pokémon Beat em Up')

# Inicia assets

background = pygame.image.load('assets/backgroundexemplo.png').convert()

# Loop de jogo

game = True
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYUP:
            game = False
    window.fill((255, 255, 255))
    window.blit(background, (0, 0))
    pygame.display.update()
    

# Fecha o jogo

pygame.quit()
