from typing import List
from problem import SearchState
from puzzle import PuzzleState
import pygame
from pygame.locals import *

# Some Color constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BRIGHTBLUE = (0, 50, 255)
DARKTURQUOISE = (3, 54, 73)
GREEN = (0, 204, 0)

BACKGROUND_COLOR = DARKTURQUOISE
TILE_COLOR = GREEN
TEXT_COLOR = WHITE
BORDER_COLOR = BRIGHTBLUE
BASIC_FONT_SIZE = 20

# Some layout constants
TILES_PER_ROW = TILES_PER_COL = 3
TILE_SIZE = 100 # In pixels
OFFSET_BETWEEN_TILES = 1
WIDTH = 640
HEIGHT = 480
BORDER_X_OFFSET = int((WIDTH - (TILES_PER_ROW * TILE_SIZE)) / 2)
BORDER_Y_OFFSET = int((HEIGHT - (TILES_PER_COL * TILE_SIZE)) / 2)

class Visualizer:

    def __init__(self, history: List[SearchState], fps=30):
        self._running = True
        self._display_surf = None
        self.size = WIDTH, HEIGHT
        self._fps = fps
        self._history = history

    # on_init calls pygame.init() that initialize all PyGame modules.
    # Then it create the main display - 640x400 window and try to use hardware acceleration. At the end this routine sets _running to True.
    def on_init(self):
        pygame.init()
        self._tile_font = pygame.font.Font('freesansbold.ttf', BASIC_FONT_SIZE)
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        pygame.display.set_caption('8-Puzzle')

    # on_event checks if Quit event happened if so sets _running to False which will break game loop.
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    # loop() compute changes in the game world like NPC's moves, player moves, AI, game score.
    def on_loop(self):
        pass

    # render() just print out on the screen graphic.
    def on_render(self, game_state):
        self._draw_board(game_state.state)
        pygame.display.flip()

    # on_cleanup call pygame.quit() that quits all PyGame modules. Anything else will be cleaned up by Python.
    def on_cleanup(self):
        pygame.quit()

    # This is basically the game loop that calls other functions to do the work.
    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        current_state = 0
        current_game_state = self._history[current_state]
        while self._running:
            for event in pygame.event.get():
                self.on_event(event)

            self.on_render(current_game_state)
            current_state += 1
            if (current_state == len(self._history)):
                # Display puzzle solved message, wait for 2-3 seconds then quit or something
                pygame.time.delay(3000)
                self._running = False
            self.on_loop()
        self.on_cleanup()

    def play(self) -> None:
        """
        Plays the visualization history of the game.
        """
        self.on_execute()

    def _get_tile_pos(self, pos_x, pos_y):
        """
        Given position of tile relative to board, returns the screen position of the tile
        """
        left = BORDER_X_OFFSET + pos_x * TILE_SIZE + pos_x * OFFSET_BETWEEN_TILES
        top = BORDER_Y_OFFSET + pos_y * TILE_SIZE + pos_y * OFFSET_BETWEEN_TILES
        return left, top

    def _draw_tile(self, pos_x, pos_y, tile):
        """
        Draws tile value at given position in the board
        """
        tile_left, tile_top = self._get_tile_pos(pos_x, pos_y)
        pygame.draw.rect(self._display_surf, TILE_COLOR, (tile_left, tile_top, TILE_SIZE, TILE_SIZE))
        text_surf = self._tile_font.render(str(tile), True, TEXT_COLOR)
        text_rect_surf = text_surf.get_rect()
        text_rect_surf.center = tile_left + int(TILE_SIZE / 2), tile_top + int(TILE_SIZE / 2)
        self._display_surf.blit(text_surf, text_rect_surf)

    def _draw_board(self, state):
        """
        Draws the board centered on the window surface
        """
        # Background color
        self._display_surf.fill(BACKGROUND_COLOR)

        # Draw each tile on the board
        for tile_x in range(len(state)):
            for tile_y in range(len(state[0])):
                if state[tile_x][tile_y] != 0:
                    self._draw_tile(tile_x, tile_y, state[tile_x][tile_y])

        # Draw border
        left, top = self._get_tile_pos(0, 0)
        width = TILES_PER_ROW * (TILE_SIZE + OFFSET_BETWEEN_TILES)
        height = TILES_PER_COL * (TILE_SIZE + OFFSET_BETWEEN_TILES)
        pygame.draw.rect(self._display_surf, BORDER_COLOR, (left, top, width, height), 4)

if __name__ == '__main__':
    puzzle_1 = [[1, 2, 3], [4, 0, 5], [7, 8, 6]]
    puzzle_2 = [[1, 2, 3], [4, 6, 0], [7, 8, 5]]
    puzzle_state_1 = PuzzleState(puzzle_1)
    puzzle_state_2 = PuzzleState(puzzle_2)
    path = [puzzle_state_1]
    # for state in path:
    #     print(state)
    Visualizer(path).play()
