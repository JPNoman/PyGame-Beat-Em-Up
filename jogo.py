# Inicia o jogo e importa coisas
import pygame
pygame.init()
import random
import math
import time
from os import path

# Define parametros
largura = 900 ## O tamanho da janela tem que ser ajustado pro tamanho certo ainda
altura = 1550
fps = 60
clock = pygame.time.Clock()
altura_player = 170
largura_player = 270
altura_inimigo = 120
largura_inimigo = 310
STILL = 0
WALK = 'walk'
EXPLODE = 'explode'
ATTACK = 'attack'
BATTLE = 'battle'
DAMAGED = 'damaged'
img_dir = path.join(path.dirname(__file__), 'assets')
direita = True # Estabelece pra que lado o jogador está olhando no começo do jogo
INIT = 0
GAME = 1
QUIT = 2
# Define algumas variáveis com as cores básicas
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
state = INIT
esquerda_enemy = False

# Define o jogador

class player(pygame.sprite.Sprite):
    def __init__(self, groups, player_sheet):
        pygame.sprite.Sprite.__init__(self)
        player_sheet = pygame.transform.scale(player_sheet, (largura_player, altura_player))
        spritesheet = load_spritesheet(player_sheet, 1, 5)
        self.animations = { # Estabelece possiveis loops de animação
            STILL: spritesheet[0:4]
        }
        self.state = STILL # Estabelece estado de animação inicial
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
        self.frame_ticks = 150  # Prestar atenção nesse parametro, pode mudar a velocidade do jogo

        # Só será possível atacar uma vez a cada 500 milissegundos
        self.last_shot = pygame.time.get_ticks()
        self.shoot_ticks = 500
        self.last_ult = pygame.time.get_ticks()
        self.ult_ticks = 4000

    def update(self):
        # Verifica o tick atual.
        now = pygame.time.get_ticks()

        if direita: # Inverte a sprite se o jogador está olhando para o outro lado
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
            if not direita:
                self.image = self.animation[self.frame]
                # Atualiza os detalhes de posicionamento
                self.rect = self.image.get_rect()
                self.rect.center = center
        
        # Atualização da posição do jogador
        self.rect.x += self.speedx
        self.rect.y += self.speedy 

        # Mantem dentro da tela
        ## Esses parametros tem que ser mudados depois pra o player só ficar no chão quando a gente tiver um mapa definido
        if self.rect.right > altura:
            self.rect.right = altura
        if self.rect.left < 0:
            self.rect.left = 0 
        if self.rect.bottom > largura:
            self.rect.bottom = largura
        if self.rect.top < 0 + 500:
            self.rect.top = 0 + 500
    
    def atacar(self):
        # Verifica se pode atacar
        now = pygame.time.get_ticks()
        # Verifica quantos ticks se passaram desde o último ataque.
        elapsed_ticks = now - self.last_shot

        # Se já pode atacar novamente...
        if elapsed_ticks > self.shoot_ticks:
            # Marca o tick da nova imagem.
            self.last_shot = now
            ataque = golpe(self.assets, self.rect.bottom, self.rect.centerx - 40) ######### Mudar esses parametros do asteroide
            if direita:
                ataque = golpe(self.assets, self.rect.bottom, self.rect.centerx + 40)
            self.groups['all_sprites'].add(ataque)
            self.groups['all_attacks'].add(ataque)
            self.assets['ice.mp3'].play()
    
    def ultar(self):
        # Verifica se pode ultar
        now = pygame.time.get_ticks()
        # Verifica quantos ticks se passaram desde o último ataque.
        elapsed_ticks = now - self.last_ult

        # Se já pode atacar novamente...
        if elapsed_ticks > self.ult_ticks:
            # Marca o tick da nova imagem.
            self.last_ult = now
            ataque = ult(self.assets, self.rect.bottom, self.rect.centerx - 40) ######### Mudar esses parametros do asteroide
            if direita:
                ataque = ult(self.assets, self.rect.bottom, self.rect.centerx + 40)
            self.groups['all_sprites'].add(ataque)
            self.groups['all_attacks'].add(ataque)
            self.assets['ice.mp3'].play()

# Define um golpe básico

class golpe(pygame.sprite.Sprite):
    # Construtor da classe.
    def __init__(self, assets, bottom, centerx):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = assets['placeholder']
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

        # Coloca no lugar inicial definido em x, y do constutor
        self.rect.centerx = centerx
        self.rect.bottom = bottom
        self.speedx = 0
        self.speedy = 0

        # Grava quando o ataque é criado
        self.last_shot = pygame.time.get_ticks()
    
    def update(self):
        now = pygame.time.get_ticks()
        elapsed_ticks = now - self.last_shot
        if elapsed_ticks > 200:
            self.kill()
        self.rect.x += self.speedx
        self.rect.y += self.speedy

class ult(pygame.sprite.Sprite):
    # Construtor da classe.
    def __init__(self, assets, bottom, centerx):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = assets['ultfroslass']
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

        # Coloca no lugar inicial definido em x, y do constutor
        self.rect.centerx = centerx
        self.rect.bottom = bottom
        if direita:
            self.speedx = 10
        else:
            self.speedx = -10
        self.speedy = 0

        # Grava quando o ataque é criado
        self.last_shot = pygame.time.get_ticks()
    
    def update(self):
        now = pygame.time.get_ticks()
        elapsed_ticks = now - self.last_shot
        if elapsed_ticks > 4000:
            self.kill()
        self.rect.x += self.speedx
        self.rect.y += self.speedy


class Enemy(pygame.sprite.Sprite):
    def __init__(self, img, enemy_sheet, player):
        # Construtor da classe mãe (Sprite).
        super().__init__()

        # Carregar e redimensionar o spritesheet
        self.spritesheet = self.load_spritesheet(enemy_sheet['walk'], 1, 8)  # Ajuste para 8 frames
        self.spritesheet_bat = self.load_spritesheet(enemy_sheet['battle'], 1, 12)  # Ajuste para 12 frames
        self.spritesheet_dam = self.load_spritesheet(enemy_sheet['damaged'], 1, 5)  # Ajuste para 5 frames

        # Configuração da animação
        self.animation = {
            WALK: self.spritesheet,
            BATTLE: self.spritesheet_bat,
            DAMAGED: self.spritesheet_dam
        }
        self.state = WALK
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100  # Troca de frame a cada 100 ms (ajuste conforme necessário)

        # Inicializar a imagem e o retângulo do sprite
        self.image = self.animation[self.state][self.frame]
        self.rect = self.image.get_rect()

        # Posicionar o inimigo em uma borda aleatória
        spawn_edge = random.choice(["top", "bottom", "left", "right"])
        if spawn_edge == "top":
            self.rect.x = random.randint(0, largura - self.rect.width)
            self.rect.y = -self.rect.height
        elif spawn_edge == "bottom":
            self.rect.x = random.randint(0, largura - self.rect.width)
            self.rect.y = altura
        elif spawn_edge == "left":
            self.rect.x = -self.rect.width
            self.rect.y = random.randint(0, altura - self.rect.height)
        elif spawn_edge == "right":
            self.rect.x = largura
            self.rect.y = random.randint(0, altura - self.rect.height)

        self.speedx = 0
        self.speedy = 0
        self.player = player
        

    def load_spritesheet(self, sheet, rows, cols):
        # Função para dividir o spritesheet em uma lista de imagens
        sprites = []
        sheet_rect = sheet.get_rect()
        frame_width = sheet_rect.width // cols
        frame_height = sheet_rect.height // rows

        for row in range(rows):
            for col in range(cols):
                frame_rect = pygame.Rect(col * frame_width, row * frame_height, frame_width, frame_height)
                image = sheet.subsurface(frame_rect)
                sprites.append(image)
        return sprites

    def update(self):
        # Controle de animação
        now = pygame.time.get_ticks()

        # Seguir o jogador
        player_x, player_y = self.player.rect.centerx, self.player.rect.centery
        enemy_x, enemy_y = self.rect.centerx, self.rect.centery

        if player_x < enemy_x:
            esquerda_enemy =True
        else:
            esquerda_enemy = False

        if esquerda_enemy: # Inverte a sprite se o jogador está olhando para o outro lado
            self.image = pygame.transform.flip(self.animation[self.state][self.frame], True, False)

        if not esquerda_enemy:
            self.image = self.animation[self.state][self.frame]

        # Calcular a distância entre o inimigo e o jogador
        distance = math.sqrt((player_x - enemy_x)**2 + (player_y - enemy_y)**2)

        if distance != 0:
            # Normalizar o vetor de direção
            direction_x = (player_x - enemy_x) / distance
            direction_y = (player_y - enemy_y) / distance

            # Ajustar a velocidade
            self.speedx = direction_x * 1.5
            self.speedy = direction_y * 1.5

        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame = (self.frame + 1) % len(self.animation[self.state])
            if esquerda_enemy: # Inverte a sprite se o jogador está olhando para o outro lado
                self.image = pygame.transform.flip(self.animation[self.state][self.frame], True, False)

            if not esquerda_enemy:
                self.image = self.animation[self.state][self.frame]

        # Atualizar posição
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if distance < largura_player/2:
            self.state = BATTLE
            self.frame = 0
            self.last_update = pygame.time.get_ticks()
            self.frame_rate = 100  # Troca de frame a cada 100 ms (ajuste conforme necessário)
        else:
            self.state = WALK
            self.frame = 0
            self.last_update = pygame.time.get_ticks()
            self.frame_rate = 100  # Troca de frame a cada 100 ms (ajuste conforme necessário)

# Classe que representa uma colisão com inimigo
# Classe que representa uma colisão com inimigo
class Explosion(pygame.sprite.Sprite):
    # Construtor da classe.
    def __init__(self, center, assets, death_sheet):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)
        # Redimensiona a superfície corretamente
        death_sheet = pygame.transform.scale(death_sheet, (largura_inimigo, altura_inimigo))
        spritesheet = load_spritesheet(death_sheet, 1, 10)
        self.animations = { # Estabelece possíveis loops de animação
            EXPLODE: spritesheet[0:4]
        }
        self.state = EXPLODE
        self.animation = self.animations[self.state]
        self.frame = 0
        self.image = self.animation[self.frame]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.last_update = pygame.time.get_ticks()
        self.frame_ticks = 50  # Ajuste conforme necessário

    def update(self):
        # Controle de animação
        now = pygame.time.get_ticks()
        elapsed_ticks = now - self.last_update

        # Se já está na hora de mudar de imagem...
        if elapsed_ticks > self.frame_ticks:
            self.last_update = now
            self.frame += 1
            if self.frame >= len(self.animation):
                self.frame = 0
                self.kill()  # Remove a explosão após terminar a animação

            self.image = self.animation[self.frame]
            self.rect = self.image.get_rect(center=self.rect.center)



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

def init_screen(screen):
    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()

    # Carrega o fundo da tela inicial
    inicial = pygame.image.load('assets/inspermonpng.png').convert()
    inicial_rect = inicial.get_rect()
    inicial = pygame.transform.scale(inicial, (altura, largura))

    running = True
    while running:

        # Ajusta a velocidade do jogo.
        clock.tick(fps)

        # Processa os eventos (mouse, teclado, botão, etc).
        for event in pygame.event.get():
            # Verifica se foi fechado.
            if event.type == pygame.QUIT:
                state = QUIT
                running = False

            if event.type == pygame.KEYUP:
                state = GAME
                running = False

        # A cada loop, redesenha o fundo e os sprites
        screen.fill(BLACK)
        screen.blit(inicial, inicial_rect)

        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()

    return state

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
        ## Eu ACHO que esse for é completamente desnecessário, mas vou deixar aí caso a gente precise no futuro
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

image = pygame.image.load('assets/mapa.jpg').convert()
image = pygame.transform.scale(image, (altura, largura))

# Sons do jogo
## Atualizar com música de menu, sound effects, etc

pygame.mixer.music.load('assets/Battle!.mp3')
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(loops=-1)

# Definindo grupos de sprites e assets

groups = {}
all_sprites = pygame.sprite.Group()
all_attacks = pygame.sprite.Group()
groups['all_sprites'] = all_sprites
groups['all_attacks'] = all_attacks
assets = {}
assets['froslass'] = pygame.image.load('assets/froslass_idle.png').convert_alpha()
assets['froslass'] = pygame.transform.scale(assets['froslass'], (largura_player, altura_player)) # Tamanho do player
assets['Meowth'] = {}
assets['Meowth']["walk"] = pygame.image.load('assets/meowth_walk.png').convert_alpha()
assets['Meowth']["walk"] = pygame.transform.scale(assets['Meowth']["walk"], (largura_inimigo, altura_inimigo)) # Tamanho do inimigo
assets['Meowth']["battle"] = pygame.image.load('assets/attack.png').convert_alpha()
assets['Meowth']["battle"] = pygame.transform.scale(assets['Meowth']["battle"], (largura_inimigo, altura_inimigo)) # Tamanho do inimigo
assets['Meowth']["damaged"] = pygame.image.load('assets/damaged.png').convert_alpha()
assets['Meowth']["damaged"] = pygame.transform.scale(assets['Meowth']["damaged"], (largura_inimigo, altura_inimigo)) # Tamanho do inimigo
assets['placeholder'] = pygame.image.load('assets/placeholder.png').convert_alpha()
assets['placeholder'] = pygame.transform.scale(assets['placeholder'], (largura_player, altura_player))
assets['ice.mp3'] = pygame.mixer.Sound('assets/ice.mp3')

assets['ultfroslass'] = pygame.image.load('assets/ultfroslass.png').convert_alpha()
assets['ultfroslass'] = pygame.transform.scale(assets['ultfroslass'], (largura_player, altura_player))
assets['death'] = pygame.image.load('assets/death_effect.png').convert_alpha()
assets['death'] = pygame.transform.scale(assets['death'], (largura_inimigo, altura_inimigo)) # Tamanho da explosão

# Cria o player
jogador = player(groups, assets['froslass'])
all_sprites.add(jogador)
ataque_atual = golpe(assets,0,0)
all_attacks.add(ataque_atual)

# Cria inimigos
enemies = pygame.sprite.Group()
for _ in range(5):  # Ajusta a quantidade de inimigos
    enemy_img = assets['Meowth']  # A imagem do inimigo
    new_enemy = Enemy(enemy_img, enemy_img, jogador)  # Passando a imagem do inimigo e o jogador
    all_sprites.add(new_enemy)
    enemies.add(new_enemy)

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
                # Dependendo da tecla, altera a velocidade do jogador e ataque.
                if event.key == pygame.K_a:
                    jogador.speedx -= 6
                    ataque_atual.speedx -= 6
                    direita = False
                if event.key == pygame.K_d:
                    jogador.speedx += 6
                    ataque_atual.speedx += 6
                    direita = True
                if event.key == pygame.K_w:
                    jogador.speedy -= 6
                    ataque_atual.speedy -= 6
                if event.key == pygame.K_s:
                    jogador.speedy += 6
                    ataque_atual.speedy += 6
                if event.key == pygame.K_SPACE:
                    jogador.atacar()
                if event.key == pygame.K_ESCAPE:
                    game = False
            # Verifica se soltou alguma tecla.
            if event.type == pygame.KEYUP:
                # Dependendo da tecla, altera a velocidade do jogador e ataque.
                if event.key == pygame.K_a:
                    jogador.speedx += 6
                    ataque_atual.speedx += 6
                if event.key == pygame.K_d:
                    jogador.speedx -= 6
                    ataque_atual.speedx -= 6
                if event.key == pygame.K_w:
                    jogador.speedy += 6
                    ataque_atual.speedy += 6
                if event.key == pygame.K_s:
                    jogador.speedy -= 6
                    ataque_atual.speedy -= 6

            # Verifica se houve colisão entre tiro e meteoro
            hits = pygame.sprite.groupcollide(enemies, all_attacks, True, True)
            for meteor in hits: # As chaves são os elementos do primeiro grupo (meteoros) que colidiram com alguma bala
                # O meteoro e destruido e precisa ser recriado
                # assets['destroy_sound'].play()
                m = Enemy(assets['Meowth'], assets['Meowth'], jogador)
                all_sprites.add(m)
                enemies.add(m)

                # No lugar do meteoro antigo, adicionar uma explosão.
                explosao = Explosion(meteor.rect.center, assets, death_sheet=assets['death'])
                all_sprites.add(explosao)
                
            # Verifica se houve colisão entre nave e meteoro
            hits = pygame.sprite.spritecollide(jogador, enemies, True)
            if len(hits) > 0:
                # Toca o som da colisão
                #assets['boom_sound'].play()
                time.sleep(5) # Precisa esperar senão fecha

                game = False
    # ----- Gera saídas
    all_sprites.update()
    window.fill((0, 0, 0))  # Preenche com a cor preta 
    window.blit(image, (0, 0))
    all_sprites.draw(window)
    pygame.display.update()  # Mostra o novo frame para o jogador
    
    if state == INIT:
        state = init_screen(window)
    elif state == GAME:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
    # Só verifica o teclado se está no estado de jogo
            if game == True:
                # Verifica se apertou alguma tecla.
                if event.type == pygame.KEYDOWN:
                    # Dependendo da tecla, altera a velocidade do jogador e ataque.
                    if event.key == pygame.K_a:
                        jogador.speedx -= 5
                        direita = False
                    if event.key == pygame.K_d:
                        jogador.speedx += 5
                        direita = True
                    if event.key == pygame.K_w:
                        jogador.speedy -= 5
                    if event.key == pygame.K_s:
                        jogador.speedy += 5
                    if event.key == pygame.K_SPACE:
                        jogador.atacar()
                    if event.key == pygame.K_q:
                        jogador.ultar()
                    if event.key == pygame.K_ESCAPE:
                        game = False
                # Verifica se soltou alguma tecla.
                if event.type == pygame.KEYUP:
                    # Dependendo da tecla, altera a velocidade do jogador e ataque.
                    if event.key == pygame.K_a:
                        jogador.speedx += 5
                    if event.key == pygame.K_d:
                        jogador.speedx -= 5
                    if event.key == pygame.K_w:
                        jogador.speedy += 5
                    if event.key == pygame.K_s:
                        jogador.speedy -= 5
        # ----- Gera saídas
        all_sprites.update()
        window.fill((0, 0, 0))  # Preenche com a cor preta 
        window.blit(image, (0, 0))
        all_sprites.draw(window)
        pygame.display.update()  # Mostra o novo frame para o jogador

    
# Fecha o jogo

pygame.quit()