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

    def __init__(self, game_instance, pos: tuple[int, int], size: int):

        self.game_instance = game_instance

        self.pos = pos  # coordinates of the highest vertex
        self.size = size

    def draw(self, d_pos, scale: int = 1):
        actual_pos = Vector2(self.pos)+Vector2(d_pos)  # get the highest vertexes' coordinates
        vertexes = [actual_pos+translation*scale*self.size for translation in self.vertexes_translation]
        vertexes.insert(0, actual_pos)
        pg.draw.polygon(self.game_instance.screen, self.COLOR, vertexes)  # draw the polygon

    def next_step(self) -> bool:
        all_tiles = self.game_instance.tiles

        # get the neighbouring tiles from the tile list

        # if next generation = alive return True
        # else return False

        return True
