# VERSION = 0.0.2 dev2

import pygame as pg

pg.init()

display = pg.display.set_mode([960, 540]) 
pg.display.set_caption("BomberNight") 

from .menu import Menu
from .game import Game, gameObjectGroup

menuGroup = pg.sprite.Group()  
gameGroup = pg.sprite.Group()  

mn = Menu(menuGroup)  
gm = Game(gameGroup)

clock = pg.time.Clock()

def run():
    while True:
        clock.tick(30) 
        if gm.running: 
            gameGroup.update()
            gameObjectGroup.update()
            gameGroup.draw(display)
            gameObjectGroup.draw(display)

        else:
            for event in pg.event.get():  
                if event.type == pg.QUIT: 
                    exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        m_pos = pg.mouse.get_pos()
                        mn.click(m_pos)
                        if mn.button == 'new_game':
                            gm.running = True
                            mn.button = False
                        
                menuGroup.update()
                menuGroup.draw(display)

        # atualiza a tela
        pg.display.update()

if __name__ == "__main__":
    run()

