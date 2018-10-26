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
TILE_SIZE = 120 # In pixels
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
        self.clock = pygame.time.Clock()

    # on_init calls pygame.init() that initialize all PyGame modules.
    # Then it create the main display - 640x400 window and try to use hardware acceleration. At the end this routine sets _running to True.
    def on_init(self):
        pygame.init()
        self._tile_font = pygame.font.Font('freesansbold.ttf', BASIC_FONT_SIZE)
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        pygame.display.set_caption('Slide Puzzle Visualization')

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

    def _slide_animation(self, board, tile_curr_pos, tile_target_pos, animation_speed):
        # Save a copy of the original surface
        self._draw_board(board)
        original_surf = self._display_surf.copy()

        src_grid_x, src_grid_y = tile_curr_pos[0], tile_curr_pos[1]
        dest_grid_x, dest_grid_y = tile_target_pos[0], tile_target_pos[1]

        # Erase the tile from the original surface
        src_coord_left, src_coord_top = self._get_tile_pos(src_grid_x, src_grid_y)
        pygame.draw.rect(original_surf, BACKGROUND_COLOR, (src_coord_left, src_coord_top, TILE_SIZE, TILE_SIZE))

        # print(board[src_x][src_y])
        # Move a distance of TILE_SIZE with speed = animation_speed per iteration
        for i in range(0, TILE_SIZE, animation_speed):
            # Check for exit here
            self._display_surf.blit(original_surf, (0,0))
            self._draw_tile(src_grid_x, src_grid_y, board[src_grid_x][src_grid_y], (dest_grid_y - src_grid_y) * i, (dest_grid_x - src_grid_x) * i)
            pygame.display.flip()
            self.clock.tick(self._fps)

    def _get_moved_tile_pos(self, curr_board, next_board):
        """
        Given 2 consecutive game board (only differs by one move), returns the position of the moved tile before and after it's been moved
        """
        return (next_board.empty_pos, curr_board.empty_pos)

    # This is basically the game loop that calls other functions to do the work.
    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        self.on_render(self._history[0])
        next_board_idx = 1
        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            if next_board_idx >= len(self._history):
                # Display puzzle solved message, wait for 2-3 seconds then quit or something
                # pygame.time.delay(3000)
                # self._running = False
                pass
            else:
                moved_tile_pos, target_pos = self._get_moved_tile_pos(self._history[next_board_idx - 1], self._history[next_board_idx])
                self._slide_animation(self._history[next_board_idx - 1].state, moved_tile_pos, target_pos, animation_speed=1)
                next_board_idx += 1
            self.on_loop()
        self.on_cleanup()

    def play(self) -> None:
        """
        Plays the visualization history of the game.
        """
        self.on_execute()

    def _get_tile_pos(self, grid_x, grid_y):
        """
        Given position of tile relative to board (grid position), returns the screen position of the tile (coordinates position)
        """
        left = BORDER_X_OFFSET + grid_y * TILE_SIZE + grid_y * OFFSET_BETWEEN_TILES
        top = BORDER_Y_OFFSET + grid_x * TILE_SIZE + grid_x * OFFSET_BETWEEN_TILES
        return left, top

    def _draw_tile(self, pos_x, pos_y, tile, offset_x=0, offset_y=0):
        """
        Draws tile value at given position in the board
        """
        tile_left, tile_top = self._get_tile_pos(pos_x, pos_y)
        pygame.draw.rect(self._display_surf, TILE_COLOR, (tile_left + offset_x, tile_top + offset_y, TILE_SIZE, TILE_SIZE))
        text_surf = self._tile_font.render(str(tile), True, TEXT_COLOR)
        text_rect_surf = text_surf.get_rect()
        text_rect_surf.center = tile_left + int(TILE_SIZE / 2) + offset_x, tile_top + int(TILE_SIZE / 2) + offset_y
        self._display_surf.blit(text_surf, text_rect_surf)

    def _draw_board(self, board):
        """
        Draws the board centered on the window surface
        """
        # Background color
        self._display_surf.fill(BACKGROUND_COLOR)

        # Draw each tile on the board
        for grid_x in range(len(board)):
            for grid_y in range(len(board[0])):
                if board[grid_x][grid_y] != 0:
                    self._draw_tile(grid_x, grid_y, board[grid_x][grid_y])

        # Draw border
        left, top = self._get_tile_pos(0, 0)
        width = TILES_PER_ROW * (TILE_SIZE + OFFSET_BETWEEN_TILES)
        height = TILES_PER_COL * (TILE_SIZE + OFFSET_BETWEEN_TILES)
        pygame.draw.rect(self._display_surf, BORDER_COLOR, (left, top, width, height), 4)

def get_puzzle_states():
    return [PuzzleState([[1, 2, 3], [4, 5, 0], [6, 7, 8]]),
            PuzzleState([[1, 2, 3], [4, 0, 5], [6, 7, 8]]),
            PuzzleState([[1, 2, 3], [4, 7, 5], [6, 0, 8]]),
            PuzzleState([[1, 2, 3], [4, 7, 5], [6, 8, 0]]),
            PuzzleState([[1, 2, 3], [4, 7, 0], [6, 8, 5]]),
            # PuzzleState([[1, 2, 0], [4, 7, 3], [6, 8, 5]]),
            ]

if __name__ == '__main__':
    path = get_puzzle_states()
    # for state in path:
    #     print(state)
    Visualizer(path).play()
