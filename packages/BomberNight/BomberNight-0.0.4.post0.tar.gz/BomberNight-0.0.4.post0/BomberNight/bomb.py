import pygame as pg
from time import time
from .utils import CAMINHO

class Bomb(pg.sprite.Sprite):
    """ Cria os objetos de bomba, controla a sua explosão e animação"""
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = pg.image.load(CAMINHO + "/images/bomba.png")
        self.image = pg.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.explosion_range = 1 
        self.start_time = time()  # pega o momento em que a bomba foi colocada
    

    def update(self):
        self.timer = time() - self.start_time
        if self.timer >= 5:
            self.explosion()
            

    def explosion(self):
        self.kill()
        

        
        
        

