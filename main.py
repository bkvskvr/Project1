import pygame
import random
from Ship import Ship
from Bot import Bot
from Board import Board

def reset_game():
    global player_board, bot_board, bot_brain, game_state
    global current_orientation, game_message, selected_arsenal_idx, arsenal

    player_board = Board()
    bot_board = Board()
    bot_brain = Bot("Бот", bot_board, player_board)
    game_state = "PLACING"
    current_orientation = "h" # Початкова орієнтація
    game_message = "Оберіть корабель, клікніть на нього."
    selected_arsenal_idx = None
    for item in arsenal:
        item["used"] = False

# Налаштування Pygame     ДАРИНА ТУТ ПЕРЕГЛЯНЬ І ГАРНО ОФОРМИ!!!
pygame.init()
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Морський бій")

BLUE = (80, 134, 191)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
GRAY = (100, 100, 100)
YELLOW = (255, 255, 0)
DARK_OVERLAY = (0, 0, 0, 180)
offset = 10
cell_size = 40
board_size = 10
margin_top = 80
margin_left_player = 70
margin_left_bot = 530

pygame.font.init() # ДАРИНА, ЗВЕРНИ УВАГУ!!!!!!!!!!!
font = pygame.font.SysFont('arial', 20)
font_large = pygame.font.SysFont('arial', 26, bold=True)
font_huge = pygame.font.SysFont('arial', 60, bold=True)
letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

# Можливий вибір всіх кораблів
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

reset_game()

# Функції малювання
def draw_grid(screen, left_margin, letters_on_right=False):
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
        if letters_on_right:
            screen.blit(letter_text, (left_margin + board_size * cell_size + 10, letter_y))
        else:
            screen.blit(letter_text, (left_margin - 30, letter_y))

def get_grid_coords(mouse_pos, left_margin):
    mx, my = mouse_pos
    if not (margin_top <= my < margin_top + board_size * cell_size and
            left_margin <= mx < left_margin + board_size * cell_size):
        return None
    return (my - margin_top) // cell_size, (mx - left_margin) // cell_size

# Функція для автоматичного замальовування навколо потопленого корабля
def mark_destroyed_perimeter(board, ship, bot_brain=None):
    for sx, sy in ship.coordinates:
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = sx + dx, sy + dy
                if 0 <= nx < 10 and 0 <= ny < 10:
                    if board.field[ny][nx] == 0:
                        board.field[ny][nx] = 2
                        if bot_brain is not None:
                            bot_brain.shoted.add((ny, nx))
                            if (ny, nx) in bot_brain.possible_opt:
                                bot_brain.possible_opt.remove((ny, nx))

def draw_end_screen(screen, win=True):
    overlay = pygame.Surface((1000, 600), pygame.SRCALPHA)
    overlay.fill(DARK_OVERLAY)
    screen.blit(overlay, (0,0))

    title_text = "ПЕРЕМОГА!" if win else "ПОРАЗКА..."
    color = YELLOW if win else RED

    title_surf = font_huge.render(title_text, True, color)
    title_rect = title_surf.get_rect(center=(500, 250))
    screen.blit(title_surf, title_rect)

    sub_text = font_large.render("Натисніть 'R' для нової гри або 'ESC' для виходу", True, WHITE)
    sub_rect = sub_text.get_rect(center=(500, 350))
    screen.blit(sub_text, sub_rect)

# Головний цикл
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

            if game_state == "GAME_OVER":
                if event.key == pygame.K_r:
                    reset_game()
                elif event.key == pygame.K_ESCAPE:
                    running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and game_state != "GAME_OVER":
                mouse_pos = pygame.mouse.get_pos()

                # ФАЗА РОЗСТАНОВКИ
                if game_state == "PLACING":
                    # 1. Перевіряємо клік по Арсеналу
                    clicked_arsenal = False
                    for i, item in enumerate(arsenal):
                        if not item["used"] and item["rect"].collidepoint(mouse_pos):
                            selected_arsenal_idx = i
                            game_message = f"Корабель обрано. Розмістіть його."
                            clicked_arsenal = True
                            break

                    # 2. Якщо клікнули не по кораблю, а по полю (щоб поставити)
                    if not clicked_arsenal and selected_arsenal_idx is not None:
                        coords_player = get_grid_coords(mouse_pos, margin_left_player)
                        if coords_player:
                            r, c = coords_player # r = y (рядок), c = x (стовпчик)
                            length = arsenal[selected_arsenal_idx]["length"]
                            temp_ship = Ship(length, current_orientation)
                            temp_ship.set_coordinate(c, r) #

                            if player_board.add_ship(temp_ship): #
                                arsenal[selected_arsenal_idx]["used"] = True
                                selected_arsenal_idx = None
                                game_message = "Корабель встановлено! Оберіть наступний."

                                # Перевірка чи всі кораблі розставлені
                                if all(item["used"] for item in arsenal):
                                    bot_board.auto_place_ships() #
                                    game_state = "PLAYING"
                                    game_message = "Флот розгорнуто! Твій хід — стріляй по правому полю."
                            else:
                                game_message = "Тут ставити не можна! Надто близько"

                # ФАЗА БОЮ
                elif game_state == "PLAYING":
                    coords_bot = get_grid_coords(mouse_pos, margin_left_bot)
                    if coords_bot:
                        r, c = coords_bot
                        # Перевірка через матрицю поля
                        if bot_board.field[r][c] in [2, 3]: #
                            game_message = "В цю клітинку вже вистрілено! Обери іншу."
                        else:
                            result = bot_board.shot(c, r) #
                            if result is True:
                                game_message = f"Влучив у {letters[r]}{c + 1}!"

                                # Шукаємо, який саме корабель бота підбито
                                for ship in bot_board.ships:
                                    if (c, r) in ship.coordinates:
                                        ship.hiten() #
                                        if ship.defeated():
                                            game_message += " КОРАБЕЛЬ ЗНИЩЕНО!"
                                            mark_destroyed_perimeter(bot_board, ship)
                                            if all(s.defeated() for s in bot_board.ships):
                                                game_state = "GAME_OVER"
                                        break
                            elif result is False:
                                game_message = "Мимо! "

                                # Хід бота
                                bot_turn = True
                                bot_hit_flag = False
                                while bot_turn and game_state == "PLAYING":
                                    b_move = bot_brain.get_move() #
                                    if not b_move: break
                                    b_row, b_col = b_move
                                    b_res = player_board.shot(b_col, b_row) #
                                    if b_res is True:
                                        bot_brain.register_hit(b_row, b_col)
                                        bot_hit_flag = True

                                        # Шукаємо який корабель гравця підбито ботом
                                        for ship in player_board.ships:
                                            if (b_col, b_row) in ship.coordinates:
                                                ship.hiten()
                                                if ship.defeated():
                                                    mark_destroyed_perimeter(player_board, ship, bot_brain)
                                                    if all(s.defeated() for s in player_board.ships):
                                                        game_state = "GAME_OVER"
                                                        bot_turn = False
                                                break
                                    elif b_res is False:
                                        bot_turn = False
                                if game_state == "PLAYING":
                                    if bot_hit_flag:
                                        game_message += " Бот влучив у твій корабель! Твій хід."
                                    else:
                                        game_message += " Бот промахнувся. Твій хід."

    # Отрисовка
    screen.fill(BLUE)
    draw_grid(screen, margin_left_player, letters_on_right=False)

    if game_state in ["PLAYING", "GAME_OVER"]:
        draw_grid(screen, margin_left_bot, letters_on_right=True)

    # Малюємо кораблі гравця (сірі блоки)
    # Беремо кораблі з об'єкта дошки
    for ship in player_board.ships:
        for x, y in ship.coordinates: # x - стовпець, y - рядок
            pygame.draw.rect(screen, GRAY, (margin_left_player + x * cell_size + 2, margin_top + y * cell_size + 2, cell_size - 4, cell_size - 4))

    # Відображення корабля пперед тим як розмістити його
    if game_state == "PLACING":
        arsenal_title = font_large.render("Набір кораблів:", True, WHITE)
        screen.blit(arsenal_title, (margin_left_bot, margin_top - 40))
        for i, item in enumerate(arsenal):
            if not item["used"]:
                color = YELLOW if i == selected_arsenal_idx else GRAY
                pygame.draw.rect(screen, color, item["rect"])
                pygame.draw.rect(screen, WHITE, item["rect"], 2)
                for j in range(1, item["length"]):
                    pygame.draw.line(screen, WHITE, (item["rect"].left + j * cell_size, item["rect"].top), (item["rect"].left + j * cell_size, item["rect"].bottom), 1)

        if selected_arsenal_idx is not None:
            mouse_pos = pygame.mouse.get_pos()
            hover_coords = get_grid_coords(mouse_pos, margin_left_player)
            if hover_coords:
                hr, hc = hover_coords
                hover_ship = Ship(arsenal[selected_arsenal_idx]["length"], current_orientation)
                hover_ship.set_coordinate(hc, hr)
                # Малюємо світло-сірим кольором (тінь) ДАРИНА, МОЖЛИВО ЗРОБИШ ГАРНІШЕ
                for x, y in hover_ship.coordinates:
                    if 0 <= x <= 9 and 0 <= y <= 9:
                        pygame.draw.rect(screen, (150, 150, 150), (margin_left_player + x * cell_size + 2, margin_top + y * cell_size + 2, cell_size - 4, cell_size - 4))

    if game_state in ["PLAYING", "GAME_OVER"]:
        # Малюємо постріли НАПРЯМУ З МАТРИЦІ ДОШКИ
        for y in range(10):
            for x in range(10):
                # Малюємо постріли гравця по боту
                if bot_board.field[y][x] == 2: # Промах
                    pygame.draw.circle(screen, WHITE, (margin_left_bot + x * cell_size + 20, margin_top + y * cell_size + 20), 5)
                elif bot_board.field[y][x] == 3: # Влучання
                    px, py = margin_left_bot + x * cell_size, margin_top + y * cell_size
                    pygame.draw.line(screen, RED, (px + offset, py + offset), (px + cell_size - offset, py + cell_size - offset), 3)
                    pygame.draw.line(screen, RED, (px + cell_size - offset, py + offset), (px + offset, py + cell_size - offset), 3)

                # Малюємо постріли бота по гравцю
                if player_board.field[y][x] == 2: # Промах
                    pygame.draw.circle(screen, WHITE, (margin_left_player + x * cell_size + 20, margin_top + y * cell_size + 20), 5)
                elif player_board.field[y][x] == 3: # Влучання
                    px, py = margin_left_player + x * cell_size, margin_top + y * cell_size
                    pygame.draw.line(screen, RED, (px + offset, py + offset), (px + cell_size - offset, py + cell_size - offset), 3)
                    pygame.draw.line(screen, RED, (px + cell_size - offset, py + offset), (px + offset, py + cell_size - offset), 3)

    # Відображення повідомлень внизу екрана
    msg_surface = font_large.render(game_message, True, YELLOW) #ДАРИНА МІНЯЙ
    msg_rect = msg_surface.get_rect(center=(500, 540))
    screen.blit(msg_surface, msg_rect)

    if game_state == "GAME_OVER":
        is_player_win = all(s.defeated() for s in bot_board.ships)
        draw_end_screen(screen, win=is_player_win)

    pygame.display.flip()

pygame.quit()