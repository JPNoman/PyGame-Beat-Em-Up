# Inicia o jogo e importa coisas

import pygame
pygame.init()
import random
import time
from os import path

# Define parametros

largura = 300 ## O tamanho da janela tem que ser ajustado pro tamanho certo ainda
altura = 600
fps = 60

# Abre a janela

window = pygame.display.set_mode((altura, largura))
pygame.display.set_caption('Pokémon Beat em Up')

# Inicia assets

background = pygame.image.load('PyGame-Beat-Em-Up/assets/backgroundexemplo.jpg').convert()

# Loop de jogo

game = True
while game:
    ataque = False
    andando = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        # Checagem de movimento ou ataques:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                ataque = True
            elif event.key == pygame.K_w or event.key == pygame.K_a or event.key == pygame.K_s or event.key == pygame.K_d:
                andando = True
    window.fill((255, 255, 255))
    window.blit(background, (0, 0))
    pygame.display.update()
    

# Fecha o jogo

pygame.quit()
