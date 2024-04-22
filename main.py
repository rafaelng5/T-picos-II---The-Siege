import pygame
import random
import math

# Carregando as imagens.
imagemPersonagem = pygame.image.load('pngegg1.png')
imagemInimigo = pygame.image.load('pngegg (3).png')
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


class Personagem:
    def __init__(self, imagem, pos_x, pos_y, largura, altura, velocidade):
        self.imagem = imagem
        self.rect = pygame.Rect(pos_x, pos_y, largura, altura)
        self.velocidade = velocidade

    def mover(self, teclas, dim_janela):
        borda_esquerda = 0
        borda_superior = 0
        borda_direita = dim_janela[0]
        borda_inferior = dim_janela[1]
        if teclas['esquerda'] and self.rect.left > borda_esquerda:
            self.rect.x -= self.velocidade
        if teclas['direita'] and self.rect.right < borda_direita:
            self.rect.x += self.velocidade
        if teclas['cima'] and self.rect.top > borda_superior:
            self.rect.y -= self.velocidade
        if teclas['baixo'] and self.rect.bottom < borda_inferior:
            self.rect.y += self.velocidade


class Inimigo:
    def __init__(self, imagem, pos_x, pos_y, tamanho, velocidade):
        self.imagem = pygame.transform.scale(imagem, (tamanho, tamanho))
        self.rect = pygame.Rect(pos_x, pos_y, tamanho, tamanho)
        self.velocidade = velocidade

    def mover(self, jogador):
        angulo = calcular_angulo(jogador, self)
        vel_x = self.velocidade * math.cos(angulo)
        vel_y = self.velocidade * math.sin(angulo)
        self.rect.x += vel_x
        self.rect.y += vel_y


def calcular_angulo(jogador, inimigo):
    delta_x = jogador.rect.centerx - inimigo.rect.centerx
    delta_y = jogador.rect.centery - inimigo.rect.centery
    return math.atan2(delta_y, delta_x)


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
somRecorde = pygame.mixer.Sound('blaster-2-81267.mp3')
somTiro = pygame.mixer.Sound('metal-blade-slice-26-195295.mp3')
pygame.mixer.music.load('the-happy-end-of-a-vintage-western-147522.mp3')

colocarTexto('The siegE', fonte, janela, LARGURAJANELA / 5, ALTURAJANELA / 3)
colocarTexto('Pressione uma tecla para começar.', fonte, janela, LARGURAJANELA / 20, ALTURAJANELA / 2)
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
    jogador = Personagem(imagemPersonagem, posX, posY, LARGURAPERSONAGEM, ALTURAPERSONAGEM, VELJOGADOR)

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
                    espada = {'objRect': pygame.Rect(jogador.rect.centerx, jogador.rect.top, LARGURAESPADA,
                                                     ALTURAESPADA),
                              'imagem': imagemEspada,
                              'vel': (0, -15)}
                    espadas.append(espada)
                    somTiro.play()
                if evento.key == pygame.K_RIGHT:
                    espada = {'objRect': pygame.Rect(jogador.rect.right, jogador.rect.centery, LARGURAESPADA,
                                                     ALTURAESPADA),
                              'imagem': imagemEspada,
                              'vel': (15, 0)}
                    espadas.append(espada)
                    somTiro.play()
                if evento.key == pygame.K_DOWN:
                    espada = {'objRect': pygame.Rect(jogador.rect.centerx, jogador.rect.bottom, LARGURAESPADA,
                                                     ALTURAESPADA),
                              'imagem': imagemEspada,
                              'vel': (0, 15)}
                    espadas.append(espada)
                    somTiro.play()
                if evento.key == pygame.K_LEFT:
                    espada = {'objRect': pygame.Rect(jogador.rect.left, jogador.rect.centery, LARGURAESPADA,
                                                     ALTURAESPADA),
                              'imagem': imagemEspada,
                              'vel': (-15, 0)}
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

        janela.blit(imagemFundoRedim, (0, 0))

        colocarTexto('Pontuação: ' + str(pontuacao), fonte, janela, 10, 0)
        colocarTexto('Recorde: ' + str(recorde), fonte, janela, 10, 40)

        contador += 1
        if contador >= ITERACOES:
            contador = 0
            tamInimigo = random.randint(TAMMINIMO, TAMMAXIMO)
            pos_x, pos_y = calcular_posicao_inicial()
            inimigo = Inimigo(imagemInimigo, pos_x, pos_y, tamInimigo, random.randint(VELMINIMA, VELMAXIMA))
            inimigos.append(inimigo)

        for inimigo in inimigos:
            inimigo.mover(jogador)
            janela.blit(inimigo.imagem, inimigo.rect)

        for inimigo in inimigos[:]:
            topo_inimigo = inimigo.rect.top
            if topo_inimigo > ALTURAJANELA:
                inimigos.remove(inimigo)

        for espada in espadas:
            espada['objRect'].x += espada['vel'][0]
            espada['objRect'].y += espada['vel'][1]
            janela.blit(espada['imagem'], espada['objRect'])

        for espada in espadas[:]:
            base_espada = espada['objRect'].bottom
            if base_espada < 0 or espada['objRect'].top > ALTURAJANELA or espada['objRect'].right < 0 or espada[
                'objRect'].left > LARGURAJANELA:
                espadas.remove(espada)

        jogador.mover(teclas, (LARGURAJANELA, ALTURAJANELA))
        janela.blit(jogador.imagem, jogador.rect)

        for inimigo in inimigos[:]:
            jogadorColidiu = jogador.rect.colliderect(inimigo.rect)
            if jogadorColidiu:
                if pontuacao > recorde:
                    recorde = pontuacao
                deve_continuar = False
            for espada in espadas[:]:
                espadaColidiu = espada['objRect'].colliderect(inimigo.rect)
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
