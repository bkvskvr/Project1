# Функції малювання
import pygame
from settings import *
import assets

def draw_grid(screen, left_margin, letters_on_right=False):
    for row in range(board_size):
        for col in range(board_size):
            rect = pygame.Rect(
                left_margin + col * cell_size,
                margin_top + row * cell_size,
                cell_size,
                cell_size
            )
            pygame.draw.rect(screen, GRID_COLOR, rect, 1, border_radius=6)

    for i in range(board_size):
        num_text = assets.font.render(str(i + 1), True, TEXT_COLOR)
        num_x = left_margin + i * cell_size + (cell_size // 2) - (num_text.get_width() // 2)
        screen.blit(num_text, (num_x, margin_top - 30))

        letter_text = assets.font.render(letters[i], True, TEXT_COLOR)
        letter_y = margin_top + i * cell_size + (cell_size // 2) - (letter_text.get_height() // 2)

        if letters_on_right:
            screen.blit(letter_text, (left_margin + board_size * cell_size + 10, letter_y))
        else:
            screen.blit(letter_text, (left_margin - 30, letter_y))


def get_grid_coords(pos, left_margin):
    x, y = pos
    if left_margin <= x <= left_margin + board_size * cell_size:
        if margin_top <= y <= margin_top + board_size * cell_size:
            col = (x - left_margin) // cell_size
            row = (y - margin_top) // cell_size
            if 0 <= col < 10 and 0 <= row < 10:
                return row, col
    return None


def draw_end_screen(screen, win=True):
    overlay = pygame.Surface((1000, 600), pygame.SRCALPHA)
    overlay.fill(DARK_OVERLAY)
    screen.blit(overlay, (0, 0))

    title_text = "ПЕРЕМОГА!" if win else "ПОРАЗКА..."
    color = (0, 255, 100) if win else RED

    title_surf = assets.font_huge.render(title_text, True, color)
    title_rect = title_surf.get_rect(center=(500, 250))
    screen.blit(title_surf, title_rect)

    sub_text = assets.font_large.render("Натисніть 'R' для нової гри або 'ESC' для виходу", True, WHITE)
    sub_rect = sub_text.get_rect(center=(500, 350))
    screen.blit(sub_text, sub_rect)

def draw_ships(screen, board, ship_images, destroyed_ships, margin_left):
    # Малюємо кораблі (сірі блоки або картинки)
    # Беремо кораблі з об'єкта дошки
    for ship in board.ships:
        min_x = min(c[0] for c in ship.coordinates)
        min_y = min(c[1] for c in ship.coordinates)

        is_horizontal = True
        if len(ship.coordinates) > 1:
            if ship.coordinates[0][0] == ship.coordinates[1][0]:
                is_horizontal = False

        length = len(ship.coordinates)
        img_key = length if is_horizontal else f"v{length}"

        px = margin_left + min_x * cell_size
        py = margin_top + min_y * cell_size

        if img_key in ship_images:
            coords_set = [tuple(c) for c in ship.coordinates]
            if coords_set not in [list(map(tuple, d)) for d in destroyed_ships]:
                screen.blit(ship_images[img_key], (px, py))
        else:
            # Запасний варіант відмальовки, якщо картинок немає
            for x, y in ship.coordinates:  # x - стовпець, y - рядок
                pygame.draw.rect(screen, SHIP_COLOR,
                                 (margin_left + x * cell_size + 2, margin_top + y * cell_size + 2, cell_size - 4,
                                  cell_size - 4), border_radius=8)
                pygame.draw.rect(screen, ACCENT,
                                 (margin_left + x * cell_size + 2, margin_top + y * cell_size + 2, cell_size - 4,
                                  cell_size - 4), 2, border_radius=8)


def draw_shots(screen, board, margin_left):
    # Малюємо постріли НАПРЯМУ З МАТРИЦІ ДОШКИ
    for y in range(10):
        for x in range(10):
            if board.field[y][x] == 2:  # Промах
                pygame.draw.circle(screen, WHITE,
                                   (margin_left + x * cell_size + 20, margin_top + y * cell_size + 20), 5)
            elif board.field[y][x] == 3:  # Влучання
                px, py = margin_left + x * cell_size, margin_top + y * cell_size
                pygame.draw.line(screen, RED, (px + offset, py + offset),
                                 (px + cell_size - offset, py + cell_size - offset), 3)
                pygame.draw.line(screen, RED, (px + cell_size - offset, py + offset),
                                 (px + offset, py + cell_size - offset), 3)