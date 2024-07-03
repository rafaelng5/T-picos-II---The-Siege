import pygame
from pygame import Surface

class Surfaces():
    def __init__(self, disp_size):
        self.surf_ship = pygame.image.load('Sprites\personagem-cima-3.png')

        self.exp_seq = pygame.image.load('Sprites\pngegg (3).png').convert_alpha()
        self.surf_asteroids = self.get_sub_surfs(self.exp_seq, 66, 194, (58, 61), (65, 0), 3)

        # Verificação de limites para surf_fire
        if (198 < 0 or 72 < 0 or
            198 + 4 > self.exp_seq.get_width() or
            72 + 8 > self.exp_seq.get_height()):
            print("Erro: Coordenadas ou dimensões inválidas para subsuperfície")
   
            self.surf_fire = None
        else:
            self.surf_fire = self.exp_seq.subsurface((198, 72), (4, 8))
            self.surf_fire = pygame.transform.rotozoom(self.surf_fire, 0, 3)

        print("Dimensões da superfície original:", self.exp_seq.get_width(), "x", self.exp_seq.get_height())
        print("Coordenadas para surf_rocket:", (173, 48))
        print("Dimensões para surf_rocket:", (6, 12))

        self.surf_rocket = self.exp_seq.subsurface((173, 48), (6, 12))
        self.surf_rocket = pygame.transform.rotozoom(self.surf_rocket, 0, 3)

        self.surf_jets = self.get_sub_surfs(self.exp_seq, 71, 15, (18, 17), (32, 0), 4)

        sub1 = self.exp_seq.subsurface((200, 5), (16, 24))
        sub1 = pygame.transform.rotozoom(sub1, 180, 2)
        sub2 = self.exp_seq.subsurface((8, 197), (48, 52))
        sub3 = self.exp_seq.subsurface((207, 144), (36, 35))
        sub4 = self.exp_seq.subsurface((151, 151), (17, 18))
        sub5 = self.exp_seq.subsurface((92, 156), (8, 8))
        self.surf_enemy1 = [sub1, sub2, sub3, sub4, sub5]

        self.surf_asteroids.insert(1, sub2)

          
        
    def get_sub_surfs(self, surf:Surface, top, left, width_height, offset_next, times):
        list = []
        for i in range(times):
            if (top < 0 or left < 0 or 
            top + width_height[0] > surf.get_width() or 
            left + width_height[1] > surf.get_height()):
            # Tratar o caso de coordenadas ou dimensões inválidas aqui
            # Por exemplo, você pode imprimir uma mensagem de erro
                print("Erro: Coordenadas ou dimensões inválidas para subsuperfície")
                return None
            #print(top, left, width_height)
            list.append(surf.subsurface((top,left), width_height))
            top = top + offset_next[0]
            left = left + offset_next[1]
        return list
