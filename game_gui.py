import pygame
from ultimate_tictactoe import UltimateTicTacToe
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
CELL_SIZE = WIDTH // 9

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LINE_COLOR = (0, 0, 0)
TEXT_COLOR = (0, 0, 0)
PLAYER_X_COLOR = (255, 0, 0)
PLAYER_O_COLOR = (0, 0, 255)
BACKGROUND_COLOR = (255, 255, 255)

# Fonts
font = pygame.font.Font(None, 36)# Initialize the game

# Initialize Pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ultimate Tic-Tac-Toe")

def draw_board(game: UltimateTicTacToe):
    screen.fill(BACKGROUND_COLOR)

    # Draw grid lines
    for i in range(1, 9):
        pygame.draw.line(screen, LINE_COLOR, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), 2)
        pygame.draw.line(screen, LINE_COLOR, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), 2)

    # Draw X and O
    for large_row in range(3):
        for large_col in range(3):
            for small_row in range(3):
                for small_col in range(3):
                    x = large_col * 3 * CELL_SIZE + small_col * CELL_SIZE
                    y = large_row * 3 * CELL_SIZE + small_row * CELL_SIZE
                    cell_value = game.board[large_row,large_col,small_row,small_col]

                    if cell_value[0] == 1:
                        pygame.draw.line(screen, PLAYER_X_COLOR, (x + 10, y + 10), (x + CELL_SIZE - 10, y + CELL_SIZE - 10), 2)
                        pygame.draw.line(screen, PLAYER_X_COLOR, (x + CELL_SIZE - 10, y + 10), (x + 10, y + CELL_SIZE - 10), 2)
                    elif cell_value[1] == 1:
                        pygame.draw.circle(screen, PLAYER_O_COLOR, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), CELL_SIZE // 2 - 10, 2)

def draw_text(message):
    text = font.render(message, True, TEXT_COLOR)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)

def main():

    game = UltimateTicTacToe()
    draw_board(game)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not game.get_winner():
                mouse_x, mouse_y = pygame.mouse.get_pos()
                large_row = mouse_y // (3 * CELL_SIZE)
                large_col = mouse_x // (3 * CELL_SIZE)
                small_row = (mouse_y % (3 * CELL_SIZE)) // CELL_SIZE
                small_col = (mouse_x % (3 * CELL_SIZE)) // CELL_SIZE

                if game.make_move((large_row, large_col, small_row, small_col)):
                    draw_board(game)
                else:
                    print("Move failed.")

            if game.get_winner():
                draw_text(f"Player {game.get_winner()} wins!")
            else:
                current_player = game.get_current_player()
                draw_text(f"Player {current_player}'s turn")

            pygame.display.flip()

if __name__ == "__main__":
    main()