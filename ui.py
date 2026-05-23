import pygame
from settings import *
import assets


def draw_grid(screen, left_margin, letters_on_right=False):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            rect = pygame.Rect(
                left_margin + col * CELL_SIZE,
                MARGIN_TOP + row * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )
            pygame.draw.rect(screen, GRID_COLOR, rect, 1, border_radius=6)

    for i in range(BOARD_SIZE):
        num_text = assets.font.render(str(i + 1), True, TEXT_COLOR)
        num_x = left_margin + i * CELL_SIZE + (CELL_SIZE // 2) - (num_text.get_width() // 2)
        screen.blit(num_text, (num_x, MARGIN_TOP - 30))

        letter_text = assets.font.render(LETTERS[i], True, TEXT_COLOR)
        letter_y = MARGIN_TOP + i * CELL_SIZE + (CELL_SIZE // 2) - (letter_text.get_height() // 2)

        if letters_on_right:
            screen.blit(letter_text, (left_margin + BOARD_SIZE * CELL_SIZE + 10, letter_y))
        else:
            screen.blit(letter_text, (left_margin - 30, letter_y))


def get_grid_coords(pos, left_margin):
    x, y = pos

    # Відсікаємо кліки поза дошкою (early return)
    if not (left_margin <= x <= left_margin + BOARD_SIZE * CELL_SIZE):
        return None
    if not (MARGIN_TOP <= y <= MARGIN_TOP + BOARD_SIZE * CELL_SIZE):
        return None

    col = (x - left_margin) // CELL_SIZE
    row = (y - MARGIN_TOP) // CELL_SIZE

    return row, col


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


def draw_ships(screen, board, ship_images, margin_left):
    for ship in board.ships:
        min_x = min(c[0] for c in ship.coordinates)
        min_y = min(c[1] for c in ship.coordinates)

        # Використовуємо властивості об'єкта
        img_key = ship.length if ship.orientation == "h" else f"v{ship.length}"

        px = margin_left + min_x * CELL_SIZE
        py = MARGIN_TOP + min_y * CELL_SIZE

        if img_key in ship_images:
            # Малюємо картинку тільки якщо корабель ще живий
            if not ship.defeated():
                screen.blit(ship_images[img_key], (px, py))
        else:
            # Запасний варіант, якщо картинок немає
            for x, y in ship.coordinates:
                rect = (margin_left + x * CELL_SIZE + 2, MARGIN_TOP + y * CELL_SIZE + 2, CELL_SIZE - 4, CELL_SIZE - 4)
                pygame.draw.rect(screen, SHIP_COLOR, rect, border_radius=8)
                pygame.draw.rect(screen, ACCENT, rect, 2, border_radius=8)


def draw_shots(screen, board, margin_left):
    half_cell = CELL_SIZE // 2

    for y in range(10):
        for x in range(10):
            if board.field[y][x] == 2:  # Промах
                pygame.draw.circle(screen, WHITE,
                                   (margin_left + x * CELL_SIZE + half_cell, MARGIN_TOP + y * CELL_SIZE + half_cell), 5)
            elif board.field[y][x] == 3:  # Влучання
                px, py = margin_left + x * CELL_SIZE, MARGIN_TOP + y * CELL_SIZE
                pygame.draw.line(screen, RED, (px + OFFSET, py + OFFSET),
                                 (px + CELL_SIZE - OFFSET, py + CELL_SIZE - OFFSET), 3)
                pygame.draw.line(screen, RED, (px + CELL_SIZE - OFFSET, py + OFFSET),
                                 (px + OFFSET, py + CELL_SIZE - OFFSET), 3)