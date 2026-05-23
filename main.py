from ui import *
from Ship import Ship
from Bot import Bot
from Board import Board
from Player import Player
from audio import Audio
import assets  


def reset_game():
    global player_board, bot_board, bot_brain, human_player, game_state, audio
    global current_orientation, game_message, selected_arsenal_idx, arsenal
    global explosions, destroyed_ships, destroyed_bot_ships

    player_board = Board()
    bot_board = Board()

    human_player = Player("Гравець", player_board, bot_board)
    bot_brain = Bot("Бот", bot_board, player_board)

    game_state = "PLACING"
    current_orientation = "h"
    game_message = "Оберіть корабель, клікніть на нього."
    selected_arsenal_idx = None

    for item in arsenal:
        item["used"] = False

    explosions = []
    destroyed_ships = []
    destroyed_bot_ships = []

    audio = Audio()
    try:
        audio.load_sound("hit", "sounds/hit.wav")
        audio.load_sound("miss", "sounds/miss.wav")
        audio.load_sound("sink", "sounds/sink.wav")
    except Exception as e:
        print("Звуки не завантажено:", e)


assets.init_game()

screen = assets.screen
ship_images = assets.ship_images
font = assets.font
font_large = assets.font_large
font_huge = assets.font_huge
background = assets.background

arsenal = [
    {"length": 4, "rect": pygame.Rect(MARGIN_LEFT_BOT, MARGIN_TOP, 4 * CELL_SIZE, CELL_SIZE), "used": False},
    {"length": 3, "rect": pygame.Rect(MARGIN_LEFT_BOT, MARGIN_TOP + 60, 3 * CELL_SIZE, CELL_SIZE), "used": False},
    {"length": 3, "rect": pygame.Rect(MARGIN_LEFT_BOT + 140, MARGIN_TOP + 60, 3 * CELL_SIZE, CELL_SIZE), "used": False},
    {"length": 2, "rect": pygame.Rect(MARGIN_LEFT_BOT, MARGIN_TOP + 120, 2 * CELL_SIZE, CELL_SIZE), "used": False},
    {"length": 2, "rect": pygame.Rect(MARGIN_LEFT_BOT + 100, MARGIN_TOP + 120, 2 * CELL_SIZE, CELL_SIZE),
     "used": False},
    {"length": 2, "rect": pygame.Rect(MARGIN_LEFT_BOT + 200, MARGIN_TOP + 120, 2 * CELL_SIZE, CELL_SIZE),
     "used": False},
    {"length": 1, "rect": pygame.Rect(MARGIN_LEFT_BOT, MARGIN_TOP + 180, CELL_SIZE, CELL_SIZE), "used": False},
    {"length": 1, "rect": pygame.Rect(MARGIN_LEFT_BOT + 60, MARGIN_TOP + 180, CELL_SIZE, CELL_SIZE), "used": False},
    {"length": 1, "rect": pygame.Rect(MARGIN_LEFT_BOT + 120, MARGIN_TOP + 180, CELL_SIZE, CELL_SIZE), "used": False},
    {"length": 1, "rect": pygame.Rect(MARGIN_LEFT_BOT + 180, MARGIN_TOP + 180, CELL_SIZE, CELL_SIZE), "used": False},
]

reset_game()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                current_orientation = "v" if current_orientation == "h" else "h"

            if game_state == "PLACING" and event.key in (pygame.K_RIGHT, pygame.K_LEFT):
                current_orientation = "v" if current_orientation == "h" else "h"

            if game_state == "GAME_OVER":
                if event.key == pygame.K_r:
                    reset_game()
                elif event.key == pygame.K_ESCAPE:
                    running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and game_state != "GAME_OVER":
                mouse_pos = pygame.mouse.get_pos()

                if game_state == "PLACING":
                    clicked_arsenal = False
                    for i, item in enumerate(arsenal):
                        if not item["used"] and item["rect"].collidepoint(mouse_pos):
                            selected_arsenal_idx = i
                            game_message = "Корабель обрано. Розмістіть його на своєму полі."
                            clicked_arsenal = True
                            break

                    if not clicked_arsenal and selected_arsenal_idx is not None:
                        coords_player = get_grid_coords(mouse_pos, MARGIN_LEFT_PLAYER)
                        if coords_player:
                            r, c = coords_player
                            length = arsenal[selected_arsenal_idx]["length"]

                            temp_ship = Ship(length, current_orientation)
                            temp_ship.set_coordinates(c, r)  # ВИПРАВЛЕНО на set_coordinates

                            if player_board.add_ship(temp_ship):
                                arsenal[selected_arsenal_idx]["used"] = True
                                selected_arsenal_idx = None
                                game_message = "Корабель встановлено! Оберіть наступний."

                                if all(item["used"] for item in arsenal):
                                    bot_board.auto_place_ships()
                                    game_state = "PLAYING"
                                    game_message = "Флот розгорнуто! Твій хід — стріляй по правому полю."
                            else:
                                game_message = "Тут ставити не можна (перетин або поруч інший корабель)!"

                elif game_state == "PLAYING":
                    coords_bot = get_grid_coords(mouse_pos, MARGIN_LEFT_BOT)
                    if coords_bot:
                        r, c = coords_bot
                        if bot_board.field[r][c] in [2, 3]:
                            game_message = "В цю клітинку вже вистрілено! Обери іншу."
                        else:
                            result = human_player.make_shot(c, r)

                            if result is True:
                                if hasattr(audio, 'play'): audio.play("hit")
                                game_message = f"Влучив у {LETTERS[r]}{c + 1}!"

                                for ship in bot_board.ships:
                                    if (c, r) in ship.coordinates:
                                        ship.hit()  # ВИПРАВЛЕНО з hiten

                                        if ship.defeated():  # ВИПРАВЛЕНО з defeated
                                            if hasattr(audio, 'play'): audio.play("sink")
                                            game_message += " КОРАБЕЛЬ ЗНИЩЕНО!"
                                            bot_board.mark_destroyed_perimeter(ship)
                                            destroyed_bot_ships.append(list(ship.coordinates))

                                            for cx, cy in ship.coordinates:
                                                explosions.append({"x": MARGIN_LEFT_BOT + cx * CELL_SIZE,
                                                                   "y": MARGIN_TOP + cy * CELL_SIZE, "frame": 0})
                                            if bot_brain.is_defeated():
                                                game_state = "GAME_OVER"
                                        break
                            elif result is False:
                                if hasattr(audio, 'play'): audio.play("miss")
                                game_message = "Мимо! "
                                bot_msg = bot_brain.make_turn(player_board, destroyed_ships)
                                game_message += bot_msg

                                if human_player.is_defeated():
                                    game_state = "GAME_OVER"


    screen.blit(background, (0, 0))
    overlay = pygame.Surface((1000, 600), pygame.SRCALPHA)
    overlay.fill((0, 0, 20, 120))
    screen.blit(overlay, (0, 0))
    draw_grid(screen, MARGIN_LEFT_PLAYER, letters_on_right=False)

    if game_state in ["PLAYING", "GAME_OVER"]:
        draw_grid(screen, MARGIN_LEFT_BOT, letters_on_right=True)

    draw_ships(screen, player_board, ship_images, MARGIN_LEFT_PLAYER)

    if game_state == "PLACING":
        arsenal_title = font_large.render("АРСЕНАЛ ФЛОТУ:", True, WHITE)
        screen.blit(arsenal_title, (MARGIN_LEFT_BOT, MARGIN_TOP - 40))

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
                        lx = item["rect"].left + j * CELL_SIZE
                        pygame.draw.line(screen, PANEL_COLOR, (lx, item["rect"].top), (lx, item["rect"].bottom), 1)

        if selected_arsenal_idx is not None:
            mouse_pos = pygame.mouse.get_pos()
            hover_coords = get_grid_coords(mouse_pos, MARGIN_LEFT_PLAYER)
            if hover_coords:
                hr, hc = hover_coords
                length = arsenal[selected_arsenal_idx]["length"]
                img_key = length if current_orientation == "h" else f"v{length}"
                hover_img = ship_images.get(img_key)

                if hover_img:
                    transparent_img = hover_img.copy()
                    transparent_img.set_alpha(150)
                    hx = MARGIN_LEFT_PLAYER + hc * CELL_SIZE
                    hy = MARGIN_TOP + hr * CELL_SIZE
                    screen.blit(transparent_img, (hx, hy))

                hover_ship = Ship(arsenal[selected_arsenal_idx]["length"], current_orientation)
                hover_ship.set_coordinates(hc, hr)

                for x, y in hover_ship.coordinates:
                    if 0 <= x <= 9 and 0 <= y <= 9:
                        hover_surface = pygame.Surface((CELL_SIZE - 4, CELL_SIZE - 4), pygame.SRCALPHA)
                        hover_surface.fill((0, 255, 255, 120))
                        screen.blit(hover_surface,
                                    (MARGIN_LEFT_PLAYER + x * CELL_SIZE + 2, MARGIN_TOP + y * CELL_SIZE + 2))

    if game_state in ["PLAYING", "GAME_OVER"]:
        draw_shots(screen, bot_board, MARGIN_LEFT_BOT)
        draw_shots(screen, player_board, MARGIN_LEFT_PLAYER)


    pygame.draw.rect(screen, PANEL_COLOR, (180, 510, 640, 55), border_radius=15)
    msg_surface = font.render(game_message, True, TEXT_COLOR)
    msg_rect = msg_surface.get_rect(center=(500, 540))
    screen.blit(msg_surface, msg_rect)

    if game_state == "GAME_OVER":
        is_player_win = bot_brain.is_defeated()
        pygame.draw.rect(screen, (20, 20, 30), (250, 180, 500, 220), border_radius=25)
        draw_end_screen(screen, win=is_player_win)

    # Анімація вибухів
    for exp in explosions[:]:
        frame = exp["frame"]
        radius = 5 + frame * 4
        alpha = max(0, 255 - frame * 6)
        surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(surf, (255, 140, 0, alpha), (radius, radius), radius)
        pygame.draw.circle(surf, (255, 255, 0, alpha // 2), (radius, radius), radius // 2)
        screen.blit(surf, (exp["x"] + CELL_SIZE // 2 - radius, exp["y"] + CELL_SIZE // 2 - radius))
        exp["frame"] += 1
        if exp["frame"] > 40:
            explosions.remove(exp)

    pygame.display.flip()

pygame.quit()