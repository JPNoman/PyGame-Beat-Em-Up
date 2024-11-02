# Inicia o jogo

import pygame
pygame.init()

# Abre a janela

window = pygame.display.set_mode((600, 300))
pygame.display.set_caption('Pokémon Beat em Up')

image = pygame.image.load('assets/background.png').convert()
image = pygame.transform.scale(image, (600, 300))
# Loop de jogo

game = True
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYUP:
            game = False
    # window.fill((255, 255, 255))
    pygame.display.update()

    # ----- Gera saídas
    window.fill((0, 0, 0))  # Preenche com a cor preta
    window.blit(image, (0, 0))
    pygame.display.update()  # Mostra o novo frame para o jogador
# Fecha o jogo

pygame.quit()
