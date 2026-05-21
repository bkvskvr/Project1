from ui import *
from Ship import Ship
from Bot import Bot
from Board import Board
from Player import Player


def reset_game():
    global player_board, bot_board, bot_brain, human_player, game_state  # ДОДАНО human_player
    global current_orientation, game_message, selected_arsenal_idx, arsenal
    global explosions, destroyed_ships, destroyed_bot_ships  # Додано для анімацій

    player_board = Board()
    bot_board = Board()

    # Ініціалізуємо і гравця, і бота як повноцінні об'єкти
    human_player = Player("Гравець", player_board, bot_board)
    bot_brain = Bot("Бот", bot_board, player_board)

    game_state = "PLACING"
    current_orientation = "h"  # Початкова орієнтація
    game_message = "Оберіть корабель, клікніть на нього."
    selected_arsenal_idx = None
    for item in arsenal:
        item["used"] = False

    explosions = []  # список активних вибухів: {"x": px, "y": py, "frame": 0}
    destroyed_ships = []  # координати знищених кораблів гравця
    destroyed_bot_ships = []  # координати знищених кораблів бота

assets.init_game()

# розпаковуємо змінні, щоб не писати "assets." скрізь:
screen, ship_images, font, font_large, font_huge, background = (
    assets.screen, assets.ship_images, assets.font,
    assets.font_large, assets.font_huge, assets.background
)


# Можливий вибір всіх кораблів
# Створюємо кнопки-кораблі для інтерфейсу вибору
arsenal = [
    {"length": 4, "rect": pygame.Rect(margin_left_bot, margin_top, 4 * cell_size, cell_size), "used": False},
    {"length": 3, "rect": pygame.Rect(margin_left_bot, margin_top + 60, 3 * cell_size, cell_size), "used": False},
    {"length": 3, "rect": pygame.Rect(margin_left_bot + 140, margin_top + 60, 3 * cell_size, cell_size), "used": False},
    {"length": 2, "rect": pygame.Rect(margin_left_bot, margin_top + 120, 2 * cell_size, cell_size), "used": False},
    {"length": 2, "rect": pygame.Rect(margin_left_bot + 100, margin_top + 120, 2 * cell_size, cell_size),
     "used": False},
    {"length": 2, "rect": pygame.Rect(margin_left_bot + 200, margin_top + 120, 2 * cell_size, cell_size),
     "used": False},
    {"length": 1, "rect": pygame.Rect(margin_left_bot, margin_top + 180, cell_size, cell_size), "used": False},
    {"length": 1, "rect": pygame.Rect(margin_left_bot + 60, margin_top + 180, cell_size, cell_size), "used": False},
    {"length": 1, "rect": pygame.Rect(margin_left_bot + 120, margin_top + 180, cell_size, cell_size), "used": False},
    {"length": 1, "rect": pygame.Rect(margin_left_bot + 180, margin_top + 180, cell_size, cell_size), "used": False},
]

reset_game()


# Головний цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Обертання корабля на 90 градусів
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                current_orientation = "v" if current_orientation == "h" else "h"

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
                            game_message = "Корабель обрано. Розмістіть його."
                            clicked_arsenal = True
                            break

                    # 2. Якщо клікнули не по кораблю, а по полю (щоб поставити)
                    if not clicked_arsenal and selected_arsenal_idx is not None:
                        coords_player = get_grid_coords(mouse_pos, margin_left_player)
                        if coords_player:
                            r, c = coords_player  # r = y (рядок), c = x (стовпчик)
                            length = arsenal[selected_arsenal_idx]["length"]
                            temp_ship = Ship(length, current_orientation)
                            temp_ship.set_coordinate(c, r)

                            if player_board.add_ship(temp_ship):
                                arsenal[selected_arsenal_idx]["used"] = True
                                selected_arsenal_idx = None
                                game_message = "Корабель встановлено! Оберіть наступний."

                                # Перевірка чи всі кораблі розставлені
                                if all(item["used"] for item in arsenal):
                                    bot_board.auto_place_ships()
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
                        if bot_board.field[r][c] in [2, 3]:
                            game_message = "В цю клітинку вже вистрілено! Обери іншу."
                        else:
                            # РОБИМО ПОСТРІЛ ЧЕРЕЗ КЛАС ГРАВЦЯ!
                            result = human_player.make_shot(c, r)
                            if result is True:
                                game_message = f"Влучив у {letters[r]}{c + 1}!"

                                # Шукаємо, який саме корабель бота підбито
                                for ship in bot_board.ships:
                                    if (c, r) in ship.coordinates:
                                        ship.hiten()
                                        if ship.defeated():
                                            game_message += " КОРАБЕЛЬ ЗНИЩЕНО!"
                                            bot_board.mark_destroyed_perimeter(bot_board, ship)
                                            destroyed_bot_ships.append(list(ship.coordinates))
                                            for cx, cy in ship.coordinates:
                                                explosions.append({"x": margin_left_bot + cx * cell_size,
                                                                   "y": margin_top + cy * cell_size, "frame": 0})
                                            # ПЕРЕВІРЯЄМО ПЕРЕМОГУ ЧЕРЕЗ КЛАС БОТА!
                                            if bot_brain.is_defeated():
                                                game_state = "GAME_OVER"
                                        break
                            elif result is False:
                                game_message = "Мимо! "

                                # Хід бота
                                bot_turn_active, bot_msg = bot_brain.make_turn(
                                    player_board, explosions, destroyed_ships,
                                    cell_size, margin_left_player, margin_top
                                )
                                game_message += bot_msg

                                # ПЕРЕВІРЯЄМО ПОРАЗКУ ЧЕРЕЗ КЛАС ГРАВЦЯ!
                                if human_player.is_defeated():
                                    game_state = "GAME_OVER"



    # Отрисовка
    screen.blit(background, (0, 0))
    overlay = pygame.Surface((1000, 600), pygame.SRCALPHA)
    overlay.fill((0, 0, 20, 120))
    screen.blit(overlay, (0, 0))

    draw_grid(screen, margin_left_player, letters_on_right=False)

    if game_state in ["PLAYING", "GAME_OVER"]:
        draw_grid(screen, margin_left_bot, letters_on_right=True)

    # Малюємо кораблі гравця (сірі блоки або картинки)
    # Беремо кораблі з об'єкта дошки
    draw_ships(screen, player_board, ship_images, destroyed_ships, margin_left_player)
    # Відображення корабля пперед тим як розмістити його
    if game_state == "PLACING":
        arsenal_title = font_large.render("АРСЕНАЛ ФЛОТУ:", True, WHITE)
        screen.blit(arsenal_title, (margin_left_bot, margin_top - 40))

        for i, item in enumerate(arsenal):
            if not item["used"]:
                if i == selected_arsenal_idx:
                    pygame.draw.rect(screen, ACCENT, item["rect"].inflate(4, 4), 2, border_radius=4)
                img = ship_images.get(item["length"])
                if img:
                    screen.blit(img, item["rect"].topleft)
                else:
                    pygame.draw.rect(screen, SHIP_COLOR, item["rect"])
                    for j in range(1, item["length"]):
                        lx = item["rect"].left + j * cell_size
                        pygame.draw.line(screen, PANEL_COLOR, (lx, item["rect"].top), (lx, item["rect"].bottom), 1)

        if selected_arsenal_idx is not None:
            mouse_pos = pygame.mouse.get_pos()
            hover_coords = get_grid_coords(mouse_pos, margin_left_player)
            if hover_coords:
                hr, hc = hover_coords
                length = arsenal[selected_arsenal_idx]["length"]
                img_key = length if current_orientation == "h" else f"v{length}"
                hover_img = ship_images.get(img_key)

                if hover_img:
                    transparent_img = hover_img.copy()
                    transparent_img.set_alpha(150)
                    hx = margin_left_player + hc * cell_size
                    hy = margin_top + hr * cell_size
                    screen.blit(transparent_img, (hx, hy))

                hover_ship = Ship(arsenal[selected_arsenal_idx]["length"], current_orientation)
                hover_ship.set_coordinate(hc, hr)
                # Малюємо світло-сірим кольором (тінь) ДАРИНА, МОЖЛИВО ЗРОБИШ ГАРНІШЕ
                for x, y in hover_ship.coordinates:
                    if 0 <= x <= 9 and 0 <= y <= 9:
                        hover_surface = pygame.Surface((cell_size - 4, cell_size - 4), pygame.SRCALPHA)
                        hover_surface.fill((0, 255, 255, 120))
                        screen.blit(hover_surface,
                                    (margin_left_player + x * cell_size + 2, margin_top + y * cell_size + 2))

        if game_state in ["PLAYING", "GAME_OVER"]:
            # Малюємо постріли для обох дощок через ui.py
            draw_shots(screen, bot_board, margin_left_bot)
            draw_shots(screen, player_board, margin_left_player)




    # Відображення повідомлень внизу екрана
    pygame.draw.rect(screen, PANEL_COLOR, (180, 510, 640, 55), border_radius=15)
    msg_surface = font.render(game_message, True, TEXT_COLOR)  # ДАРИНА МІНЯЙ
    msg_rect = msg_surface.get_rect(center=(500, 540))
    screen.blit(msg_surface, msg_rect)

    if game_state == "GAME_OVER":
        # І ТУТ ПЕРЕВІРКА ПЕРЕМОГИ ЧЕРЕЗ КЛАС БОТА!
        is_player_win = bot_brain.is_defeated()
        pygame.draw.rect(screen, (20, 20, 30), (250, 180, 500, 220), border_radius=25)
        draw_end_screen(screen, win=is_player_win)

    for exp in explosions[:]:
        frame = exp["frame"]
        radius = 5 + frame * 4
        alpha = max(0, 255 - frame * 6)
        surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(surf, (255, 140, 0, alpha), (radius, radius), radius)
        pygame.draw.circle(surf, (255, 255, 0, alpha // 2), (radius, radius), radius // 2)
        screen.blit(surf, (exp["x"] + cell_size // 2 - radius, exp["y"] + cell_size // 2 - radius))
        exp["frame"] += 1
        if exp["frame"] > 40:
            explosions.remove(exp)

    pygame.display.flip()

pygame.quit()