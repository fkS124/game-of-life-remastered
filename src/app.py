import pygame as pg

from .game import Game


class App:

    FPS = 60

    def __init__(self, size: tuple[int, int]):

        # initialize if not initialized yet
        if not pg.get_init():
            pg.init()

        # create screen
        self.display = pg.display.set_mode(size, pg.SCALED)
        self.W, self.H = size

        # set window's title
        pg.display.set_caption("Hexagonal Game of Life")

        # running variable
        self.running = True

        # fps management
        self.clock = pg.time.Clock()

        # game of life class
        self.game = Game(self.display)

    def _quit(self):
        self.running = False
        pg.quit()
        raise SystemExit

    def run(self):

        while self.running:

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self._quit()

                self.game.handle_events(event)

            self.display.fill((255, 255, 255))
            self.game.update()

            self.clock.tick(self.FPS)
            pg.display.update()
