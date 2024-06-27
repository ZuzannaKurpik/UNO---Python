import random, sys, pygame

from player import Player, Robot

pygame.init()
buttons = []


def game_loop(player_types, screen, player_name):
    global buttons
    players = []

    number = 1
    for i in player_types:
        if i == "Normal":
            players.append(Player(number))
        elif i == "Robot":
            players.append(Robot(number))
        number += 1

    talia = dect.copy()
    shuffle_deck(talia)
    unfold(talia, players)

    pygame.display.set_caption("Game : UNO")

    color_dict = {'B': BLUE, 'G': GREEN, 'Y': YELLOW, 'R': RED}
    font = pygame.font.Font(None, 26)
    color_buttons = [pygame.Rect(600, 300 + i*70, 50, 50) for i in range(4)]
    color_button_colors = [BLUE, GREEN, YELLOW, RED]
    choosing_color = False
    card_width = 70
    cards_per_row = 9

    current_player = 1
    reveal_cards = 1
    direction = 1

    next_button = pygame.Rect(screen.get_width() //2 + 100, screen.get_height() // 2 + 100, 100, 30)
    draw_card_button = pygame.Rect(screen.get_width() // 2 + 100, screen.get_height() // 2 + 140, 100, 30)
    uno_button = pygame.Rect(screen.get_width() // 2 + 100, screen.get_height() // 2 + 180, 100, 30)

    invalid_move_message = None
    uno_player = []

    while True:
        first_card = talia[0]
        if first_card[0].isdigit():
            last_card = first_card
            talia.pop(0)
            break
        else:
            talia.append(talia.pop(0))

    while True:
        winner = check_for_winner(players)
        if winner is not None:
            pygame.display.quit()
            winner_player = f"{winner.number} {player_name[winner.number-1]}"
            display_winner(winner_player)
            break

        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if next_button.collidepoint(mouse_pos):
                    if not current_player in uno_player and len(players[current_player-1].cards) == 1:
                        players[current_player - 1].add_card(talia[0])
                        players[current_player - 1].add_card(talia[1])
                        players[current_player - 1].add_card(talia[2])
                        players[current_player - 1].add_card(talia[3])
                        players[current_player - 1].add_card(talia[4])
                        players[current_player - 1].sort_cards()
                        talia.pop()
                        talia.pop()
                        talia.pop()
                        talia.pop()
                        talia.pop()
                        invalid_move_message = f"Player {current_player} You don't say uno!!!"

                    if reveal_cards == 0:
                        current_player = (current_player + direction - 1) % len(players) + 1
                        reveal_cards = 1
                    else:
                        reveal_cards = 0
                elif draw_card_button.collidepoint(mouse_pos):
                    if len(dect) == 0:
                        talia.extend(dect)
                        for player in players:
                            for card in player.cards:
                                talia.remove(card)
                        talia.remove(last_card)
                        shuffle_deck(talia)
                    players[current_player - 1].add_card(talia[0])
                    players[current_player - 1].sort_cards()
                    talia.pop(0)
                    reveal_cards = 0
                    if current_player in uno_player and len(players[current_player -1].cards) > 1:
                        uno_player.remove(current_player)

                elif uno_button.collidepoint(mouse_pos):
                    if len(players[current_player-1].cards) == 1 and not current_player in uno_player:
                        uno_player.append(current_player)
                    else:
                        invalid_move_message = "You can't say UNO"
                elif choosing_color:
                    for i, button in enumerate(color_buttons):
                        if button.collidepoint(mouse_pos):
                            color_codes = ["B", "G", "Y", "R"]
                            last_card = last_card[0] + color_codes[i]
                            choosing_color = False
                            reveal_cards = 0
                else:
                    for i, player in enumerate(players):
                        for j, card in enumerate(player.cards):
                            row = j // cards_per_row
                            col = j % cards_per_row
                            if i == 0:  # Gracz na dole ekranu
                                start_x = (screen.get_width() - min(len(player.cards), cards_per_row) * card_width) // 2
                                x = start_x + col * card_width
                                y = row * card_width
                            elif i == 1:  # Gracz po prawej stronie ekranu
                                start_y = (screen.get_height() - min(len(player.cards), cards_per_row) * card_width) // 2
                                x = screen.get_width() - card_width - (row * card_width)
                                y = start_y + col * card_width
                            elif i == 2:  # Gracz na górze ekranu
                                start_x = (screen.get_width() - min(len(player.cards), cards_per_row) * card_width) // 2
                                x = start_x + col * card_width
                                y = screen.get_height() - (row + 1) * card_width
                            else:  # Gracz po lewej stronie ekranu
                                start_y = (screen.get_height() - min(len(player.cards), cards_per_row) * card_width) // 2
                                x = row * card_width
                                y = start_y + col * card_width

                            card_rect = pygame.Rect(x, y, 60, 60)
                            if card_rect.collidepoint(mouse_pos):
                                if reveal_cards == 0 or current_player != player.number:
                                    invalid_move_message = "It's not your tourn"
                                elif last_card is not None and card[0] != last_card[0] and card[1] != last_card[1] and card not in ["CC", "PF"]:
                                    invalid_move_message = "You cannot play this card."
                                else:
                                    if card[0] == "R" and last_card[1] == card[1]:
                                        if direction == 1:
                                            direction = -1
                                        elif direction == -1:
                                            direction = 1
                                    elif card[0] == "B" and card[1] == last_card[1]:
                                        current_player = (current_player + direction -1) % len(players) + 1
                                    elif card[0] == "P" and not card[1] == "F" and card[1] == last_card[1]:
                                        next_palyer = (current_player + direction -1) % len(players) + 1
                                        players[next_palyer -1].add_card(talia[0])
                                        players[next_palyer -1].add_card(talia[1])
                                        players[next_palyer -1].sort_cards()
                                        talia.pop()
                                        talia.pop()
                                    elif card == "CC":
                                        choosing_color = True
                                    elif card == "PF":
                                        next_palyer = (current_player + direction - 1) % len(players) + 1
                                        players[next_palyer - 1].add_card(talia[0])
                                        players[next_palyer - 1].add_card(talia[1])
                                        players[next_palyer - 1].add_card(talia[2])
                                        players[next_palyer - 1].add_card(talia[3])
                                        players[next_palyer - 1].sort_cards()
                                        talia.pop()
                                        talia.pop()
                                        talia.pop()
                                        talia.pop()
                                        choosing_color = True

                                    # current_player += direction
                                    last_card = card
                                    players[i].cards.pop(j)
                                    invalid_move_message = None
                                    if not choosing_color:
                                        reveal_cards = 0
                                break


        screen.fill((BACKROUND))

        if last_card is not None:
            color = color_dict.get(last_card[1], WHITE)
        else:
            color = WHITE
        pygame.draw.rect(screen, color, pygame.Rect(screen.get_width() // 2 - 100, screen.get_height() // 2 - 100, 200, 200))

        pygame.draw.rect(screen, BLACK, next_button)
        pygame.draw.rect(screen, BLACK, draw_card_button)
        pygame.draw.rect(screen, BLACK, uno_button)
        next_text = font.render("Next", True, WHITE)
        draw_card_text = font.render("Draw Card", True, WHITE)
        uno_text = font.render("UNO", True, WHITE)
        screen.blit(next_text, (next_button.x + 30, next_button.y + 10))
        screen.blit(draw_card_text, (draw_card_button.x + 10, draw_card_button.y + 10))
        screen.blit(uno_text, (uno_button.x + 30, uno_button.y + 10))

        for i, player in enumerate(players):
            for j, card in enumerate(player.cards):
                row = j // cards_per_row
                col = j % cards_per_row
                if i == 0:  # Gracz na dole ekranu
                    start_x = (screen.get_width() - min(len(player.cards), cards_per_row) * card_width) // 2
                    x = start_x + col * card_width
                    y = row * card_width
                elif i == 1:  # Gracz po prawej stronie ekranu
                    start_y = (screen.get_height() - min(len(player.cards), cards_per_row) * card_width) // 2
                    x = screen.get_width() - card_width - (row * card_width)
                    y = start_y + col * card_width
                elif i == 2:  # Gracz na górze ekranu
                    start_x = (screen.get_width() - min(len(player.cards), cards_per_row) * card_width) // 2
                    x = start_x + col * card_width
                    y = screen.get_height() - (row + 1) * card_width
                else:  # Gracz po lewej stronie ekranu
                    start_y = (screen.get_height() - min(len(player.cards), cards_per_row) * card_width) // 2
                    x = row * card_width
                    y = start_y + col * card_width

                if player_types[current_player-1] == "Robot":
                    color = BLACK
                    text = None
                else:
                    if player.number == current_player and reveal_cards == 1:
                        color = color_dict.get(card[1], WHITE)
                        text = font.render(card, True, BLACK)
                    else:
                        color = BLACK
                        text = None

                pygame.draw.rect(screen, color, pygame.Rect(x, y, 60, 60))
                pygame.draw.rect(screen, WHITE, pygame.Rect(x, y, 60, 60), 2)
                if text is not None:
                    screen.blit(text, (x+5, y+5))

            player_name_text = font.render(f"Player {player.number} : {player_name[i]}", True, BLACK)
            if i == 1:
                screen.blit(player_name_text, (x - 80, y + 70))
            elif i == 3:
                screen.blit(player_name_text, (x + 10, y + 70))
            else:
                screen.blit(player_name_text, (x, y+75 if i < 2 else y - 20))

        current_player_text = font.render(f"Current Player: {current_player} {player_name[current_player - 1]}", True, BLACK)
        screen.blit(current_player_text, (screen.get_width() // 2 - 50, screen.get_height() // 2 + 220))

        uno_player_text = font.render(f"Uno players: {uno_player}", True, BLACK)
        screen.blit(uno_player_text, (next_button.x - 200, next_button.y))

        if last_card is not None:
            color = color_dict.get(last_card[1], WHITE)
            pygame.draw.rect(screen, color, pygame.Rect(screen.get_width() // 2 - 30, screen.get_height() // 2 - 30, 60, 60))
            pygame.draw.rect(screen, BLACK, pygame.Rect(screen.get_width() // 2 - 30, screen.get_height() // 2 - 30, 60, 60), 2)
            text = font.render(last_card, True, BLACK)
            screen.blit(text, (screen.get_width() // 2 - 25, screen.get_height() // 2 - 25))

        if invalid_move_message is not None:
            invalid_move_text = font.render(invalid_move_message, True, RED)
            screen.blit(invalid_move_text, (screen.get_width() // 2 - 50, screen.get_height() // 2 + 260))

        if direction == -1:
            pygame.draw.polygon(screen, BLACK, [(screen.get_width() // 2 + 105, screen.get_height() // 2),
                                                (screen.get_width() // 2 + 125, screen.get_height() // 2 - 10),
                                                (screen.get_width() // 2 + 125, screen.get_height() // 2 + 10)])
        else:
            pygame.draw.polygon(screen, BLACK, [(screen.get_width() // 2 + 125, screen.get_height() // 2),
                                                (screen.get_width() // 2 + 105, screen.get_height() // 2 - 10),
                                                (screen.get_width() // 2 + 105, screen.get_height() // 2 + 10)])

        if choosing_color:
            for i, button in enumerate(color_buttons):
                pygame.draw.rect(screen, color_button_colors[i], button)

        if player_types[current_player-1] == "Robot" and reveal_cards == 0:
            pygame.time.wait(500)
            robot_card = players[current_player -1].play_card(last_card)
            next_palyer = (current_player + direction - 1) % len(players) + 1
            if robot_card is None:
                if len(dect) == 0:
                    talia.extend(dect)
                    for player in players:
                        for card in player.cards:
                            talia.remove(card)
                    talia.remove(last_card)
                    shuffle_deck(talia)
                players[current_player - 1].add_card(talia[0])
                players[current_player - 1].sort_cards()
                talia.pop(0)
                invalid_move_message = f"Robot draw new card"
            else:
                invalid_move_message = f"Robot play card {robot_card}"

                if robot_card[0] == "P" and not robot_card[1] == "F":
                    players[next_palyer - 1].add_card(talia[0])
                    players[next_palyer - 1].add_card(talia[1])
                    players[next_palyer - 1].sort_cards()
                    talia.pop()
                    talia.pop()
                    current_player = (current_player + direction - 1) % len(players) + 1
                elif robot_card == "PF":
                    players[next_palyer - 1].add_card(talia[0])
                    players[next_palyer - 1].add_card(talia[1])
                    players[next_palyer - 1].add_card(talia[2])
                    players[next_palyer - 1].add_card(talia[3])
                    players[next_palyer - 1].sort_cards()
                    talia.pop()
                    talia.pop()
                    talia.pop()
                    talia.pop()
                    current_player = (current_player + direction - 1) % len(players) + 1
                    for c in players[current_player-1].cards:
                        if not c[1] == "F" or not c[1] == "C":
                            robot_card = "P" + c[1]
                            break
                elif robot_card[0] == "B":
                    current_player = (current_player + direction - 1) % len(players) + 1
                elif robot_card[0] == "R":
                    if direction == 1:
                        direction = -1
                    elif direction == -1:
                        direction = 1

                last_card = robot_card
            pygame.time.wait(500)
            current_player = (current_player + direction - 1) % len(players) + 1
            reveal_cards = 1

            if len(players[current_player-1].cards) == 1:
                uno_player.append(current_player)
            elif current_player in uno_player and len(players[current_player -1].cards) > 1:
                uno_player.remove(current_player)

        legend_text = '"B" - block, "P color" - +2, "R" - reverse, "PF" - +4, "CC" - change color'
        line_surface = font.render(legend_text, True, BLACK)
        screen.blit(line_surface, (screen.get_width() // 2 - 230, screen.get_height() // 2 - 125))

        pygame.display.flip()

dect = ["0B", "1B", "2B", "3B", "4B", "5B", "6B", "7B", "8B", "9B", "BB", "PB", "RB",
        "0B", "1B", "2B", "3B", "4B", "5B", "6B", "7B", "8B", "9B", "BB", "PB", "RB",
        "0Y", "1Y", "2Y", "3Y", "4Y", "5Y", "6Y", "7Y", "8Y", "9Y", "BY", "PY", "RY",
        "0Y", "1Y", "2Y", "3Y", "4Y", "5Y", "6Y", "7Y", "8Y", "9Y", "BY", "PY", "RY",
        "0R", "1R", "2R", "3R", "4R", "5R", "6R", "7R", "8R", "9R", "BR", "PR", "RR",
        "0R", "1R", "2R", "3R", "4R", "5R", "6R", "7R", "8R", "9R", "BR", "PR", "RR",
        "0G", "1G", "2G", "3G", "4G", "5G", "6G", "7G", "8G", "9G", "BG", "PG", "RG",
        "0G", "1G", "2G", "3G", "4G", "5G", "6G", "7G", "8G", "9G", "BG", "PG", "RG",
        "CC", "CC", "CC", "CC", "PF", "PF", "PF", "PF"]

BLUE = (15, 226, 255)
GREEN = (130, 255, 90)
YELLOW = (255, 222, 68)
RED = (255, 77, 77)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BACKROUND = (110, 80, 74)

DPURPLE = (52, 28, 71)
LAVENDER = (192, 107, 225)
SKY = (177, 227, 255)
LGREEN = (179, 255, 202)
LGREY = (219, 219, 219)

def unfold(dect, players):
    for i in range(8):
        for player in players:
            player.add_card(card=dect[0])
            dect.pop(0)
    for p in players:
        p.sort_cards()


def shuffle_deck(deck):
    for i in range(4):
        random.shuffle(deck)


def check_for_winner(players):
    for p in players:
        if len(p.cards) == 0:
            return p
    return None


def display_winner(winner):
    pygame.init()
    winner_screen = pygame.display.set_mode((520, 400))
    pygame.display.set_caption("Winner")

    font = pygame.font.Font(r'C:\Windows\Fonts\COLONNA.ttf', 35)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        winner_screen.fill(DPURPLE)
        text = font.render(f"The winner is: {winner}", False, SKY)
        winner_screen.blit(text, (25, font.get_height()))
        pygame.display.flip()