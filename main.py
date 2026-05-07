import pygame

pygame.init()

screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Морський бій")

BLUE = (80, 134, 191)
WHITE = (255, 255, 255)

# Налаштування поля
cell_size = 40  # Раозмір клітинки
board_size = 10  # 10 на 10
margin_top = 80  # зверху
margin_left_player = 70
margin_left_bot = 550

pygame.font.init()
font = pygame.font.SysFont('arial', 20)

letters = ['A', 'B', 'C', 'D', 'E', 'F', 'J', 'K', 'L', 'M']

def draw_grid(screen, left_margin):
    for i in range(board_size + 1):
        y = margin_top + i * cell_size
        pygame.draw.line(screen, WHITE, (left_margin, y), (left_margin + board_size * cell_size, y), 2)

        x = left_margin + i * cell_size
        pygame.draw.line(screen, WHITE, (x, margin_top), (x, margin_top + board_size * cell_size), 2)

    for i in range(board_size):
        letter_text = font.render(letters[i], True, WHITE)
        letter_x = left_margin + i * cell_size + (cell_size // 2) - (letter_text.get_width() // 2)
        letter_y = margin_top - 30
        screen.blit(letter_text, (letter_x, letter_y))

        num_text = font.render(str(i + 1), True, WHITE)
        num_x = left_margin - 30 - (num_text.get_width() // 2)
        num_y = margin_top + i * cell_size + (cell_size // 2) - (num_text.get_height() // 2)
        screen.blit(num_text, (num_x, num_y))

def get_grid_coords(mouse_pos, left_margin):
    mx, my = mouse_pos

    if my < margin_top or my >= margin_top + board_size * cell_size:
        return None
    if mx < left_margin or mx >= left_margin + board_size * cell_size:
        return None

    column = (mx - left_margin) // cell_size
    row = (my - margin_top) // cell_size

    return (row, column)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                print(f"клік в пікселях: {mouse_pos}")

                coords_player = get_grid_coords(mouse_pos, margin_left_player)
                if coords_player:
                    row, col = coords_player
                    print(f"поле ігрока: Матриця({row}, {col}), Клітинка {letters[col]}{row + 1}")

                coords_bot = get_grid_coords(mouse_pos, margin_left_bot)
                if coords_bot:
                    row, col = coords_bot
                    print(f"поле бота: Матрица({row}, {col}), Клітинка {letters[col]}{row + 1}")

    screen.fill(BLUE)

    draw_grid(screen, margin_left_player)
    draw_grid(screen, margin_left_bot)

    # Обновлення екрану
    pygame.display.flip()
# Вихід
pygame.quit()