import pygame
import random
import math
import Constantes
import Procedimentos

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
        angulo = Procedimentos.calcular_angulo(jogador, self)
        vel_x = self.velocidade * math.cos(angulo)
        vel_y = self.velocidade * math.sin(angulo)
        self.rect.x += vel_x
        self.rect.y += vel_y