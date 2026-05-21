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