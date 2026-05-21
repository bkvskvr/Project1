# Налаштування Pygame     ДАРИНА ТУТ ПЕРЕГЛЯНЬ І ГАРНО ОФОРМИ!!!
import pygame
from settings import cell_size

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
        background = pygame.image.load("background.jpg")
        background = pygame.transform.scale(background, (1000, 600))
    except Exception:
        # Заглушка, якщо картинки ще немає в папці
        background = pygame.Surface((1000, 600))
        background.fill((7, 15, 25))

    ship_images = {}

    try:
        # Завантаження
        ship1 = pygame.image.load("ship1.png").convert_alpha()
        ship2 = pygame.image.load("ship2.png").convert_alpha()
        ship3 = pygame.image.load("ship3.png").convert_alpha()
        ship4 = pygame.image.load("ship4.png").convert_alpha()

        # Масштабування під клітинки
        ship_images[1] = pygame.transform.smoothscale(ship1, (cell_size, cell_size))
        ship_images[2] = pygame.transform.smoothscale(ship2, (cell_size * 2, cell_size))
        ship_images[3] = pygame.transform.smoothscale(ship3, (cell_size * 3, cell_size))
        ship_images[4] = pygame.transform.smoothscale(ship4, (cell_size * 4, cell_size))

        # Вертикальні версії
        ship_images["v1"] = pygame.transform.rotate(ship_images[1], -90)
        ship_images["v2"] = pygame.transform.rotate(ship_images[2], -90)
        ship_images["v3"] = pygame.transform.rotate(ship_images[3], -90)
        ship_images["v4"] = pygame.transform.rotate(ship_images[4], -90)

        print("PNG кораблі завантажені!")
    except Exception as e:
        print("Помилка завантаження картинок:", e)

    pygame.font.init()  # ДАРИНА, ЗВЕРНИ УВАГУ!!!!!!!!!!!
    try:
        font = pygame.font.SysFont("Cy Grotesk Std Trial", 20)
        font_large = pygame.font.SysFont("Cy Grotesk Std Trial", 28, bold=True)
        font_huge = pygame.font.SysFont("Cy Grotesk Std Trial", 72, bold=True)
    except:
        font = pygame.font.SysFont("arial", 20)
        font_large = pygame.font.SysFont("arial", 28, bold=True)
        font_huge = pygame.font.SysFont("arial", 72, bold=True)