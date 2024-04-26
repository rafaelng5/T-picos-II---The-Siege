import Constantes
import math
import random

def calcular_posicao_inicial():
    # Calcula a posição inicial do inimigo
    direcoes = ['esquerda', 'direita', 'cima', 'baixo']
    direcao = random.choice(direcoes)
    if direcao == 'esquerda':
        pos_x = -96
        pos_y = random.randint(204, Constantes.ALTURAJANELA - 204)
    elif direcao == 'direita':
        pos_x = Constantes.LARGURAJANELA + 96
        pos_y = random.randint(204, Constantes.ALTURAJANELA - 204)
    elif direcao == 'cima':
        pos_x = random.randint(204, Constantes.LARGURAJANELA - 204)
        pos_y = -96
    else:
        pos_x = random.randint(204, Constantes.LARGURAJANELA - 204)
        pos_y = Constantes.ALTURAJANELA + 96
    return pos_x, pos_y


def calcular_angulo(jogador, inimigo):
    delta_x = jogador.rect.centerx - inimigo.rect.centerx
    delta_y = jogador.rect.centery - inimigo.rect.centery
    return math.atan2(delta_y, delta_x)