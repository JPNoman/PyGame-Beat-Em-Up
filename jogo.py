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
clock = pygame.time.Clock()
altura_player = 120
largura_player = 120

# Define o jogador

class player(pygame.sprite.Sprite):
    def __init__(self, groups, assets):
        pygame.sprite.Sprite.__init__(self)
        self.image = assets['sprite_provisoria']
        self.rect = self.image.get_rect()
        self.rect.centerx = largura 
        self.rect.bottom = altura 
        self.speedx = 0
        self.speedy = 0
        self.groups = groups
        self.assets = assets

    def update(self):
        # Atualização da posição do jogador
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # Mantem dentro da tela
        ## Esses parametros tem que ser mudados depois pra o player só ficar no chão
        if self.rect.right > altura:
            self.rect.right = altura
        if self.rect.left < 0:
            self.rect.left = 0 
        if self.rect.bottom > largura:
            self.rect.bottom = largura
        if self.rect.top < 0:
            self.rect.top = 0

# Abre a janela

window = pygame.display.set_mode((altura, largura))
pygame.display.set_caption('Pokémon Beat em Up')

# Inicia assets

image = pygame.image.load('PyGame-Beat-Em-Up/assets/backgroundexemplo.jpg').convert()
image = pygame.transform.scale(image, (altura, largura))

# Sons do jogo

pygame.mixer.music.load('PyGame-Beat-Em-Up/assets/Battle!.mp3')
pygame.mixer.music.set_volume(0.4)

pygame.mixer.music.play(loops=-1)

# Definindo grupos de sprites
groups = {}
all_sprites = pygame.sprite.Group()
groups['all_sprites'] = all_sprites
assets = {}
assets['sprite_provisoria'] = pygame.image.load('PyGame-Beat-Em-Up/assets/sprite_provisoria.webp').convert()
assets['sprite_provisoria'] = pygame.transform.scale(assets['sprite_provisoria'], (largura_player, altura_player)) # Tamanho do player
# Cria o player

jogador = player(groups, assets)
all_sprites.add(jogador)

image = pygame.image.load('assets/background.png').convert()
image = pygame.transform.scale(image, (600, 300))
# Loop de jogo

game = True
while game:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYUP:
            game = False
    window.fill((255, 255, 255))
    pygame.display.update()

# Fecha o jogo

pygame.quit()