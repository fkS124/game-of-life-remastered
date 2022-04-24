import pygame as pg
from pygame import Vector2
from pygame.gfxdraw import aapolygon
from math import sqrt
from .tile import Tile
from copy import copy
from typing import Union


class Game:
    neighbouring_vertexes_translation = [
        Vector2(-sqrt(3) / 2, 3 / 2),
        Vector2(sqrt(3) / 2, 3 / 2),
        Vector2(-sqrt(3), 0),
        Vector2(sqrt(3), 0),
        Vector2(-sqrt(3) / 2, - 3 / 2),
        Vector2(sqrt(3) / 2, - 3 / 2),
    ]

    N_STAY_ALIVE = 3
    N_DIE = 5
    N_BIRTH = 2

    def __init__(self, screen: pg.Surface):
        # get the display
        self.screen = screen
        self.W, self.H = self.screen.get_size()
        self.gen = 0

        # view settings
        self.d_pos = Vector2(0, 0)
        self.scale = 10

        # all the tiles
        self.tiles_alive: list[Tile] = []
        self.pos_alive = []
        self.neighbours = []
        self.pos_neighbours = []
        for tile in self.tiles_alive:
            for i in range(6):
                if not (neighbour := self.get_neighbours(tile.pos)[i]) in (self.pos_neighbours or self.pos_alive):
                    self.neighbours.append(Tile(self, neighbour))
                    self.pos_neighbours.append(neighbour)
        self.dragging = False

    def draw_hexagon(self, pos: tuple[int, int], color: tuple[int, int, int] = (0, 0, 0)):
        actual_pos = Vector2(pos[1] * self.scale * sqrt(3) / 2,
                             -(pos[0] + pos[1] * 0.5) * self.scale) + self.d_pos
        vertexes = [actual_pos + translation * self.scale for translation in Tile.vertexes_translation]
        vertexes.insert(0, actual_pos)
        aapolygon(self.screen, vertexes, color)

    def handle_events(self, event):
        if event.type == pg.MOUSEBUTTONUP:
            if event.button == 5:
                if self.scale > 5:
                    self.scale -= 1
            elif event.button == 4:
                if self.scale < 200:
                    self.d_pos = (Vector2(pg.mouse.get_pos())+self.d_pos)/2
                    self.scale += 1

        elif event.type == pg.MOUSEMOTION:
            if self.dragging:  # drag the screen
                self.d_pos += pg.Vector2(event.rel)

        elif event.type == pg.KEYDOWN:
            if event.key == 13:
                self.next_generation()
                self.update_neighbours()

    def distance(self, x: Union[tuple[float, float], Vector2], y: Union[tuple[float, float], Vector2]) -> float:
        return (y[0] - x[0]) ** 2 + (y[1] - x[1]) ** 2

    def coordinates_to_hexagon(self, pos: tuple[int, int]):
        p0 = (-1, 0)
        searching = True
        while searching:
            searching = False
            d = self.distance((Vector2(p0[1] * sqrt(3) / 2 * self.scale,
                                       -(p0[0] + p0[1] * 0.5) * self.scale) + self.d_pos), pos)
            p = self.get_neighbours(p0)
            for i in range(6):
                d1 = self.distance((Vector2(p[i][1] * sqrt(3) / 2 * self.scale,
                                            -(p[i][0] + p[i][1] * 0.5) * self.scale) + self.d_pos), pos)
                if d1 == d:
                    break
                elif d1 < d:
                    searching = True
                    d = d1
                    p0 = p[i]
                    break
        return p0[0] + 1, p0[1]

    def update_neighbours(self):
        self.neighbours = []
        self.pos_neighbours = []
        for tile in self.pos_alive:
            new_neighbour = self.get_neighbours(tile)
            for i in range(6):
                if new_neighbour[i] not in (self.pos_alive or self.pos_neighbours):
                    self.pos_neighbours.append(new_neighbour[i])
                    self.neighbours.append(Tile(self, new_neighbour[i]))

    def number_of_neighbours(self, pos: tuple[int, int]):
        neighbours = self.get_neighbours(pos)
        return sum([neighbours[i] in self.pos_alive for i in range(6)])

    def next_generation(self):
        to_save = []
        for tile in self.tiles_alive:
            if tile.next_step() and tile.pos not in to_save:
                to_save.append(tile.pos)
        for neighbour_pos in self.pos_neighbours:
            if self.number_of_neighbours(neighbour_pos) == self.N_BIRTH and neighbour_pos not in to_save:
                to_save.append(neighbour_pos)

        self.tiles_alive = []
        self.pos_alive = []
        for pos in to_save:
            self.pos_alive.append(pos)
            self.tiles_alive.append(Tile(self, pos))
        self.update_neighbours()

        self.gen += 1
        print(len(self.tiles_alive), "generation :", self.gen)

    def draw_grid(self):
        drawn = []
        for neighbour in self.neighbours:
            if neighbour.pos not in drawn:
                drawn.append(neighbour.pos)

        for draw in drawn:
            self.draw_hexagon(tuple(draw), color=(255, 0, 0))

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

        if pg.mouse.get_pressed()[2]:
            new_coordinates = self.coordinates_to_hexagon(pg.mouse.get_pos())
            if new_coordinates not in self.pos_alive:
                self.tiles_alive.append(Tile(self, new_coordinates))
                self.pos_alive.append(new_coordinates)
                self.update_neighbours()

        for tile in self.tiles_alive:
            tile.draw(self.d_pos, self.scale)

        self.draw_grid()
        self.draw_hexagon(self.coordinates_to_hexagon(pg.mouse.get_pos()), color=(0, 255, 0))
