import pygame
import random
from Ship import Ship
from Bot import Bot
from Board import Board

# Створюємо ОБ'ЄКТИ ДОЩОК для логіки
player_board = Board()
bot_board = Board()

# --- 1. Ініціалізація флоту гравця ---
player_ships = []
game_state = "PLACING"
current_orientation = "h" # Початкова орієнтація

# НОВА ЗМІННА: зберігає повідомлення для екрану
game_message = "Оберіть корабель з Арсеналу справа (клікніть на нього)."

# --- 2. Списки для пострілів бота на полі гравця ---
bot_shots_miss = []
bot_shots_hit = []

# Ініціалізація бота (передаємо 3 аргументи, як вимагає Player)
bot_brain = Bot("Комп'ютер", bot_board, player_board)

# --- Налаштування Pygame ---
pygame.init()
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Морський бій")

BLUE = (80, 134, 191)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
GRAY = (100, 100, 100)
YELLOW = (255, 255, 0)
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
font_large = pygame.font.SysFont('arial', 26, bold=True)
letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

# === НОВИЙ БЛОК: АРСЕНАЛ ФЛОТУ ===
# Створюємо кнопки-кораблі для інтерфейсу вибору
arsenal = [
    {"length": 4, "rect": pygame.Rect(margin_left_bot, margin_top, 4*cell_size, cell_size), "used": False},
    {"length": 3, "rect": pygame.Rect(margin_left_bot, margin_top + 60, 3*cell_size, cell_size), "used": False},
    {"length": 3, "rect": pygame.Rect(margin_left_bot + 140, margin_top + 60, 3*cell_size, cell_size), "used": False},
    {"length": 2, "rect": pygame.Rect(margin_left_bot, margin_top + 120, 2*cell_size, cell_size), "used": False},
    {"length": 2, "rect": pygame.Rect(margin_left_bot + 100, margin_top + 120, 2*cell_size, cell_size), "used": False},
    {"length": 2, "rect": pygame.Rect(margin_left_bot + 200, margin_top + 120, 2*cell_size, cell_size), "used": False},
    {"length": 1, "rect": pygame.Rect(margin_left_bot, margin_top + 180, cell_size, cell_size), "used": False},
    {"length": 1, "rect": pygame.Rect(margin_left_bot + 60, margin_top + 180, cell_size, cell_size), "used": False},
    {"length": 1, "rect": pygame.Rect(margin_left_bot + 120, margin_top + 180, cell_size, cell_size), "used": False},
    {"length": 1, "rect": pygame.Rect(margin_left_bot + 180, margin_top + 180, cell_size, cell_size), "used": False},
]
selected_arsenal_idx = None # Індекс вибраного корабля


# --- Функції малювання ---
def draw_grid(screen, left_margin):
    for i in range(board_size + 1):
        y = margin_top + i * cell_size
        pygame.draw.line(screen, WHITE, (left_margin, y), (left_margin + board_size * cell_size, y), 2)
        x = left_margin + i * cell_size
        pygame.draw.line(screen, WHITE, (x, margin_top), (x, margin_top + board_size * cell_size), 2)

    for i in range(board_size):
        num_text = font.render(str(i + 1), True, WHITE)
        num_x = left_margin + i * cell_size + (cell_size // 2) - (num_text.get_width() // 2)
        screen.blit(num_text, (num_x, margin_top - 30))

        letter_text = font.render(letters[i], True, WHITE)
        letter_y = margin_top + i * cell_size + (cell_size // 2) - (letter_text.get_height() // 2)
        screen.blit(letter_text, (left_margin - 30, letter_y))

def get_grid_coords(mouse_pos, left_margin):
    mx, my = mouse_pos
    if not (margin_top <= my < margin_top + board_size * cell_size and
            left_margin <= mx < left_margin + board_size * cell_size):
        return None
    return (my - margin_top) // cell_size, (mx - left_margin) // cell_size

def place_bot_ships(board):
    lengths = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    for length in lengths:
        placed = False
        while not placed:
            orient = random.choice(['h', 'v'])
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            ship = Ship(length, orient)
            ship.set_coordinate(x, y)
            if board.add_ship(ship):
                placed = True

# Функція для автоматичного замальовування периметру потопленого корабля
def mark_destroyed_perimeter(board, ship, shots_miss_list, bot_brain=None):
    for sx, sy in ship.coordinates:
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = sx + dx, sy + dy
                if 0 <= nx < 10 and 0 <= ny < 10:
                    if board.field[ny][nx] == 0: # Якщо там вода
                        board.field[ny][nx] = 2  # Ставимо промах
                        if (ny, nx) not in shots_miss_list:
                            shots_miss_list.append((ny, nx))

                        # Якщо це поле гравця, забороняємо боту сюди стріляти
                        if bot_brain is not None:
                            bot_brain.shoted.add((ny, nx))
                            if (ny, nx) in bot_brain.possible_opt:
                                bot_brain.possible_opt.remove((ny, nx))


# --- Головний цикл ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Обертання корабля на 90 градусів
        elif event.type == pygame.KEYDOWN:
            if game_state == "PLACING":
                if event.key in (pygame.K_RIGHT, pygame.K_LEFT):
                    current_orientation = "v" if current_orientation == "h" else "h"

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()

                # ---- ФАЗА РОЗСТАНОВКИ ----
                if game_state == "PLACING":
                    # 1. Перевіряємо клік по Арсеналу
                    clicked_arsenal = False
                    for i, item in enumerate(arsenal):
                        if not item["used"] and item["rect"].collidepoint(mouse_pos):
                            selected_arsenal_idx = i
                            game_message = f"Обрано корабель на {item['length']} палуб. Клікніть на ліве поле."
                            clicked_arsenal = True
                            break

                    # 2. Якщо клікнули не по Арсеналу, а по полю (щоб поставити)
                    if not clicked_arsenal and selected_arsenal_idx is not None:
                        coords_player = get_grid_coords(mouse_pos, margin_left_player)
                        if coords_player:
                            r, c = coords_player # r = y (рядок), c = x (стовпчик)
                            length = arsenal[selected_arsenal_idx]["length"]

                            temp_ship = Ship(length, current_orientation)
                            temp_ship.set_coordinate(c, r)

                            if player_board.add_ship(temp_ship):
                                arsenal[selected_arsenal_idx]["used"] = True
                                selected_arsenal_idx = None
                                game_message = "Корабель встановлено! Оберіть наступний."

                                # Перевірка чи всі кораблі розставлені
                                if all(item["used"] for item in arsenal):
                                    place_bot_ships(bot_board)
                                    game_state = "PLAYING"
                                    game_message = "Флот розгорнуто! Твій хід — стріляй по правому полю."
                            else:
                                game_message = "Тут ставити не можна! (Перетин або надто близько)"

                # ---- ФАЗА БОЮ ----
                elif game_state == "PLAYING":
                    coords_bot = get_grid_coords(mouse_pos, margin_left_bot)
                    if coords_bot:
                        r, c = coords_bot
                        if coords_bot in player_shots_miss or coords_bot in player_shots_hit:
                            game_message = "В цю клітинку вже вистрілено! Обери іншу."
                        else:
                            result = bot_board.shot(c, r)

                            if result is True:
                                player_shots_hit.append(coords_bot)
                                game_message = f"Влучив у {letters[r]}{c + 1}!"

                                # Шукаємо, який саме корабель бота підбито
                                for ship in bot_board.ships:
                                    if (c, r) in ship.coordinates:
                                        ship.hiten() #
                                        if ship.defeated():
                                            game_message += " КОРАБЕЛЬ ЗНИЩЕНО!"
                                            mark_destroyed_perimeter(bot_board, ship, player_shots_miss)
                                        break

                            elif result is False:
                                player_shots_miss.append(coords_bot)
                                game_message = "Мимо! "

                                # Хід бота
                                bot_turn = True
                                bot_hit_flag = False
                                while bot_turn:
                                    b_move = bot_brain.get_move()
                                    if not b_move: break

                                    b_row, b_col = b_move # y, x
                                    b_res = player_board.shot(b_col, b_row)

                                    if b_res is True:
                                        bot_shots_hit.append((b_row, b_col))
                                        bot_brain.register_hit(b_row, b_col)
                                        bot_hit_flag = True

                                        # Шукаємо, який корабель гравця підбито ботом
                                        for ship in player_board.ships:
                                            if (b_col, b_row) in ship.coordinates:
                                                ship.hiten()
                                                if ship.defeated():
                                                    mark_destroyed_perimeter(player_board, ship, bot_shots_miss, bot_brain)
                                                break

                                    elif b_res is False:
                                        bot_shots_miss.append((b_row, b_col))
                                        bot_turn = False

                                if bot_hit_flag:
                                    game_message += "Бот влучив у твій корабель! Твій хід."
                                else:
                                    game_message += "Бот промахнувся. Твій хід."

    # --- Отрисовка ---
    screen.fill(BLUE)
    draw_grid(screen, margin_left_player)

    # Малюємо праве поле тільки в режимі бою
    if game_state == "PLAYING":
        draw_grid(screen, margin_left_bot)

    # Малюємо кораблі гравця (сірі блоки)
    for ship in player_board.ships:
        for x, y in ship.coordinates:
            pygame.draw.rect(screen, GRAY, (margin_left_player + x * cell_size + 2,
                                            margin_top + y * cell_size + 2,
                                            cell_size - 4, cell_size - 4))

    # Відображення Арсеналу та "тіні" під час розстановки
    if game_state == "PLACING":
        arsenal_title = font_large.render("Арсенал (Клікніть на корабель):", True, WHITE)
        screen.blit(arsenal_title, (margin_left_bot, margin_top - 40))

        for i, item in enumerate(arsenal):
            if not item["used"]:
                color = YELLOW if i == selected_arsenal_idx else GRAY
                rect = item["rect"]
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, WHITE, rect, 2)
                # Малюємо клітинки всередині корабля в арсеналі
                for j in range(1, item["length"]):
                    pygame.draw.line(screen, WHITE, (rect.left + j * cell_size, rect.top), (rect.left + j * cell_size, rect.bottom), 1)

        # Тінь вибраного корабля на полі
        if selected_arsenal_idx is not None:
            mouse_pos = pygame.mouse.get_pos()
            hover_coords = get_grid_coords(mouse_pos, margin_left_player)

            if hover_coords:
                hr, hc = hover_coords
                hover_ship = Ship(arsenal[selected_arsenal_idx]["length"], current_orientation)
                hover_ship.set_coordinate(hc, hr)

                for x, y in hover_ship.coordinates:
                    if 0 <= x <= 9 and 0 <= y <= 9:
                        pygame.draw.rect(screen, (150, 150, 150),
                                         (margin_left_player + x * cell_size + 2,
                                          margin_top + y * cell_size + 2,
                                          cell_size - 4, cell_size - 4))

    # Малюємо постріли (ТІЛЬКИ В РЕЖИМІ БОЮ)
    if game_state == "PLAYING":
        # Постріли гравця по боту
        for r, c in player_shots_miss:
            pygame.draw.circle(screen, WHITE, (margin_left_bot + c * cell_size + 20, margin_top + r * cell_size + 20), 5)
        for r, c in player_shots_hit:
            x = margin_left_bot + c * cell_size
            y = margin_top + r * cell_size
            pygame.draw.line(screen, RED, (x + offset, y + offset), (x + cell_size - offset, y + cell_size - offset), 3)
            pygame.draw.line(screen, RED, (x + cell_size - offset, y + offset), (x + offset, y + cell_size - offset), 3)

        # Постріли бота по гравцю
        for r, c in bot_shots_miss:
            pygame.draw.circle(screen, WHITE, (margin_left_player + c * cell_size + 20, margin_top + r * cell_size + 20), 5)
        for r, c in bot_shots_hit:
            x = margin_left_player + c * cell_size
            y = margin_top + r * cell_size
            pygame.draw.line(screen, RED, (x + offset, y + offset), (x + cell_size - offset, y + cell_size - offset), 3)
            pygame.draw.line(screen, RED, (x + cell_size - offset, y + offset), (x + offset, y + cell_size - offset), 3)


    # --- ВІДОБРАЖЕННЯ ПОВІДОМЛЕНЬ ВНИЗУ ЕКРАНУ ---
    msg_surface = font_large.render(game_message, True, YELLOW)
    msg_rect = msg_surface.get_rect(center=(500, 540))
    screen.blit(msg_surface, msg_rect)

    pygame.display.flip()

pygame.quit()