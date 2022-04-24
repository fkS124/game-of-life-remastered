
import pygame as pg

from .game import Game
from .ui import Button


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

        # running variables
        self.running = True
        self.started = False
        self.paused = True
        self.delay_between_generations = 500
        self.last_gen_time = 0

        # fps management
        self.clock = pg.time.Clock()

        # game of life class
        self.game = Game(self.display)

        # ui
        self.buttons: list[Button] = [
            Button(self.display, (100, 40), (20, 20), "Start", 40, (0, 255, 0), (255, 255, 255), (0, 200, 0),
                   (200, 200, 200), func=self.start_generations),
            Button(self.display, (100, 40), (20, 70), "Pause", 40, (255, 0, 0), (255, 255, 255), (200, 0, 0),
                   (200, 200, 200), func=self.pause_generations),
        ]

    def _quit(self):
        self.running = False
        pg.quit()
        raise SystemExit

    def start_generations(self):
        if self.paused and not self.started:
            self.last_gen_time = pg.time.get_ticks()
            self.paused = False
            self.started = True
            self.game.next_generation()

    def pause_generations(self):
        self.paused = True
        self.started = False

    def run(self):

        while self.running:

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self._quit()

                self.game.handle_events(event)

                if event.type == pg.MOUSEBUTTONDOWN:
                    _ = [button.handle_clicks(event.pos) for button in self.buttons]

            self.display.fill((255, 255, 255))
            self.game.update()
            _ = [button.render(pg.mouse.get_pos()) for button in self.buttons]

            if self.started:
                if pg.time.get_ticks() - self.last_gen_time > self.delay_between_generations:
                    self.last_gen_time = pg.time.get_ticks()
                    self.game.next_generation()

            self.clock.tick(self.FPS)
            pg.display.update()
