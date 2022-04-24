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
        self.size = 50

        # all the tiles
        self.tiles_alive: list[Tile] = [Tile(self, (0, 0), self.size), Tile(self, (1, 1), self.size),
                                        Tile(self, (-2, 1), self.size)]
        self.neighbours = []
        for tile in self.tiles_alive:
            for i in range(6):
                if not (neighbour := Tile(self, (self.get_neighbours(tile.pos)[i]), self.size)) in (self.neighbours or self.tiles_alive):
                    self.neighbours.append(neighbour)
        self.dragging = False

    def draw_hexagon(self, pos: tuple[int, int]):
        actual_pos = (pos[1] * self.size * self.scale * sqrt(3) / 2,
                      -(pos[0] + pos[1] * 0.5) * self.size * self.scale) + self.d_pos
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

    def update_neighbours(self):
        self.neighbours = []
        for tile in self.tiles_alive:
            for i in range(6):
                if not (neighbour := Tile(self, (self.get_neighbours(tile.pos)[i]), self.size)) in (self.neighbours or self.tiles_alive):
                    self.neighbours.append(neighbour)


    def number_of_neighbours(self, pos: tuple[int, int]):
        n = 0
        for i in range(6):
            for tile in self.tiles_alive:
                if self.get_neighbours(pos)[i] == tile.pos:
                    n += 1
        return n

    def next_generation(self):

        for tile in self.tiles_alive:
            for i in range(0, 6):
                if self.number_of_neighbours(tile.pos) == 1:
                    pass
        for tile in self.neighbours:
            T = True
            if self.number_of_neighbours(tile.pos) == 3:
                for i in range(len(self.tiles_alive)):
                    if tile.pos == self.tiles_alive[i].pos:
                        T = False
                        print('AEWRHWSRTN')
            if T:
                self.tiles_alive.append(tile)
                T = True

    def draw_grid(self):
        drawn = []
        for neighbour in self.neighbours:
            if neighbour.pos not in drawn:
                drawn.append(neighbour.pos)

        for draw in drawn:
            self.draw_hexagon(tuple(draw))

    def get_neighbours(self, pos: tuple[int, int]):
        return [
            (pos[0] + 1, pos[1] + 1),
            (pos[0] + 2, pos[1] - 1),
            (pos[0] - 1, pos[1] + 2),
            (pos[0] - 2, pos[1] + 1),
            (pos[0] - 1, pos[1] - 1),
            (pos[0] + 1, pos[1] - 2),
        ]

    def update(self):
        self.dragging = pg.mouse.get_pressed()[0]
        self.draw_grid()
        for tile in self.tiles_alive:
            tile.draw(self.d_pos, self.scale)
        self.next_generation()
        self.update_neighbours()
        print(self.tiles_alive)
