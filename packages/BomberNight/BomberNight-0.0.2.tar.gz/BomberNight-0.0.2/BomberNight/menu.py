import pygame as pg
from .utils import *

class Menu(pg.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = pg.image.load(CAMINHO + "/images/menu.jpg")
        self.image = pg.transform.scale(self.image, (HEIGHT, WIDTH))
        self.rect = self.image.get_rect()
        self.button = None

        self.newGame_img = pg.image.load(CAMINHO + "/images/inicio.png")
        self.newGame_img = pg.transform.scale(self.newGame_img, (200, 50))
        self.newGame_rect = pg.rect.Rect(400, WIDTH//2, 200, 50)
        self.image.blit(self.newGame_img, (400, WIDTH//2))

    def update(self):
        pass

    def click(self, m_pos):
        if self.newGame_rect.collidepoint(m_pos):
            self.button = "new_game"
        

class SecondaryMenu(pg.sprite.Sprite):
    """ menu de pausa de quando o jogo tá em execussão """
    def __init__(self, *groups):
        super().__init__(groups)
        self.image = pg.image.load("images/secondaryMenu.png")
        self.image = pg.transform.scale(self.image, (HEIGHT, WIDTH))
        self.rect = self.image.get_rect()
