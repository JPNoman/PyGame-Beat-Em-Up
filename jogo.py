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
STILL = 0
img_dir = path.join(path.dirname(__file__), 'assets')
direita = False

# Define o jogador

class player(pygame.sprite.Sprite):
    def __init__(self, groups, player_sheet):
        pygame.sprite.Sprite.__init__(self)
        player_sheet = pygame.transform.scale(player_sheet, (190, 100))
        spritesheet = load_spritesheet(player_sheet, 1, 5)
        self.animations = {
            STILL: spritesheet[0:4]
        }
        self.state = STILL
        self.animation = self.animations[self.state]
        self.frame = 0
        self.image = self.animation[self.frame]
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()
        self.rect.centerx = largura 
        self.rect.bottom = altura 
        self.speedx = 0
        self.speedy = 0
        self.groups = groups
        self.assets = assets
        # Guarda o tick da primeira imagem
        self.last_update = pygame.time.get_ticks()
        # Controle de ticks de animação: troca de imagem a cada self.frame_ticks milissegundos.
        self.frame_ticks = 300

    def update(self):
        # Verifica o tick atual.
        now = pygame.time.get_ticks()

        if direita:
            self.image = pygame.transform.flip(self.animation[self.frame], True, False)

        # Verifica quantos ticks se passaram desde a ultima mudança de frame.
        elapsed_ticks = now - self.last_update

        # Se já está na hora de mudar de imagem...
        if elapsed_ticks > self.frame_ticks:

            # Marca o tick da nova imagem.
            self.last_update = now

            # Avança um quadro.
            self.frame += 1

            # Atualiza animação atual
            self.animation = self.animations[self.state]
            # Reinicia a animação caso o índice da imagem atual seja inválido
            if self.frame >= len(self.animation):
                self.frame = 0
            
            # Armazena a posição do centro da imagem
            center = self.rect.center
            # Atualiza imagem atual
            self.image = self.animation[self.frame]
            # Atualiza os detalhes de posicionamento
            self.rect = self.image.get_rect()
            self.rect.center = center
        
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

# Recebe uma imagem de sprite sheet e retorna uma lista de imagens. 
# É necessário definir quantos sprites estão presentes em cada linha e coluna.
# Essa função assume que os sprites no sprite sheet possuem todos o mesmo tamanho.
def load_spritesheet(spritesheet, rows, columns):
    # Calcula a largura e altura de cada sprite.
    sprite_width = spritesheet.get_width() // columns
    sprite_height = spritesheet.get_height() // rows
    
    # Percorre todos os sprites adicionando em uma lista.
    sprites = []
    for row in range(rows):
        for column in range(columns):
            # Calcula posição do sprite atual
            x = column * sprite_width
            y = row * sprite_height
            # Define o retângulo que contém o sprite atual
            dest_rect = pygame.Rect(x, y, sprite_width, sprite_height)

            # Cria uma imagem vazia do tamanho do sprite
            image = pygame.Surface((sprite_width, sprite_height), pygame.SRCALPHA)
            # Copia o sprite atual (do spritesheet) na imagem
            image.blit(spritesheet, (0, 0), dest_rect)
            sprites.append(image)
    return sprites

def game_screen(screen):
    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()

    # Carrega spritesheet
    player_sheet = pygame.image.load(path.join(img_dir, 'froslass_idle.png')).convert_alpha()

    # Cria Sprite do jogador
    player = player(player_sheet)
    # Cria um grupo de todos os sprites e adiciona o jogador.
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    PLAYING = 0
    DONE = 1

    state = PLAYING
    while state != DONE:
        
        # Ajusta a velocidade do jogo.
        clock.tick(fps)
        
        # Processa os eventos (mouse, teclado, botão, etc).
        for event in pygame.event.get():
            
            # Verifica se foi fechado.
            if event.type == pygame.QUIT:
                state = DONE
                
        # Depois de processar os eventos.
        # Atualiza a acao de cada sprite. O grupo chama o método update() de cada Sprite dentre dele.
        all_sprites.update()
        
        # A cada loop, redesenha o fundo e os sprites
        screen.fill(0,0,0)
        all_sprites.draw(screen)
        

        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()

# Abre a janela

window = pygame.display.set_mode((altura, largura))
pygame.display.set_caption('Pokémon Beat em Up')

# Inicia assets

image = pygame.image.load('assets/backgroundexemplo.jpg').convert()
image = pygame.transform.scale(image, (altura, largura))

# Sons do jogo

pygame.mixer.music.load('assets/Battle!.mp3')
pygame.mixer.music.set_volume(0.4)

pygame.mixer.music.play(loops=-1)

# Definindo grupos de sprites
groups = {}
all_sprites = pygame.sprite.Group()
groups['all_sprites'] = all_sprites
assets = {}
assets['froslass'] = pygame.image.load('assets/froslass_idle.png').convert_alpha()
assets['froslass'] = pygame.transform.scale(assets['froslass'], (largura_player, altura_player)) # Tamanho do player
# Cria o player

jogador = player(groups, assets['froslass'])
all_sprites.add(jogador)

# Loop de jogo

game = True
while game:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
# Só verifica o teclado se está no estado de jogo
        if game == True:
            # Verifica se apertou alguma tecla.
            if event.type == pygame.KEYDOWN:
                # Dependendo da tecla, altera a velocidade.
                if event.key == pygame.K_a:
                    jogador.speedx -= 8
                    direita = False
                if event.key == pygame.K_d:
                    jogador.speedx += 8
                    direita = True
                if event.key == pygame.K_w:
                    jogador.speedy -= 8
                if event.key == pygame.K_s:
                    jogador.speedy += 8
            # Verifica se soltou alguma tecla.
            if event.type == pygame.KEYUP:
                # Dependendo da tecla, altera a velocidade.
                if event.key == pygame.K_a:
                    jogador.speedx += 8
                if event.key == pygame.K_d:
                    jogador.speedx -= 8
                if event.key == pygame.K_w:
                    jogador.speedy += 8
                if event.key == pygame.K_s:
                    jogador.speedy -= 8
    # ----- Gera saídas
    all_sprites.update()
    window.fill((0, 0, 0))  # Preenche com a cor preta 
    window.blit(image, (0, 0))
    all_sprites.draw(window)
    pygame.display.update()  # Mostra o novo frame para o jogador
    
# Fecha o jogo

pygame.quit()