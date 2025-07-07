import pygame
import const
from const import SCALE_IMAGE

carro1 = SCALE_IMAGE(pygame.image.load('assets/Car.png'), 0.54)
carro1_rect = carro1.get_rect()
carro1_rect.centerx = const.WIN_WIDTH // 2  # meio horizontal da tela
carro1_rect.bottom = const.WIN_HEIGHT - 50  # um pouco acima da borda inferior
hitbox_carro1 = carro1_rect.inflate(-80, -20)


class Inimigos:
    def __init__(self, x, y, image, speed):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = y
        self.hitbox = self.rect.inflate(-80, -35)

        self.speed = speed

    def move(self):
        self.rect.y += self.speed
        self.hitbox.y += self.speed

    def draw(self, window, ):
        window.blit(self.image, self.rect)
        #pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)


carro2 = SCALE_IMAGE(pygame.image.load('assets/Audi.png'), 0.5)
carro3 = SCALE_IMAGE(pygame.image.load('assets/taxi.png'), 0.5)
carro4 = SCALE_IMAGE(pygame.image.load('assets/Ambulance.png'), 0.5)
carro5 = SCALE_IMAGE(pygame.image.load('assets/Mini_truck.png'), 0.5)
carro6 = SCALE_IMAGE(pygame.image.load('assets/Police.png'), 0.5)
carro7 = SCALE_IMAGE(pygame.image.load('assets/Black_viper.png'), 0.5)

inimigos_imgs = [carro2, carro3, carro4, carro5, carro6, carro7]

mina = SCALE_IMAGE(pygame.image.load("assets/mina.png"), 0.06)


class Mina:
    def __init__(self, x, y, image, speed):
        self.image = image
        self.rect = self.image.get_rect()

        self.rect.centerx = x
        self.rect.y = y

        self.hitbox = self.rect.inflate(-0, -15)

        self.speed = speed

    def move(self):
        self.rect.y += self.speed
        self.hitbox.y += self.speed

    def draw(self, window):
        window.blit(self.image, self.rect)
