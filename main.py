import pygame
import random
import math
import Constantes
import Procedimentos
import Classes


# Carregando as imagens.
imagemPersonagem = pygame.image.load('pngegg1.png')
imagemInimigo = pygame.image.load('pngegg (3).png')
imagemEspada = pygame.image.load('espada.png')
imagemEspadaDireita = pygame.image.load('espada_direita.png')
imagemEspadaEsquerda = pygame.image.load('espada_esquerda.png')
imagemEspadaBaixo = pygame.image.load('espada_baixo.png')
imagemFundo = pygame.image.load('JOPK_Level_1_2.png')

Constantes.LARGURAPERSONAGEM = imagemPersonagem.get_width()
Constantes.ALTURAPERSONAGEM = imagemPersonagem.get_height()
Constantes.LARGURAESPADA = imagemEspada.get_width()
Constantes.ALTURAESPADA = imagemEspada.get_height()


pygame.init()
relogio = pygame.time.Clock()
janela = pygame.display.set_mode((Constantes.LARGURAJANELA, Constantes.ALTURAJANELA))
pygame.display.set_caption('The siegE')

pygame.mouse.set_visible(False)
imagemFundoRedim = pygame.transform.scale(imagemFundo, (Constantes.LARGURAJANELA, Constantes.ALTURAJANELA))

fonte = pygame.font.Font(None, 48)

somFinal = pygame.mixer.Sound('bach-violin-concerto-in-a-minor-3-movement-bwv-1041-183738.mp3')
somRecorde = pygame.mixer.Sound('blaster-2-81267.mp3')
somTiro = pygame.mixer.Sound('metal-blade-slice-26-195295.mp3')
pygame.mixer.music.load('the-happy-end-of-a-vintage-western-147522.mp3')

Procedimentos.colocarTexto('The siegE', fonte, janela, Constantes.LARGURAJANELA / 5, Constantes.ALTURAJANELA / 3)
Procedimentos.colocarTexto('Pressione uma tecla para começar.', fonte, janela, Constantes.LARGURAJANELA / 20, Constantes.ALTURAJANELA / 2)
pygame.display.update()
Procedimentos.aguardarEntrada()
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

    posX = Constantes.LARGURAJANELA / 2
    posY = Constantes.ALTURAJANELA - 50
    jogador = Classes.Personagem(imagemPersonagem, posX, posY, Constantes.LARGURAPERSONAGEM, Constantes.ALTURAPERSONAGEM, Constantes.VELJOGADOR)

    while deve_continuar:
        pontuacao += 1
        if pontuacao == recorde:
            somRecorde.play()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                Procedimentos.terminar()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    Procedimentos.terminar()
                if evento.key == pygame.K_a:
                    teclas['esquerda'] = True
                if evento.key == pygame.K_d:
                    teclas['direita'] = True
                if evento.key == pygame.K_w:
                    teclas['cima'] = True
                if evento.key == pygame.K_s:
                    teclas['baixo'] = True
                if evento.key == pygame.K_UP:
                    espada = {'objRect': pygame.Rect(jogador.rect.centerx, jogador.rect.top, Constantes.LARGURAESPADA,
                                                     Constantes.ALTURAESPADA),
                              'imagem': imagemEspada,
                              'vel': (0, -15)}
                    espadas.append(espada)
                    somTiro.play()
                if evento.key == pygame.K_RIGHT:
                    espada = {'objRect': pygame.Rect(jogador.rect.right, jogador.rect.centery, Constantes.LARGURAESPADA,
                                                     Constantes.ALTURAESPADA),
                              'imagem': imagemEspadaDireita,
                              'vel': (15, 0)}
                    espadas.append(espada)
                    somTiro.play()
                if evento.key == pygame.K_DOWN:
                    espada = {'objRect': pygame.Rect(jogador.rect.centerx, jogador.rect.bottom, Constantes.LARGURAESPADA,
                                                     Constantes.ALTURAESPADA),
                              'imagem': imagemEspadaBaixo,
                              'vel': (0, 15)}
                    espadas.append(espada)
                    somTiro.play()
                if evento.key == pygame.K_LEFT:
                    espada = {'objRect': pygame.Rect(jogador.rect.left, jogador.rect.centery, Constantes.LARGURAESPADA,
                                                     Constantes.ALTURAESPADA),
                              'imagem': imagemEspadaEsquerda, 
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

        Procedimentos.colocarTexto('Pontuação: ' + str(pontuacao), fonte, janela, 10, 0)
        Procedimentos.colocarTexto('Recorde: ' + str(recorde), fonte, janela, 10, 40)

        contador += 1
        if contador >= Constantes.ITERACOES:
            contador = 0
            tamInimigo = random.randint(Constantes.TAMMINIMO, Constantes.TAMMAXIMO)
            pos_x, pos_y = Procedimentos.calcular_posicao_inicial()
            inimigo = Classes.Inimigo(imagemInimigo, pos_x, pos_y, tamInimigo, random.randint(Constantes.VELMINIMA, Constantes.VELMAXIMA))
            inimigos.append(inimigo)

        for inimigo in inimigos:
            inimigo.mover(jogador)
            janela.blit(inimigo.imagem, inimigo.rect)

        for inimigo in inimigos[:]:
            topo_inimigo = inimigo.rect.top
            if topo_inimigo > Constantes.ALTURAJANELA:
                inimigos.remove(inimigo)

        for espada in espadas:
            espada['objRect'].x += espada['vel'][0]
            espada['objRect'].y += espada['vel'][1]
            janela.blit(espada['imagem'], espada['objRect'])

        for espada in espadas[:]:
            base_espada = espada['objRect'].bottom
            if base_espada < 0 or espada['objRect'].top > Constantes.ALTURAJANELA or espada['objRect'].right < 0 or espada[
                'objRect'].left > Constantes.LARGURAJANELA:
                espadas.remove(espada)

        jogador.mover(teclas, (Constantes.LARGURAJANELA, Constantes.ALTURAJANELA))
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
        relogio.tick(Constantes.QPS)

    pygame.mixer.music.stop()
    somFinal.play()
    Procedimentos.colocarTexto('GAME OVER', fonte, janela, (Constantes.LARGURAJANELA / 3), (Constantes.ALTURAJANELA / 3))
    Procedimentos.colocarTexto('Pressione uma tecla para jogar.', fonte, janela, (Constantes.LARGURAJANELA / 10), (Constantes.ALTURAJANELA / 2))
    pygame.display.update()
    Procedimentos.aguardarEntrada()
    somFinal.stop()
