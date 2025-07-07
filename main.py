import pygame
import random
import carros
from background import background
from const import WIN_WIDTH, WIN_HEIGHT
#ru 4732194
pygame.init()

menu_background = pygame.image.load("assets/fundo_menuprincipal.png")
menu_background = pygame.transform.scale(menu_background, (WIN_WIDTH, WIN_HEIGHT))
# Música do menu
pygame.mixer.music.load("assets/music.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)


def mostrar_menu():
    titulo_fonte = pygame.font.Font("assets/Pixel_Emulator.otf", 60)
    opcao_fonte = pygame.font.Font("assets/Pixel_Emulator.otf", 36)

    opcoes = ["Fácil", "Médio", "Difícil"]
    selecionado = 0

    while True:
        window.blit(menu_background, (0, 0))

        # Título do jogo
        titulo = titulo_fonte.render("Traffic Boom", True, (25, 25, 255))
        window.blit(titulo, (WIN_WIDTH // 2 - titulo.get_width() // 2, 100))

        # Opções de dificuldade
        for i, texto in enumerate(opcoes):
            cor = (0, 0, 255) if i == selecionado else (255, 255, 255)
            opcao_render = opcao_fonte.render(texto, True, cor)
            window.blit(opcao_render, (WIN_WIDTH // 2 - opcao_render.get_width() // 2, 250 + i * 50))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selecionado = (selecionado - 1) % len(opcoes)
                elif event.key == pygame.K_DOWN:
                    selecionado = (selecionado + 1) % len(opcoes)
                elif event.key == pygame.K_RETURN:
                    return opcoes[selecionado]


window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

som_batida = pygame.mixer.Sound("assets/8-bit-explosion-3-340456.wav")

FPS = 120

run = True
game_over = False

clock = pygame.time.Clock()

bg = background(window)
# Mostra o menu
dificuldade = mostrar_menu()
pygame.mixer.music.stop()
pygame.mixer.init()
pygame.mixer.music.load("assets/8bitmusic.mp3")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

# Definições de dificuldade
if dificuldade == "Fácil":
    tempo_spawn_intervalo = 1500
    intervalo_spawn_mina = 1700
    velocidade_inimigo = 2
    velocidade_mina = 4
    velocidade_fundo = 4
elif dificuldade == "Médio":
    tempo_spawn_intervalo = 900
    intervalo_spawn_mina = 1600
    velocidade_inimigo = 4
    velocidade_mina = 6
    velocidade_fundo = 6
elif dificuldade == "Difícil":
    tempo_spawn_intervalo = 500
    intervalo_spawn_mina = 1400
    velocidade_inimigo = 7
    velocidade_mina = 9
    velocidade_fundo = 9
score = 0
tempo_inicio = pygame.time.get_ticks()

# inimigos carros
inimigos_ativos = []
tempo_ultimo_spawn = pygame.time.get_ticks()

# inimigo mina
minas_ativas = []
tempo_ultimo_spawn_mina = pygame.time.get_ticks()

while run:
    clock.tick(FPS)
    agora = pygame.time.get_ticks()

    pygame.display.update()
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False
            break
    if not game_over:
        # Atualiza o score com base no tempo
        tempo_atual = pygame.time.get_ticks()
        tempo_passado = (tempo_atual - tempo_inicio) // 500  # segundos
        score = tempo_passado * 11
        bg.move(velocidade_fundo)
        keys = pygame.key.get_pressed()
        vel = 6
        if keys[pygame.K_LEFT] and carros.carro1_rect.left > 139:
            carros.carro1_rect.x -= vel
        if keys[pygame.K_RIGHT] and carros.carro1_rect.right < 709:
            carros.carro1_rect.x += vel
        hitbox_carro1 = carros.carro1_rect.inflate(-80, -20)

        # spawn de carros
        if agora - tempo_ultimo_spawn > tempo_spawn_intervalo:
            tempo_ultimo_spawn = agora
            faixas = [238, 364, 482, 598]  # principais
            # faixas = [230, 330, 360, 363, 480, 485, 598, 620]
            x = random.choice(faixas)
            img = random.choice(carros.inimigos_imgs)
            largura = img.get_width()
            # dentro da pista

            novo_inimigo = carros.Inimigos(x, -100, img, velocidade_inimigo)
            novo_inimigo.faixa = x  # adiciona o atributo faixa
            inimigos_ativos.append(novo_inimigo)
        # spawn de mina
        if agora - tempo_ultimo_spawn_mina > intervalo_spawn_mina:

            faixas = [238, 364, 482, 598]  # mesmas faixas dos carros

            # Pega todas as faixas já ocupadas por inimigos
            faixas_ocupadas = [inimigo.faixa for inimigo in inimigos_ativos]

            # Remove faixas ocupadas da lista de spawn disponíveis
            faixas_livres = [faixa for faixa in faixas if faixa not in faixas_ocupadas]

            if faixas_livres:
                x = random.choice(faixas_livres)
                minas_ativas.append(carros.Mina(x, -100, carros.mina, velocidade_mina))
                tempo_ultimo_spawn_mina = agora


        minas_ativas = [m for m in minas_ativas if m.rect.top < WIN_HEIGHT]
        inimigos_ativos = [i for i in inimigos_ativos if i.rect.top < WIN_HEIGHT]
        window.fill((0, 0, 0))
        bg.draw()
        # Movimento e desenho das minas
        for mina in minas_ativas:
            mina.move()
            mina.draw(window)

        window.blit(carros.carro1, carros.carro1_rect)
        # pygame.draw.rect(window, (255, 0, 0), hitbox_carro1, 2)
        # colisao carros
        for inimigo in inimigos_ativos:
            inimigo.move()
            inimigo.draw(window)
            if hitbox_carro1.colliderect(inimigo.hitbox):

                colidiu = True
                pygame.mixer.music.stop()
                if colidiu:
                    if not game_over:
                        som_batida.play()
                        pygame.mixer.music.stop()
                    game_over = True

    # colisão com minas
    for mina in minas_ativas:
        if hitbox_carro1.colliderect(mina.hitbox):

            colidiu = True
            pygame.mixer.music.stop()
            if colidiu:
                if not game_over:
                    som_batida.play()
                    pygame.mixer.music.stop()
                game_over = True
    if game_over:
        fonte = pygame.font.SysFont("Arial", 60, bold=True)
        texto_game_over = fonte.render("GAME OVER", True, (255, 0, 0))
        texto_restart = pygame.font.SysFont("Arial", 30).render("Pressione ENTER para reiniciar", True, (255, 255, 255))
        texto_score = pygame.font.SysFont("Arial", 40).render(f"Score: {score}", True, (255, 255, 255))

        window.blit(texto_game_over, (WIN_WIDTH // 2 - texto_game_over.get_width() // 2, WIN_HEIGHT // 2 - 50))
        window.blit(texto_restart, (WIN_WIDTH // 2 - texto_restart.get_width() // 2, WIN_HEIGHT // 2 + 20))
        window.blit(texto_score, (WIN_WIDTH // 2 - texto_score.get_width() // 2, WIN_HEIGHT // 2 + 70))

        pygame.display.update()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            # Resetando o jogo
            game_over = False
            score = 0
            tempo_inicio = pygame.time.get_ticks()
            carros.carro1_rect.centerx = WIN_WIDTH // 2
            carros.carro1_rect.bottom = WIN_HEIGHT - 50
            inimigos_ativos.clear()
            minas_ativas.clear()
            tempo_ultimo_spawn = pygame.time.get_ticks()
            tempo_ultimo_spawn_mina = pygame.time.get_ticks()
            pygame.mixer.music.play(-1)
        continue
    fonte_score = pygame.font.SysFont("Arial", 24)
    texto_score_jogo = fonte_score.render(f"Score: {score}", True, (255, 255, 255))
    window.blit(texto_score_jogo, (10, 10))
    pygame.display.update()

pygame.quit()
