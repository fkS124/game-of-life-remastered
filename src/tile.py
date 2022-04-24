import pygame as pg
from pygame import Vector2
from math import sqrt


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


    def __init__(self, game_instance, pos: tuple[int, int], size: int):

        self.game_instance = game_instance

        self.pos = pos  # coordinates of the highest vertex
        self.size = size
        self.alive_list = [(0, 0)]

    def draw(self, d_pos, scale: int = 1):
        actual_pos = (self.pos[1]*self.size*sqrt(3)/2*scale, -(self.pos[0]+self.pos[1]*0.5)*self.size*scale) + d_pos
        vertexes = [actual_pos + translation * scale * self.size for translation in self.vertexes_translation]
        vertexes.insert(0, actual_pos)
        pg.draw.polygon(self.game_instance.screen, self.COLOR, vertexes)  # draw the polygon

    def next_step(self) -> bool:
        all_tiles = self.game_instance.tiles

        # get the neighbouring tiles from the tile list

        # if next generation = alive return True
        # else return False

        return True
