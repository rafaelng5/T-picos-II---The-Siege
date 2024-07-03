import pygame
import random
import Constantes
import Procedimentos
import Classes
import LoadImages
import LoadSoud
import customtkinter as ctk
from PIL import Image, ImageTk

# Variáveis globais para volumes e pontuações
volume_musica = 0.5
volume_efeitos = 0.5
pontuacoes = []

# Função para iniciar o jogo
def iniciar_jogo():
    global pontuacoes
    Constantes.LARGURAPERSONAGEM = LoadImages.imagemPersonagem.get_width()
    Constantes.ALTURAPERSONAGEM = LoadImages.imagemPersonagem.get_height()
    Constantes.LARGURAESPADA = LoadImages.imagemEspada.get_width()
    Constantes.ALTURAESPADA = LoadImages.imagemEspada.get_height()

    pygame.init()
    relogio = pygame.time.Clock()
    janela = pygame.display.set_mode((Constantes.LARGURAJANELA, Constantes.ALTURAJANELA))
    pygame.display.set_caption('The SiegE')

    pygame.mouse.set_visible(False)
    imagemFundoRedim = pygame.transform.scale(LoadImages.imagemFundo, (Constantes.LARGURAJANELA, Constantes.ALTURAJANELA))

    fonte = pygame.font.Font(None, 48)

    pygame.mixer.music.load('Sons\\the-happy-end-of-a-vintage-western-147522.mp3')
    pygame.mixer.music.set_volume(volume_musica)
    Procedimentos.colocarTexto('The SiegE', fonte, janela, Constantes.LARGURAJANELA / 5, Constantes.ALTURAJANELA / 3)
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
        
        jogador = Classes.Personagem(LoadImages.imagemPersonagem, posX, posY, Constantes.LARGURAPERSONAGEM, Constantes.ALTURAPERSONAGEM, Constantes.VELJOGADOR)
        
        while deve_continuar:
            pontuacao += 1
            if pontuacao == recorde:
                LoadSoud.somRecorde.play()
                LoadSoud.somRecorde.set_volume(volume_efeitos)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    Procedimentos.terminar()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        mostrar_pausa(janela)
                    if evento.key == pygame.K_a:
                        teclas['esquerda'] = True
                    if evento.key == pygame.K_d:
                        teclas['direita'] = True
                    if evento.key == pygame.K_w:
                        teclas['cima'] = True
                    if evento.key == pygame.K_s:
                        teclas['baixo'] = True
                    if evento.key == pygame.K_UP:
                        espada = {'objRect': pygame.Rect(jogador.rect.centerx - 32, jogador.rect.top - 50, Constantes.LARGURAESPADA,
                                                        Constantes.ALTURAESPADA),
                                'imagem': LoadImages.imagemEspada,
                                'vel': (0, -15)}
                        espadas.append(espada)
                        LoadSoud.somTiro.play()
                        LoadSoud.somTiro.set_volume(volume_efeitos)
                    if evento.key == pygame.K_RIGHT:
                        espada = {'objRect': pygame.Rect(jogador.rect.right - 20, jogador.rect.centery - 30, Constantes.LARGURAESPADA,
                                                        Constantes.ALTURAESPADA),
                                'imagem': LoadImages.imagemEspadaDireita,
                                'vel': (15, 0)}
                        espadas.append(espada)
                        LoadSoud.somTiro.play()
                        LoadSoud.somTiro.set_volume(volume_efeitos)
                    if evento.key == pygame.K_DOWN:
                        espada = {'objRect': pygame.Rect(jogador.rect.centerx - 32, jogador.rect.bottom - 15, Constantes.LARGURAESPADA,
                                                        Constantes.ALTURAESPADA),
                                'imagem': LoadImages.imagemEspadaBaixo,
                                'vel': (0, 15)}
                        espadas.append(espada)
                        LoadSoud.somTiro.play()
                        LoadSoud.somTiro.set_volume(volume_efeitos)
                    if evento.key == pygame.K_LEFT:
                        espada = {'objRect': pygame.Rect(jogador.rect.left - 35, jogador.rect.centery - 30, Constantes.LARGURAESPADA,
                                                        Constantes.ALTURAESPADA),
                                'imagem': LoadImages.imagemEspadaEsquerda, 
                                'vel': (-15, 0)}
                        espadas.append(espada)
                        LoadSoud.somTiro.play()
                        LoadSoud.somTiro.set_volume(volume_efeitos)

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
                inimigo = Classes.Inimigo(LoadImages.imagemInimigo, pos_x, pos_y, tamInimigo, random.randint(Constantes.VELMINIMA, Constantes.VELMAXIMA))
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
        LoadSoud.somFinal.play()
        LoadSoud.somFinal.set_volume(volume_efeitos)
        pontuacoes.append(pontuacao)
        pontuacoes = sorted(pontuacoes, reverse=True)[:5]  # Mantém apenas as 5 melhores pontuações
        Procedimentos.colocarTexto('GAME OVER', fonte, janela, (Constantes.LARGURAJANELA / 3), (Constantes.ALTURAJANELA / 3))
        Procedimentos.colocarTexto('Pressione uma tecla para jogar.', fonte, janela, (Constantes.LARGURAJANELA / 10), (Constantes.ALTURAJANELA / 2))
        pygame.display.update()
        Procedimentos.aguardarEntrada()
        LoadSoud.somFinal.stop()

def sair_jogo():
    root.quit()



def mostrar_pausa(janela):
    fonte = pygame.font.Font(None, 48)
    Procedimentos.colocarTexto('PAUSE', fonte, janela, (Constantes.LARGURAJANELA / 2.5), (Constantes.ALTURAJANELA / 3))
    Procedimentos.colocarTexto('Pressione ESC para continuar.', fonte, janela, (Constantes.LARGURAJANELA / 8), (Constantes.ALTURAJANELA / 2))
    Procedimentos.colocarTexto('Pressione Q para voltar ao menu.', fonte, janela, (Constantes.LARGURAJANELA / 8), (Constantes.ALTURAJANELA / 1.5))
    pygame.display.update()
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return
                if evento.key == pygame.K_q:
                    pygame.quit()
                    return

def abrir_configuracoes():
    global volume_musica, volume_efeitos

    config_window = ctk.CTkToplevel(root)
    config_window.title('Configurações')
    config_window.geometry('400x300')
    config_window.grab_set()  # Torna a janela modal
    config_window.lift()  # Traz a janela à frente

    def voltar_menu():
        config_window.destroy()

    # Slider para ajustar o volume da música
    volume_musica_label = ctk.CTkLabel(config_window, text="Volume da Música")
    volume_musica_label.pack(pady=10)

    volume_musica_slider = ctk.CTkSlider(config_window, from_=0, to=1, command=ajustar_volume_musica)
    volume_musica_slider.set(volume_musica)
    volume_musica_slider.pack(pady=10)

    # Slider para ajustar o volume dos efeitos sonoros
    volume_efeitos_label = ctk.CTkLabel(config_window, text="Volume dos Efeitos Sonoros")
    volume_efeitos_label.pack(pady=10)

    volume_efeitos_slider = ctk.CTkSlider(config_window, from_=0, to=1, command=ajustar_volume_efeitos)
    volume_efeitos_slider.set(volume_efeitos)
    volume_efeitos_slider.pack(pady=10)

    # Botão para voltar ao menu principal
    botao_voltar = ctk.CTkButton(config_window, text='Voltar', command=voltar_menu)
    botao_voltar.pack(pady=20)

def ajustar_volume_musica(valor):
    global volume_musica
    volume_musica = float(valor)
    pygame.mixer.music.set_volume(volume_musica)

def ajustar_volume_efeitos(valor):
    global volume_efeitos
    volume_efeitos = float(valor)

def exibir_pontuacoes():
    pontuacoes_window = ctk.CTkToplevel(root)
    pontuacoes_window.title('Pontuações')
    pontuacoes_window.geometry('400x300')
    pontuacoes_window.grab_set()  # Torna a janela modal
    pontuacoes_window.lift()  # Traz a janela à frente

    def voltar_menu():
        pontuacoes_window.destroy()

    pontuacoes_label = ctk.CTkLabel(pontuacoes_window, text="Melhores Pontuações", font=("arial", 20))
    pontuacoes_label.pack(pady=10)

    for idx, pontuacao in enumerate(pontuacoes, start=1):
        pontuacao_label = ctk.CTkLabel(pontuacoes_window, text=f"{idx}. {pontuacao}")
        pontuacao_label.pack(pady=5)

    botao_voltar = ctk.CTkButton(pontuacoes_window, text='Voltar', command=voltar_menu)
    botao_voltar.pack(pady=20)

# Configuração da janela do menu com customtkinter
root = ctk.CTk()
root.title('Menu do Jogo')
root.geometry('1000x1000')

# Carregar e exibir uma imagem com PIL
imagem = Image.open('Imagens\\fundo.jpg')
imagem = imagem.resize((520, 400), Image.LANCZOS)
photo = ImageTk.PhotoImage(imagem)
label_imagem = ctk.CTkLabel(root, font=("arial", 48), text="The SiegE", image=photo)
label_imagem.pack(pady=20)

# Botões do menu
botao_iniciar = ctk.CTkButton(root, text='Iniciar Jogo', command=iniciar_jogo)
botao_iniciar.pack(pady=10)

botao_configuracoes = ctk.CTkButton(root, text='Configurações', command=abrir_configuracoes)
botao_configuracoes.pack(pady=10)

botao_pontuacoes = ctk.CTkButton(root, text='Pontuações', command=exibir_pontuacoes)
botao_pontuacoes.pack(pady=10)

botao_sair = ctk.CTkButton(root, text='Sair', command=sair_jogo)
botao_sair.pack(pady=10)

root.mainloop()
