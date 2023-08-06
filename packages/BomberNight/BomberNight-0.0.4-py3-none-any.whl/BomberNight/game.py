import pygame as pg

from .player import Player
from .bomb import Bomb
from .utils import *

gameObjectGroup = pg.sprite.Group() 
bombGroup = pg.sprite.Group(gameObjectGroup) 

pl = Player(gameObjectGroup)  

class Game(pg.sprite.Sprite):
    """ Esta classe controla somente a execução da partida, não a do programa em si"""
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = pg.image.load(CAMINHO + "/images/mapa.jpg")
        self.image = pg.transform.scale(self.image, (HEIGHT, WIDTH)).convert()
        self.rect = self.image.get_rect()
        self.running = False

    def update(self):
        if self.running:
            for event in pg.event.get(): 
                if event.type == pg.QUIT:
                    exit()
                if event.type == pg.KEYDOWN: 
                    if event.key == pg.K_ESCAPE:
                        self.running = False
                    if event.key == pg.K_SPACE: 
                        if pl.bomb_limit >= len(bombGroup):  # limita as bombas
                            newBomb = Bomb(gameObjectGroup, bombGroup) 
                            newBomb.rect.center = pl.rect.center  
