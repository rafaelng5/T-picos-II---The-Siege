import pygame
import random
import math
# Carregando as imagens.
imagemPersonagem = pygame.image.load('pngegg1.png')
imagemInimigo = pygame.image.load('pngegg (3).png ')
imagemEspada = pygame.image.load('espada.png')
imagemFundo = pygame.image.load('JOPK_Level_1_2.png')
LARGURAJANELA = 600  # largura da janela
ALTURAJANELA = 600  # altura da janela
CORTEXTO = (255, 255, 255)  # cor do texto (branca)
QPS = 60  # quadros por segundo
TAMMINIMO = 40  # tamanho mínimo do inimigo
TAMMAXIMO = 40  # tamanho máximo do inimigo
VELMINIMA = 1  # velocidade mínima do inimigo
VELMAXIMA = 8  # velocidade máxima do inimigo
ITERACOES = 6  # número de iterações antes de criar um novo inimigo
VELJOGADOR = 5  # velocidade da nave
VELINIMIGO = 2  # velocidade dos inimigos
VELESPADA = (0, -15)  # velocidade do espada
LARGURAPERSONAGEM = imagemPersonagem.get_width()
ALTURAPERSONAGEM = imagemPersonagem.get_height()
LARGURAESPADA = imagemEspada.get_width()
ALTURAESPADA = imagemEspada.get_height()

def calcular_posicao_inicial():
    # Calcula a posição inicial do inimigo
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

def calcular_angulo(jogador, inimigo):
    delta_x = jogador['objRect'].centerx - inimigo['objRect'].centerx
    delta_y = jogador['objRect'].centery - inimigo['objRect'].centery
    return math.atan2(delta_y, delta_x)

def moverinimigo(inimigo, jogador):
    angulo = calcular_angulo(jogador, inimigo)
    vel_x = VELINIMIGO * math.cos(angulo)
    vel_y = VELINIMIGO * math.sin(angulo)
    inimigo['objRect'].x += vel_x
    inimigo['objRect'].y += vel_y

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
    inimigos = []
    espadas = []
    pontuacao = 0
    deve_continuar = True
    teclas = {}
    teclas['esquerda'] = teclas['direita'] = teclas['cima'] = teclas['baixo'] = False
    contador = 0
    pygame.mixer.music.play(-1, 0.0)

    posX = LARGURAJANELA / 2
    posY = ALTURAJANELA - 50
    jogador = {'objRect': pygame.Rect(posX, posY, LARGURAPERSONAGEM, ALTURAPERSONAGEM), 'imagem': imagemPersonagem, 'vel': VELJOGADOR}

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
                if evento.key == pygame.K_a:
                    teclas['esquerda'] = True
                if evento.key == pygame.K_d:
                    teclas['direita'] = True
                if evento.key == pygame.K_w:
                    teclas['cima'] = True
                if evento.key == pygame.K_s:
                    teclas['baixo'] = True
                if evento.key == pygame.K_UP:
                    espada = {'objRect': pygame.Rect(jogador['objRect'].centerx, jogador['objRect'].top, LARGURAESPADA, ALTURAESPADA),
                            'imagem': imagemEspada,
                            'vel': VELESPADA}
                    espadas.append(espada)
                    somTiro.play()
                if evento.key == pygame.K_RIGHT:
                    espada = {'objRect': pygame.Rect(jogador['objRect'].right, jogador['objRect'].centery, LARGURAESPADA, ALTURAESPADA),
                            'imagem': imagemEspada,
                            'vel': VELESPADA}
                    espadas.append(espada)
                    somTiro.play()
                if evento.key == pygame.K_DOWN:
                    espada = {'objRect': pygame.Rect(jogador['objRect'].centerx, jogador['objRect'].bottom, LARGURAESPADA, ALTURAESPADA),
                            'imagem': imagemEspada,
                            'vel': VELESPADA}
                    espadas.append(espada)
                    somTiro.play()
                if evento.key == pygame.K_LEFT:
                    espada = {'objRect': pygame.Rect(jogador['objRect'].left, jogador['objRect'].centery, LARGURAESPADA, ALTURAESPADA),
                            'imagem': imagemEspada,
                            'vel': VELESPADA}
                    espadas.append(espada)
                    somTiro.play()
                
            if evento.type == pygame.KEYUP:
                if evento.key == pygame.K_a:
                    teclas['esquerda'] = False
                if evento.key == pygame.K_d:
                    teclas['direita'] = False
                if evento.key == pygame.K_w:
                    teclas['cima'] = False
                if evento.key == pygame.K_s:
                    teclas['baixo'] = False
            
        janela.blit(imagemFundoRedim, (0,0))

        colocarTexto('Pontuação: ' + str(pontuacao), fonte, janela, 10, 0)
        colocarTexto('Recorde: ' + str(recorde), fonte, janela, 10, 40)

        contador += 1
        if contador >= ITERACOES:
            contador = 0
            tamIminigo = random.randint(TAMMINIMO, TAMMAXIMO)
            pos_x, pos_y = calcular_posicao_inicial()
            inimigo = {'objRect': pygame.Rect(pos_x, pos_y, tamIminigo, tamIminigo),
                         'imagem': pygame.transform.scale(imagemInimigo, (tamIminigo, tamIminigo)),
                         'vel': (random.randint(-1,1), random.randint(VELMINIMA, VELMAXIMA))}
            inimigos.append(inimigo)

        for inimigo in inimigos:
            moverinimigo(inimigo, jogador)
            janela.blit(inimigo['imagem'], inimigo['objRect'])

        for inimigo in inimigos[:]:
            topo_inimigo = inimigo['objRect'].top
            if topo_inimigo > ALTURAJANELA:
                inimigos.remove(inimigo)

        for espada in espadas:
                espada['objRect'].y += espada['vel'][1]
                janela.blit(espada['imagem'], espada['objRect'])
            

        for espada in espadas[:]:
            base_espada = espada['objRect'].bottom
            if base_espada < 0:
                espadas.remove(espada)

        moverJogador(jogador, teclas, (LARGURAJANELA, ALTURAJANELA))
        janela.blit(jogador['imagem'], jogador['objRect'])

        for inimigo in inimigos[:]:
            jogadorColidiu = jogador['objRect'].colliderect(inimigo['objRect'])
            if jogadorColidiu:
                if pontuacao > recorde:
                    recorde = pontuacao
                deve_continuar = False
            for espada in espadas[:]:
                espadaColidiu = espada['objRect'].colliderect(inimigo['objRect'])
                if espadaColidiu:
                    espadas.remove(espada)
                    inimigos.remove(inimigo)

        pygame.display.update()
        relogio.tick(QPS)

    pygame.mixer.music.stop()
    somFinal.play()
    colocarTexto('GAME OVER', fonte, janela, (LARGURAJANELA / 3), (ALTURAJANELA / 3))
    colocarTexto('Pressione uma tecla para jogar.', fonte, janela, (LARGURAJANELA / 10), (ALTURAJANELA / 2))
    pygame.display.update()
    aguardarEntrada()
    somFinal.stop()
