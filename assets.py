import pygame
from settings import CELL_SIZE

# Глобальні змінні для доступу з main.py
screen = None
ship_images = {}
font = None
font_large = None
font_huge = None
background = None


def init_game():
    global screen, ship_images, font, font_large, font_huge, background

    pygame.init()
    screen = pygame.display.set_mode((1000, 600))
    pygame.display.set_caption("Морський бій")


    try:
        bg_img = pygame.image.load("background.jpg")
        background = pygame.transform.scale(bg_img, (1000, 600))
    except FileNotFoundError:
        # Заглушка, якщо картинки немає
        background = pygame.Surface((1000, 600))
        background.fill((7, 15, 25))

    try:
        for i in range(1, 5):
            img = pygame.image.load(f"ship{i}.png").convert_alpha()
            scaled_img = pygame.transform.smoothscale(img, ( CELL_SIZE * i,  CELL_SIZE))
            ship_images[i] = scaled_img
            ship_images[f"v{i}"] = pygame.transform.rotate(scaled_img, -90)

    except FileNotFoundError:
        print("Увага: Не знайдені файли кораблів (ship1.png - ship4.png).")

    try:
        font = pygame.font.SysFont("Cy Grotesk Std Trial", 20)
        font_large = pygame.font.SysFont("Cy Grotesk Std Trial", 28, bold=True)
        font_huge = pygame.font.SysFont("Cy Grotesk Std Trial", 72, bold=True)
    except Exception:
        font = pygame.font.SysFont("arial", 20)
        font_large = pygame.font.SysFont("arial", 28, bold=True)
        font_huge = pygame.font.SysFont("arial", 72, bold=True)