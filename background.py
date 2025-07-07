import pygame


pista = pygame.image.load("assets/pista.png")


class background:
    def __init__(self, window):
        self.window = window
        self.pista = pista
        self.height = self.pista.get_height()

        self.rect1 = self.pista.get_rect(topleft=(0, 0))
        self.rect2 = self.pista.get_rect(topleft=(0, -self.height))

    def move(self, speed):
        self.rect1.centery += speed
        self.rect2.centery += speed
        if self.rect1.top >= self.window.get_height():
            self.rect1.bottom = self.rect2.top
        if self.rect2.top >= self.window.get_height():
            self.rect2.bottom = self.rect1.top

    def draw(self):
        self.window.blit(self.pista, self.rect1)
        self.window.blit(self.pista, self.rect2)



