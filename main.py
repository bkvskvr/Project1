import pygame
from Ship import Ship
from Bot import Bot

# Якщо файл Board.py порожній або не використовується, цей імпорт можна прибрати
# from Board import Board

# --- 1. Ініціалізація флоту гравця ---
player_ships = []
ps1 = Ship(3, "v")
ps1.set_coordinate(2, 2)  # Корабель на В3, В4, В5
player_ships.append(ps1)

ps2 = Ship(1, "h")
ps2.set_coordinate(7, 7)  # Одиночний корабель
player_ships.append(ps2)

# --- 2. Списки для пострілів бота на полі гравця ---
bot_shots_miss = []
bot_shots_hit = []

# Ініціалізація бота (передаємо 3 аргументи, як вимагає Player)
bot_brain = Bot("Комп'ютер", None, None)

# Кораблі бота (ті, по яких стріляє гравець)
bot_ships = []
s1 = Ship(3, "h")
s1.set_coordinate(0, 0)
bot_ships.append(s1)

s2 = Ship(2, "v")
s2.set_coordinate(4, 5)
bot_ships.append(s2)

# --- Налаштування Pygame ---
pygame.init()
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Морський бій")

BLUE = (80, 134, 191)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
GRAY = (100, 100, 100)
offset = 10
cell_size = 40
board_size = 10
margin_top = 80
margin_left_player = 70
margin_left_bot = 550

player_shots_miss = []
player_shots_hit = []

pygame.font.init()
font = pygame.font.SysFont('arial', 20)
letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']


# --- Функції малювання ---
def draw_grid(screen, left_margin):
    for i in range(board_size + 1):
        y = margin_top + i * cell_size
        pygame.draw.line(screen, WHITE, (left_margin, y), (left_margin + board_size * cell_size, y), 2)
        x = left_margin + i * cell_size
        pygame.draw.line(screen, WHITE, (x, margin_top), (x, margin_top + board_size * cell_size), 2)

    for i in range(board_size):
        letter_text = font.render(letters[i], True, WHITE)
        letter_x = left_margin + i * cell_size + (cell_size // 2) - (letter_text.get_width() // 2)
        screen.blit(letter_text, (letter_x, margin_top - 30))
        num_text = font.render(str(i + 1), True, WHITE)
        num_y = margin_top + i * cell_size + (cell_size // 2) - (num_text.get_height() // 2)
        screen.blit(num_text, (left_margin - 30, num_y))


def get_grid_coords(mouse_pos, left_margin):
    mx, my = mouse_pos
    if not (margin_top <= my < margin_top + board_size * cell_size and
            left_margin <= mx < left_margin + board_size * cell_size):
        return None
    return (my - margin_top) // cell_size, (mx - left_margin) // cell_size


# --- Головний цикл ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # ВИПРАВЛЕНО: elif тепер на одному рівні з if event.type == pygame.QUIT
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                coords_bot = get_grid_coords(mouse_pos, margin_left_bot)

                if coords_bot:
                    if coords_bot in player_shots_miss or coords_bot in player_shots_hit:
                        print("В цю клітинку вже вистрілено!")
                    else:
                        hit_detected = False
                        # 1. Перевірка влучання гравця
                        for ship in bot_ships:
                            if coords_bot in ship.coordinates:
                                ship.hiten()
                                player_shots_hit.append(coords_bot)
                                hit_detected = True
                                print(f"Влучив! Життів у корабля бота: {ship.lives}")
                                if ship.defeated():
                                    print("КОРАБЕЛЬ БОТА ПОТОПЛЕНО!")
                                break

                        # 2. Якщо гравець промахнувся — хід бота
                        if not hit_detected:
                            player_shots_miss.append(coords_bot)
                            print("Мимо! Хід бота...")

                            bot_turn = True
                            while bot_turn:
                                b_move = bot_brain.get_move()
                                if not b_move: break  # На всяк випадок

                                b_row, b_col = b_move
                                bot_hit_something = False

                                for p_ship in player_ships:
                                    if (b_row, b_col) in p_ship.coordinates:
                                        p_ship.hiten()
                                        bot_shots_hit.append((b_row, b_col))
                                        bot_hit_something = True
                                        print(f"Бот влучив у {letters[b_col]}{b_row + 1}!")
                                        if p_ship.defeated():
                                            print("Твій корабель знищено!")
                                        break

                                if not bot_hit_something:
                                    bot_shots_miss.append((b_row, b_col))
                                    bot_turn = False  # Бот промахнувся

    # --- Отрисовка ---
    screen.fill(BLUE)
    draw_grid(screen, margin_left_player)
    draw_grid(screen, margin_left_bot)

    # Малюємо кораблі гравця (сірі блоки)
    for ship in player_ships:
        for r, c in ship.coordinates:
            pygame.draw.rect(screen, GRAY, (margin_left_player + c * cell_size + 2,
                                            margin_top + r * cell_size + 2,
                                            cell_size - 4, cell_size - 4))

    # Малюємо постріли гравця по боту
    for r, c in player_shots_miss:
        pygame.draw.circle(screen, WHITE, (margin_left_bot + c * cell_size + 20, margin_top + r * cell_size + 20), 5)
    for r, c in player_shots_hit:
        x = margin_left_bot + c * cell_size
        y = margin_top + r * cell_size
        pygame.draw.line(screen, RED, (x + offset, y + offset), (x + cell_size - offset, y + cell_size - offset), 3)
        pygame.draw.line(screen, RED, (x + cell_size - offset, y + offset), (x + offset, y + cell_size - offset), 3)

    # Малюємо постріли бота по гравцю
    for r, c in bot_shots_miss:
        pygame.draw.circle(screen, WHITE, (margin_left_player + c * cell_size + 20, margin_top + r * cell_size + 20), 5)
    for r, c in bot_shots_hit:
        x = margin_left_player + c * cell_size
        y = margin_top + r * cell_size
        pygame.draw.line(screen, RED, (x + offset, y + offset), (x + cell_size - offset, y + cell_size - offset), 3)
        pygame.draw.line(screen, RED, (x + cell_size - offset, y + offset), (x + offset, y + cell_size - offset), 3)

    pygame.display.flip()

pygame.quit()