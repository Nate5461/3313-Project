import socket
import numpy as np
import pygame
import threading
import multiprocessing
import sys
import math

pygame.init()
BLUE_COLOR = (0, 0, 255)
BLACK_COLOR = (0, 0, 0)
RED_COLOR = (255, 0, 0)
YELLOW_COLOR = (255, 255, 0)

NUM_ROWS = 6
NUM_COLUMNS = 7
WIDTH, HEIGHT = 800, 600



# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)

# Fonts
MENU_FONT = pygame.font.SysFont(None, 60)
OPTION_FONT = pygame.font.SysFont(None, 40)
GAME_FONT = pygame.font.SysFont(None, 30)

SQUARE_SIZE = 100
width = NUM_COLUMNS * SQUARE_SIZE
height = (NUM_ROWS + 1) * SQUARE_SIZE
size = (width, height)
RADIUS = int(SQUARE_SIZE / 2 - 5)
screen = pygame.display.set_mode(size)

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
 
def pygame_loop(screen, SQUARE_SIZE, RADIUS, height, client_socket):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARE_SIZE))

                # Send the selected column to the server
                ba = bytearray(str(col), 'utf-8')
                client_socket.send(ba)

        pygame.display.update()

def server_loop(client_socket, board, condition):
    while True:
        data = client_socket.recv(1024)
        if len(data) <= 0:
            print("The socket appears to have been closed")
            break

        board_str = data.decode()
        print("Received board: ", board_str)

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def draw_button(text, font, color, surface, rect, hover):
    pygame.draw.rect(surface, color, rect)
    text_surface = font.render(text, True, BLACK if not hover else WHITE)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)

def draw_game_list(surface):
    game_names = ["Game 1", "Game 2", "Game 3", "Game 4", "Game 5"]  # Sample game names
    game_y = HEIGHT // 2 + 2 * 50
    for game_name in game_names:
        text_obj = GAME_FONT.render(game_name, True, BLACK)
        text_rect = text_obj.get_rect(center=(WIDTH // 2, game_y))
        surface.blit(text_obj, text_rect)
        game_y += 50

def display_game_ids(game_ids, client_socket):
    clock = pygame.time.Clock()
    while True:
        screen.fill(WHITE)
        draw_text("Select a game to join", MENU_FONT, BLACK, screen, WIDTH // 2, HEIGHT // 4)
        
        game_y = HEIGHT // 2 + 2 * 50
        game_id_rects = []
        for game_id in game_ids:
            rect = pygame.Rect(WIDTH // 2 - 100, game_y, 200, 50)
            game_id_rects.append(rect)
            draw_button(str(game_id), OPTION_FONT, GRAY, screen, rect, False)
            game_y += 60

        pygame.display.update()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for i, rect in enumerate(game_id_rects):
                    if rect.collidepoint(mouse_x, mouse_y):
                        print(f"Joining game {game_ids[i]}...")
                        client_socket.send(f"join {game_ids[i]}".encode())

def main_menu():
    client_socket = create_client_socket()
    

    clock = pygame.time.Clock()
    while True:
        screen.fill(WHITE)
        draw_text("Main Menu", MENU_FONT, BLACK, screen, WIDTH // 2, HEIGHT // 4)
        
        # Draw empty box
        pygame.draw.rect(screen, GRAY, (WIDTH // 4, HEIGHT // 3, WIDTH // 2, HEIGHT // 4))
        
        # Button dimensions and positioning
        button_width, button_height = 200, 50
        button_x, button_spacing = WIDTH // 2, 100

        # Start Game Button
        start_button_rect = pygame.Rect(button_x - button_width // 2, HEIGHT // 2, button_width, button_height)
        draw_button("Start Game", OPTION_FONT, GRAY, screen, start_button_rect, False)
        
        # Options Button
        join_button_rect = pygame.Rect(button_x - button_width // 2, HEIGHT // 2 + button_spacing, button_width, button_height)
        draw_button("Join", OPTION_FONT, GRAY, screen, join_button_rect, False)
        
        # Exit Button
        exit_button_rect = pygame.Rect(button_x - button_width // 2, HEIGHT // 2 + 2 * button_spacing, button_width, button_height)
        draw_button("Exit", OPTION_FONT, GRAY, screen, exit_button_rect, False)

        # Check for hover effect
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if start_button_rect.collidepoint(mouse_x, mouse_y):
            draw_button("Start Game", OPTION_FONT, GREEN, screen, start_button_rect, True)
        elif join_button_rect.collidepoint(mouse_x, mouse_y):
            draw_button("Join", OPTION_FONT, GREEN, screen, join_button_rect, True)
        elif exit_button_rect.collidepoint(mouse_x, mouse_y):
            draw_button("Exit", OPTION_FONT, GREEN, screen, exit_button_rect, True)

        pygame.display.update()
        clock.tick(60)
        
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button_rect.collidepoint(mouse_x, mouse_y):
                        print("Starting ConnectFour...")
                        client_socket.send(b"start")
                        p = multiprocessing.Process(target=pygame_loop, args=(screen, SQUARE_SIZE, RADIUS, HEIGHT, client_socket))
                    elif join_button_rect.collidepoint(mouse_x, mouse_y):
                        client_socket.send(b"join")
                        data = client_socket.recv(1024)
                        print("hello")
                        print("Data: ", data)
                        game_ids = list(map(int, data.decode().split()))
                        print("Game IDs: ", game_ids)
                        j = threading.Thread(target=display_game_ids, args=(game_ids, client_socket))
                    elif exit_button_rect.collidepoint(mouse_x, mouse_y):
                        pygame.quit()
                        sys.exit()

def main():

    board = []
    condition = threading.Condition()

    client_socket = create_client_socket()

    server_thread = threading.Thread(target=server_loop, args=(client_socket, board, condition))
    server_thread.start()



    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARE_SIZE))

                # Send the selected column to the server
                ba = bytearray(str(col), 'utf-8')
                client_socket.send(ba)

        with condition:
            condition.wait()
            draw_board(board, screen, SQUARE_SIZE, RADIUS, height)

        pygame.display.update()

    server_thread.join()

    print("Sleep now")
    client_socket.close()

if __name__ == "__main__":
    main_menu()