import pygame
import sys
import subprocess

pygame.init()

# Set up window
WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Main Menu")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)

# Fonts
MENU_FONT = pygame.font.SysFont(None, 60)
OPTION_FONT = pygame.font.SysFont(None, 40)
GAME_FONT = pygame.font.SysFont(None, 30)

# Functions
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

def main_menu():
    clock = pygame.time.Clock()
    
    while True:
        WINDOW.fill(WHITE)
        draw_text("Main Menu", MENU_FONT, BLACK, WINDOW, WIDTH // 2, HEIGHT // 4)
        
        # Draw empty box
        pygame.draw.rect(WINDOW, GRAY, (WIDTH // 4, HEIGHT // 3, WIDTH // 2, HEIGHT // 4))
        
        # Button dimensions and positioning
        button_width, button_height = 200, 50
        button_x, button_spacing = WIDTH // 2, 100
        
        # Start Game Button
        start_button_rect = pygame.Rect(button_x - button_width // 2, HEIGHT // 2, button_width, button_height)
        draw_button("Start Game", OPTION_FONT, GRAY, WINDOW, start_button_rect, False)
        
        # Options Button
        options_button_rect = pygame.Rect(button_x - button_width // 2, HEIGHT // 2 + button_spacing, button_width, button_height)
        draw_button("Options", OPTION_FONT, GRAY, WINDOW, options_button_rect, False)
        
        # Exit Button
        exit_button_rect = pygame.Rect(button_x - button_width // 2, HEIGHT // 2 + 2 * button_spacing, button_width, button_height)
        draw_button("Exit", OPTION_FONT, GRAY, WINDOW, exit_button_rect, False)
        
        # Check for hover effect
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if start_button_rect.collidepoint(mouse_x, mouse_y):
            draw_button("Start Game", OPTION_FONT, GREEN, WINDOW, start_button_rect, True)
        elif options_button_rect.collidepoint(mouse_x, mouse_y):
            draw_button("Options", OPTION_FONT, GREEN, WINDOW, options_button_rect, True)
        elif exit_button_rect.collidepoint(mouse_x, mouse_y):
            draw_button("Exit", OPTION_FONT, GREEN, WINDOW, exit_button_rect, True)
        
        pygame.display.update()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(mouse_x, mouse_y):
                    print("Starting ConnectFour...")
                    subprocess.Popen(["python", "ConnectFour.py"])  # Start ConnectFour.py script
                elif options_button_rect.collidepoint(mouse_x, mouse_y):
                    print("Options")
                    # Call your options function or script here
                elif exit_button_rect.collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
    main_menu()
