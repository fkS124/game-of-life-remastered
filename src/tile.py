import pygame as pg
from pygame import Vector2
from pygame.gfxdraw import filled_polygon
from math import sqrt
from random import randint


class Tile:

    vertexes_translation = [
        Vector2(sqrt(3) / 2, 1 / 2),
        Vector2(sqrt(3) / 2, 3 / 2),
        Vector2(0, 2),
        Vector2(-sqrt(3) / 2, 3 / 2),
        Vector2(-sqrt(3) / 2, 1 / 2)
    ]
    COLOR = (0, 0, 0)

    axis = [

    ]

    def __init__(self, game_instance, pos: tuple[int, int]):

        self.game_instance = game_instance

        self.pos = pos  # coordinates of the highest vertex
        self.alive_list = [(0, 0)]

        # self.COLOR = (randint(0, 255), randint(0, 255), randint(0, 255))

    def draw(self, d_pos, scale: int = 1):
        actual_pos = Vector2(self.pos[1]*sqrt(3)/2*scale, -(self.pos[0]+self.pos[1]*0.5)*scale) + Vector2(d_pos)
        vertexes = [actual_pos + translation * scale for translation in self.vertexes_translation]
        vertexes.insert(0, actual_pos)
        filled_polygon(self.game_instance.screen, vertexes, self.COLOR)  # draw the polygon

    def next_step(self) -> bool:
        n_neighbours = self.game_instance.number_of_neighbours(self.pos)
        if n_neighbours < self.game_instance.N_STAY_ALIVE:
            return False
        elif self.game_instance.N_STAY_ALIVE <= n_neighbours < self.game_instance.N_DIE:
            return True
        else:
            return False
