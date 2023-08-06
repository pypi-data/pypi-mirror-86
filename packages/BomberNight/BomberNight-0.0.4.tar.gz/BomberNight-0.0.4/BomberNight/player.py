import pygame as pg
from .utils import *

class Player(pg.sprite.Sprite):
    """ Cria, movimenta e anima o objeto do player """
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = pg.image.load(CAMINHO + "/images/player.png")  
        self.image = pg.transform.scale(self.image, (100, 100))  
        self.rect = pg.rect.Rect(HEIGHT//2, WIDTH//2, 100, 100)  
        self.bomb_limit = 50 

    def update(self):
        """ controla toda a movimentação do player """
        keys = pg.key.get_pressed()
        if keys[pg.K_w] or keys[pg.K_UP]:
            self.rect.y -= 5
        if keys[pg.K_s] or keys[pg.K_DOWN]:
            self.rect.y += 5
        if keys[pg.K_a] or keys[pg.K_LEFT]:
            self.rect.x -= 5
        if keys[pg.K_d] or keys[pg.K_RIGHT]:
            self.rect.x += 5
        
        # garante que o player não saia da tela
        if self.rect.top <= 42:
            self.rect.top = 42
        if self.rect.bottom >= 498:
            self.rect.bottom = 498
        if self.rect.left <= 55:
            self.rect.left = 55
        if self.rect.right >= 905:
            self.rect.right = 905
