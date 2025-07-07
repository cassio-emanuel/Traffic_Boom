import pygame

from background import pista

WIN_WIDTH, WIN_HEIGHT = pista.get_width(), pista.get_height()

#Mudar tamanho da imagem
def SCALE_IMAGE(img, factor):
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)
