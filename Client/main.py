import socket
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


def create_client_socket():
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Define the server address and port
    server_address = ('127.0.0.1', 3000)

    # Connect the socket to the server
    client_socket.connect(server_address)

    return client_socket

def draw_board(board, screen, SQUARE_SIZE, RADIUS, height):
    for c in range(NUM_COLUMNS):
        for r in range(NUM_ROWS):
            pygame.draw.rect(screen, BLUE_COLOR, (c * SQUARE_SIZE, r * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, BLACK_COLOR, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), int(r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)

    for c in range(NUM_COLUMNS):
        for r in reversed(range(NUM_ROWS)):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED_COLOR, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), height - int((NUM_ROWS - r - 1) * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW_COLOR, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), height - int((NUM_ROWS - r - 1) * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
    pygame.display.update()

def get_board(board_str):
    rows = board_str.split('\n')
    return [[int(cell) for cell in row.split(' ') if cell] for row in rows if row]
 
def main():

    pygame.init()

    SQUARE_SIZE = 100
    width = NUM_COLUMNS * SQUARE_SIZE
    height = (NUM_ROWS + 1) * SQUARE_SIZE
    size = (width, height)
    RADIUS = int(SQUARE_SIZE / 2 - 5)
    screen = pygame.display.set_mode(size)
    myfont = pygame.font.SysFont("monospace", 75)

    client_socket = create_client_socket()
    print("Connected to the server at 127.0.0.1:3000")

    entry = ""
    while entry != "done":
        entry = input("Enter a string to send: ")
        ba = bytearray(entry, 'utf-8')
        written = client_socket.send(ba)

        if written != len(ba):
            print("Wrote: ", written)
            print("The socket appears to have been closed")
            break
        else:
            print("Sent: ", entry)

        data = client_socket.recv(1024)
        if len(data) <= 0:
            print("The socket appears to have been closed")
            break

        board_str = data.decode()
        board = get_board(board_str)
        print("Received board: ", board)

        draw_board(board, screen, SQUARE_SIZE, RADIUS, height)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()


    print("Sleep now")
    client_socket.close()

if __name__ == "__main__":
    main()