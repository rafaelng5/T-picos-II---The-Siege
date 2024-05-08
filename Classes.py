import pygame
import random
import math
import Constantes
import Procedimentos
import Surfaces


class Personagem:
    #surfaces:Surfaces, startx, starty, speed
    def __init__(self, imagem, pos_x, pos_y, largura, altura, velocidade):
        #super().__init__(surfaces[0], startx, starty, 1)
        self.imagem = imagem
        self.rect = pygame.Rect(pos_x, pos_y, largura, altura)
        self.velocidade = velocidade                            
        #self.fly_cycle = surfaces
        self.animation_index = 0
        self.delay = 0
        self.jet_delay = 7
        #self.objRect.center = (startx, starty+10)  # correct positioning 
        
        #self.speed = speed      # velocidade da nave       
      
           

        
        
    def fly_animation(self):
        self.surf = self.fly_cycle[self.animation_index]        
        
        if self.animation_index < len(self.fly_cycle)-1:
            self.delay += 1
            if self.delay > self.jet_delay:
                self.animation_index += 1
                self.delay = 0
        else:
            self.animation_index = 0  

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
        
        
        
        
