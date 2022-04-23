import pygame as pg
from pygame import Vector2
from pygame.gfxdraw import aapolygon
from math import sqrt

from .tile import Tile


class Game:

    neighbouring_vertexes_translation = [
        Vector2(-sqrt(3) / 2, 3 / 2),
        Vector2(sqrt(3) / 2, 3 / 2),
        Vector2(-sqrt(3), 0),
        Vector2(sqrt(3), 0),
        Vector2(-sqrt(3) / 2, - 3 / 2),
        Vector2(sqrt(3) / 2, - 3 / 2),
    ]

    def __init__(self, screen: pg.Surface):
        # get the display
        self.screen = screen
        self.W, self.H = self.screen.get_size()

        # view settings
        self.d_pos = pg.Vector2(0, 0)
        self.scale = 1
        self.size = 5

        # all the tiles
        self.tiles: list[Tile] = [Tile(self, (15, 15), self.size)]

        # mouse management
        self.dragging = False

    def draw_hexagon(self, pos: tuple[int, int]):
        actual_pos = Vector2(pos) + Vector2(self.d_pos)  # get the highest vertexes' coordinates
        vertexes = [actual_pos + translation * self.scale * self.size for translation in Tile.vertexes_translation]
        vertexes.insert(0, actual_pos)
        aapolygon(self.screen, vertexes, (0, 0, 0))

    def handle_events(self, event):
        if event.type == pg.MOUSEBUTTONUP:
            if event.button == 3:
                pass
                # add tile here
            elif event.button == 5:
                if self.scale > 1:
                    self.scale -= 1
            elif event.button == 4:
                if self.scale < 10:
                    self.scale += 1

        elif event.type == pg.MOUSEMOTION:
            if self.dragging:  # drag the screen
                self.d_pos += pg.Vector2(event.rel)

    def next_generation(self):

        # apply the rules

        pass

    def draw_grid(self):

        drawn = []
        for tile in self.tiles:
            neighbours = self.get_neighbours(tile.pos)
            for neighbour in neighbours:
                if neighbour not in drawn:
                    drawn.append(neighbour)

        for draw in drawn:
            self.draw_hexagon(tuple(draw))

    def get_neighbours(self, pos: tuple[int, int]) -> list[Vector2]:
        return [
            Vector2(pos) + translation * self.size * self.scale
            for translation in self.neighbouring_vertexes_translation
        ]

    def update(self):

        self.dragging = pg.mouse.get_pressed()[0]

        self.draw_grid()
        for tile in self.tiles:
            tile.draw(self.d_pos, self.scale)
