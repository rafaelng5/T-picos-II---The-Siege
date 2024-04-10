import pygame
import random
import math
# Carregando as imagens.
imagemNave = pygame.image.load('pngegg1.png')
imagemAsteroide = pygame.image.load('pngegg (3).png ')
imagemRaio = pygame.image.load('espada.png')
imagemFundo = pygame.image.load('JOPK_Level_1_2.png')
LARGURAJANELA = 600  # largura da janela
ALTURAJANELA = 600  # altura da janela
CORTEXTO = (255, 255, 255)  # cor do texto (branca)
QPS = 40  # quadros por segundo
TAMMINIMO = 40  # tamanho mínimo do asteroide
TAMMAXIMO = 40  # tamanho máximo do asteroide
VELMINIMA = 1  # velocidade mínima do asteroide
VELMAXIMA = 8  # velocidade máxima do asteroide
ITERACOES = 6  # número de iterações antes de criar um novo asteroide
VELJOGADOR = 5  # velocidade da nave
VELASTEROIDE = 2  # velocidade dos asteroides
VELRAIO = (0, -15)  # velocidade do raio
LARGURANAVE = imagemNave.get_width()
ALTURANAVE = imagemNave.get_height()
LARGURARAIO = imagemRaio.get_width()
ALTURARAIO = imagemRaio.get_height()

def calcular_posicao_inicial():
    # Calcula a posição inicial do asteroide
    direcoes = ['esquerda', 'direita', 'cima', 'baixo']
    direcao = random.choice(direcoes)
    if direcao == 'esquerda':
        pos_x = -96
        pos_y = random.randint(204, ALTURAJANELA - 204)
    elif direcao == 'direita':
        pos_x = LARGURAJANELA + 96
        pos_y = random.randint(204, ALTURAJANELA - 204)
    elif direcao == 'cima':
        pos_x = random.randint(204, LARGURAJANELA - 204)
        pos_y = -96
    else:
        pos_x = random.randint(204, LARGURAJANELA - 204)
        pos_y = ALTURAJANELA + 96
    return pos_x, pos_y

def moverJogador(jogador, teclas, dim_janela):
    borda_esquerda = 0
    borda_superior = 0
    borda_direita = dim_janela[0]
    borda_inferior = dim_janela[1]
    if teclas['esquerda'] and jogador['objRect'].left > borda_esquerda:
        jogador['objRect'].x -= jogador['vel']
    if teclas['direita'] and jogador['objRect'].right < borda_direita:
        jogador['objRect'].x += jogador['vel']
    if teclas['cima'] and jogador['objRect'].top > borda_superior:
        jogador['objRect'].y -= jogador['vel']
    if teclas['baixo'] and jogador['objRect'].bottom < borda_inferior:
        jogador['objRect'].y += jogador['vel']

def calcular_angulo(jogador, asteroide):
    delta_x = jogador['objRect'].centerx - asteroide['objRect'].centerx
    delta_y = jogador['objRect'].centery - asteroide['objRect'].centery
    return math.atan2(delta_y, delta_x)

def moverAsteroide(asteroide, jogador):
    angulo = calcular_angulo(jogador, asteroide)
    vel_x = VELASTEROIDE * math.cos(angulo)
    vel_y = VELASTEROIDE * math.sin(angulo)
    asteroide['objRect'].x += vel_x
    asteroide['objRect'].y += vel_y

def terminar():
    pygame.quit()
    exit()

def aguardarEntrada():
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                terminar()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    terminar()
                return

def colocarTexto(texto, fonte, janela, x, y):
    objTexto = fonte.render(texto, True, CORTEXTO)
    rectTexto = objTexto.get_rect()
    rectTexto.topleft = (x, y)
    janela.blit(objTexto, rectTexto)

pygame.init()
relogio = pygame.time.Clock()
janela = pygame.display.set_mode((LARGURAJANELA, ALTURAJANELA))
pygame.display.set_caption('The siegE')

pygame.mouse.set_visible(False)
imagemFundoRedim = pygame.transform.scale(imagemFundo, (LARGURAJANELA, ALTURAJANELA))

fonte = pygame.font.Font(None, 48)

somFinal = pygame.mixer.Sound('bach-violin-concerto-in-a-minor-3-movement-bwv-1041-183738.mp3')
somRecorde =  pygame.mixer.Sound('blaster-2-81267.mp3')
somTiro =  pygame.mixer.Sound('metal-blade-slice-26-195295.mp3')
pygame.mixer.music.load('the-happy-end-of-a-vintage-western-147522.mp3')

colocarTexto('The siegE', fonte, janela, LARGURAJANELA / 5, ALTURAJANELA / 3)
colocarTexto('Pressione uma tecla para começar.', fonte, janela, LARGURAJANELA / 20 , ALTURAJANELA / 2)
pygame.display.update()
aguardarEntrada()
recorde = 0

while True:
    asteroides = []
    raios = []
    pontuacao = 0
    deve_continuar = True
    teclas = {}
    teclas['esquerda'] = teclas['direita'] = teclas['cima'] = teclas['baixo'] = False
    contador = 0
    pygame.mixer.music.play(-1, 0.0)

    posX = LARGURAJANELA / 2
    posY = ALTURAJANELA - 50
    jogador = {'objRect': pygame.Rect(posX, posY, LARGURANAVE, ALTURANAVE), 'imagem': imagemNave, 'vel': VELJOGADOR}

    while deve_continuar:
        pontuacao += 1
        if pontuacao == recorde:
            somRecorde.play()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                terminar()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    terminar()
                if evento.key == pygame.K_LEFT or evento.key == pygame.K_a:
                    teclas['esquerda'] = True
                if evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:
                    teclas['direita'] = True
                if evento.key == pygame.K_UP or evento.key == pygame.K_w:
                    teclas['cima'] = True
                if evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                    teclas['baixo'] = True
                if evento.key == pygame.K_SPACE:
                    raio = {'objRect': pygame.Rect(jogador['objRect'].centerx, jogador['objRect'].top, LARGURARAIO, ALTURARAIO),
                            'imagem': imagemRaio,
                            'vel': VELRAIO}
                    raios.append(raio)
                    somTiro.play()
            if evento.type == pygame.KEYUP:
                if evento.key == pygame.K_LEFT or evento.key == pygame.K_a:
                    teclas['esquerda'] = False
                if evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:
                    teclas['direita'] = False
                if evento.key == pygame.K_UP or evento.key == pygame.K_w:
                    teclas['cima'] = False
                if evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                    teclas['baixo'] = False
            if evento.type == pygame.MOUSEMOTION:
                centroX_jogador = jogador['objRect'].centerx
                centroY_jogador = jogador['objRect'].centery
                jogador['objRect'].move_ip(evento.pos[0] - centroX_jogador, evento.pos[1] - centroY_jogador)
            if evento.type == pygame.MOUSEBUTTONDOWN:
                raio = {'objRect': pygame.Rect(jogador['objRect'].centerx, jogador['objRect'].top, LARGURARAIO, ALTURARAIO),
                        'imagem': imagemRaio,
                        'vel': VELRAIO}
                raios.append(raio)
                somTiro.play()

        janela.blit(imagemFundoRedim, (0,0))

        colocarTexto('Pontuação: ' + str(pontuacao), fonte, janela, 10, 0)
        colocarTexto('Recorde: ' + str(recorde), fonte, janela, 10, 40)

        contador += 1
        if contador >= ITERACOES:
            contador = 0
            tamAsteroide = random.randint(TAMMINIMO, TAMMAXIMO)
            pos_x, pos_y = calcular_posicao_inicial()
            asteroide = {'objRect': pygame.Rect(pos_x, pos_y, tamAsteroide, tamAsteroide),
                         'imagem': pygame.transform.scale(imagemAsteroide, (tamAsteroide, tamAsteroide)),
                         'vel': (random.randint(-1,1), random.randint(VELMINIMA, VELMAXIMA))}
            asteroides.append(asteroide)

        for asteroide in asteroides:
            moverAsteroide(asteroide, jogador)
            janela.blit(asteroide['imagem'], asteroide['objRect'])

        for asteroide in asteroides[:]:
            topo_asteroide = asteroide['objRect'].top
            if topo_asteroide > ALTURAJANELA:
                asteroides.remove(asteroide)

        for raio in raios:
            raio['objRect'].y += raio['vel'][1]
            janela.blit(raio['imagem'], raio['objRect'])

        for raio in raios[:]:
            base_raio = raio['objRect'].bottom
            if base_raio < 0:
                raios.remove(raio)

        moverJogador(jogador, teclas, (LARGURAJANELA, ALTURAJANELA))
        janela.blit(jogador['imagem'], jogador['objRect'])

        for asteroide in asteroides[:]:
            jogadorColidiu = jogador['objRect'].colliderect(asteroide['objRect'])
            if jogadorColidiu:
                if pontuacao > recorde:
                    recorde = pontuacao
                deve_continuar = False
            for raio in raios[:]:
                raioColidiu = raio['objRect'].colliderect(asteroide['objRect'])
                if raioColidiu:
                    raios.remove(raio)
                    asteroides.remove(asteroide)

        pygame.display.update()
        relogio.tick(QPS)

    pygame.mixer.music.stop()
    somFinal.play()
    colocarTexto('GAME OVER', fonte, janela, (LARGURAJANELA / 3), (ALTURAJANELA / 3))
    colocarTexto('Pressione uma tecla para jogar.', fonte, janela, (LARGURAJANELA / 10), (ALTURAJANELA / 2))
    pygame.display.update()
    aguardarEntrada()
    somFinal.stop()
