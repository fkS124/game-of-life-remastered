import pygame as pg
from typing import Union


class Button:

    def __init__(self,
                 dsp: pg.Surface,
                 size: tuple[int, int],
                 pos: tuple[int, int],
                 text: str,
                 font_size: int,
                 color: Union[pg.Color, tuple[int, int, int]],
                 font_color: Union[pg.Color, tuple[int, int, int]],
                 hover_color: Union[pg.Color, tuple[int, int, int]],
                 font_hv_color: Union[pg.Color, tuple[int, int, int]],
                 func: Union[None, callable],
                 args: Union[None, tuple] = None,
                 special_char: bool = False
                 ):

        # display
        self._display = dsp

        # pos = (x, y) and size = (width, height)
        self.pos = pos
        self.size = size

        # init font
        self.font = pg.font.Font(None, font_size)
        # render text
        self.text_rendered = self.font.render(text, True, font_color)
        self.hv_text_rendered = self.font.render(text, True, font_hv_color)

        # the function called on click
        self.func = func
        self.args = args

        # colors
        self._COLOR = color
        self._HV_COLOR = hover_color

    def handle_clicks(self, mouse_pos):
        if pg.Rect(self.pos, self.size).collidepoint(mouse_pos):
            if callable(self.func):
                if self.args is not None:
                    self.func(*self.args)
                else:
                    self.func()

    def render(self, mouse_pos):

        # position rect
        rect = pg.Rect(self.pos, self.size)

        if rect.collidepoint(mouse_pos):
            pg.draw.rect(self._display, self._HV_COLOR, rect, border_radius=8)
            self._display.blit(self.hv_text_rendered, self.hv_text_rendered.get_rect(center=rect.center))
        else:
            pg.draw.rect(self._display, self._COLOR, rect, border_radius=8)
            self._display.blit(self.text_rendered, self.text_rendered.get_rect(center=rect.center))
