import numpy as np
import pygame
import sys
import math

BLUE_COLOR = (0, 0, 255)
BLACK_COLOR = (0, 0, 0)
RED_COLOR = (255, 0, 0)
YELLOW_COLOR = (255, 255, 0)

NUM_ROWS = 6
NUM_COLUMNS = 7

def create_board():
    board = np.zeros((NUM_ROWS, NUM_COLUMNS))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[NUM_ROWS - 1][col] == 0

def get_next_open_row(board, col):
    for r in range(NUM_ROWS):
        if board[r][col] == 0:
            return r

def print_board(board):
    print(np.flip(board, 0))

def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(NUM_COLUMNS - 3):
        for r in range(NUM_ROWS):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                return True

    # Check vertical locations for win
    for c in range(NUM_COLUMNS):
        for r in range(NUM_ROWS - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                return True

    # Check positively sloped diagonals
    for c in range(NUM_COLUMNS - 3):
        for r in range(NUM_ROWS - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(NUM_COLUMNS - 3):
        for r in range(3, NUM_ROWS):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                return True

def draw_board(board):
    for c in range(NUM_COLUMNS):
        for r in range(NUM_ROWS):
            pygame.draw.rect(screen, BLUE_COLOR, (c * SQUARE_SIZE, r * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, BLACK_COLOR, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), int(r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)

    for c in range(NUM_COLUMNS):
        for r in range(NUM_ROWS):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED_COLOR, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), height - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW_COLOR, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), height - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
    pygame.display.update()

board = create_board()
print_board(board)
game_over = False
turn = 0

pygame.init()

SQUARE_SIZE = 100

width = NUM_COLUMNS * SQUARE_SIZE
height = (NUM_ROWS + 1) * SQUARE_SIZE

size = (width, height)

RADIUS = int(SQUARE_SIZE / 2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK_COLOR, (0, 0, width, SQUARE_SIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED_COLOR, (posx, int(SQUARE_SIZE / 2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW_COLOR, (posx, int(SQUARE_SIZE / 2)), RADIUS)
            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK_COLOR, (0, 0, width, SQUARE_SIZE))
            if turn == 0:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARE_SIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)

                    if winning_move(board, 1):
                        label = myfont.render("Player 1 wins!!", 1, RED_COLOR)
                        screen.blit(label, (40, 10))
                        game_over = True

            else:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARE_SIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)

                    if winning_move(board, 2):
                        label = myfont.render("Player 2 wins!!", 1, YELLOW_COLOR)
                        screen.blit(label, (40, 10))
                        game_over = True

            print_board(board)
            draw_board(board)

            turn += 1
            turn = turn % 2

            if game_over:
                pygame.time.wait(3000)
