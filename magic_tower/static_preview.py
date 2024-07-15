import pygame
from pygame.locals import QUIT
from lega.misc import terminate
from lega.screen import scrmgr
from magic_tower import assets
from enum import Enum

WIN_WIDTH = 1280
WIN_HEIGHT = 768  # 720 cannot be divided by 64

TILE_WIDTH = 64  # 地砖的边长

N_COLS = WIN_WIDTH // TILE_WIDTH  # 一排能放多少块地砖
N_ROWS = WIN_HEIGHT // TILE_WIDTH  # 一列能放多少块地砖

screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
clock = pygame.time.Clock()
FPS = 10

class Tile(int, Enum):
    EMPTY = 0
    GRASS = 1

row = [Tile.EMPTY] * N_COLS
tiles = [row.copy() for i in range(N_ROWS)]

# 如果直接
# tiles = [ [Tile.EMPTY] * N_COLS ] * N_ROWS
# 那么下面的赋值会改变整个 1 号列的内容
tiles[0][1] = Tile.GRASS

def get_tile(tile_enum):
    match tile_enum:
        case Tile.EMPTY:
            return assets.EMPTY
        case Tile.GRASS:
            return assets.GRASS

def draw_everything():
    for i in range(N_ROWS):
        for j in range(N_COLS):
            top = i * TILE_WIDTH
            left = j * TILE_WIDTH
            tile = get_tile(tiles[i][j])
            screen.blit(tile, (left, top))

    pygame.display.update()


def main():
    draw_everything()
    while True:
        for e in pygame.event.get():
            if e.type == QUIT:
                terminate()
        
        clock.tick(FPS)
