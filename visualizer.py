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
YELLOW_2048 = (237, 197, 63)
BACKGROUND_2048 = (187, 173, 160)
# TILE_2048 = (205, 193, 180)

BACKGROUND_COLOR = BACKGROUND_2048
TILE_COLOR = YELLOW_2048
TEXT_COLOR = WHITE
BORDER_COLOR = BRIGHTBLUE
BASIC_FONT_SIZE = 20

# Some layout constants
TILE_SIZE = 80 # In pixels
BORDER_WIDTH = 1
OFFSET_BETWEEN_TILES = 8

class Visualizer:

    def __init__(self, history: List[SearchState], fps=45):
        self._running = True
        self._display_surf = None
        self._fps = fps
        self._history = history
        self.clock = pygame.time.Clock()

        self._tiles_per_row = len(history[0].state[0])
        self._tiles_per_col = len(history[0].state)
        self._width = 2 * TILE_SIZE * 2 + self._tiles_per_row * TILE_SIZE + self._tiles_per_row * OFFSET_BETWEEN_TILES + BORDER_WIDTH
        self._height = 1 * TILE_SIZE * 2 + self._tiles_per_col * TILE_SIZE + self._tiles_per_col * OFFSET_BETWEEN_TILES + BORDER_WIDTH
        print(self._width)
        print(self._height)
        self._border_x_offset = int((self._width - (self._tiles_per_row * TILE_SIZE)) / 2)
        self._border_y_offset = int((self._height - (self._tiles_per_col * TILE_SIZE)) / 2)

    def on_init(self):
        pygame.init()
        self._tile_font = pygame.font.Font('freesansbold.ttf', BASIC_FONT_SIZE)
        self._display_surf = pygame.display.set_mode((self._width, self._height), pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        pygame.display.set_caption('Slide Puzzle Visualization')

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):
        pass

    def on_render(self, game_state, msg):
        self._draw_board(game_state.state, msg)
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def _slide_animation(self, board, tile_curr_pos, tile_target_pos, animation_speed):
        # Save a copy of the original surface
        self._draw_board(board, "Solving puzzle...")
        original_surf = self._display_surf.copy()

        src_grid_x, src_grid_y = tile_curr_pos[0], tile_curr_pos[1]
        dest_grid_x, dest_grid_y = tile_target_pos[0], tile_target_pos[1]

        # Erase the tile from the original surface
        src_coord_left, src_coord_top = self._get_tile_pos(src_grid_x, src_grid_y)
        pygame.draw.rect(original_surf, BACKGROUND_COLOR, (src_coord_left, src_coord_top, TILE_SIZE, TILE_SIZE))

        # print(board[src_x][src_y])
        # Move a distance of TILE_SIZE with speed = animation_speed per iteration
        for i in range(0, TILE_SIZE + animation_speed, animation_speed):
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

        self.on_render(self._history[0], "Solving puzzle...")
        next_board_idx = 1
        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            if next_board_idx >= len(self._history):
                self.on_render(self._history[-1], "Puzzle Solved!")
                # Display puzzle solved message, wait for 2-3 seconds then quit or something
                # pygame.time.delay(3000)
                # self._running = False
                pass
            else:
                moved_tile_pos, target_pos = self._get_moved_tile_pos(self._history[next_board_idx - 1], self._history[next_board_idx])
                self._slide_animation(self._history[next_board_idx - 1].state, moved_tile_pos, target_pos, animation_speed=int(TILE_SIZE / 12))
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
        left = self._border_x_offset + grid_y * TILE_SIZE + grid_y * OFFSET_BETWEEN_TILES
        top = self._border_y_offset + grid_x * TILE_SIZE + grid_x * OFFSET_BETWEEN_TILES
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

    def _draw_board(self, board, msg=None):
        """
        Draws the board centered on the window surface
        """
        # Background color
        self._display_surf.fill(BACKGROUND_COLOR)

        if msg:
            text_surf = self._tile_font.render(msg, True, TEXT_COLOR)
            text_rect_surf = text_surf.get_rect()
            text_rect_surf.topleft = 10, 10
            self._display_surf.blit(text_surf, text_rect_surf)
        # Draw border
        left, top = self._get_tile_pos(0, 0)
        width = self._tiles_per_row * (TILE_SIZE + OFFSET_BETWEEN_TILES)
        height = self._tiles_per_col * (TILE_SIZE + OFFSET_BETWEEN_TILES)
        pygame.draw.rect(self._display_surf, BACKGROUND_COLOR, (left, top, width, height))

        # Draw each tile on the board
        for grid_x in range(len(board)):
            for grid_y in range(len(board[0])):
                if board[grid_x][grid_y] != 0:
                    self._draw_tile(grid_x, grid_y, board[grid_x][grid_y])



def get_puzzle_states():
    return [PuzzleState([[1, 2, 3], [4, 5, 0], [6, 7, 8]]),
            PuzzleState([[1, 2, 3], [4, 0, 5], [6, 7, 8]]),
            PuzzleState([[1, 2, 3], [4, 7, 5], [6, 0, 8]]),
            PuzzleState([[1, 2, 3], [4, 7, 5], [6, 8, 0]]),
            PuzzleState([[1, 2, 3], [4, 7, 0], [6, 8, 5]]),
            PuzzleState([[1, 2, 0], [4, 7, 3], [6, 8, 5]]),
            ]

if __name__ == '__main__':
    path = get_puzzle_states()
    # for state in path:
    #     print(state)
    Visualizer(path).play()
