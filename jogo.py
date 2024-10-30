# Inicia o jogo

import pygame
pygame.init()

# Abre a janela

window = pygame.display.set_mode((600, 300))
pygame.display.set_caption('Pokémon Beat em Up')

# Inicia assets

image = pygame.image.load('PyGame-Beat-Em-Up/assets/backgroundexemplo.jpg').convert()
image = pygame.transform.scale(image, (altura, largura))

# Loop de jogo

game = True
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        # Checagem de movimento ou ataques:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                ataque = True
            elif event.key == pygame.K_w or event.key == pygame.K_a or event.key == pygame.K_s or event.key == pygame.K_d:
                andando = True
    window.fill((0, 0, 0))  # Preenche com a cor preta
    window.blit(image, (0, 0))
    pygame.display.update() # Mostra o novo frame para o jogador
    # ----- Gera saídas
    window.fill((0, 0, 0))  # Preenche com a cor preta
    window.blit(image, (0, 0))
    pygame.display.update()  # Mostra o novo frame para o jogador
# Fecha o jogo

pygame.quit()