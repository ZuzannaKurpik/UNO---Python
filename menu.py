import pygame, sys, os
from game import game_loop

pygame.init()

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % (5, 30)

screen_W, screen_H = 400, 300
menu_screen = pygame.display.set_mode((520, 400))
pygame.display.set_caption("Menu")

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DPURPLE = (52, 28, 71)
LAVENDER = (192, 107, 225)
SKY = (177, 227, 255)
LGREEN = (179, 255, 202)
BLACK = (0, 0, 0)
LGREY = (219, 219, 219)

player_name = ["", "", "", ""]
name_inpust_boxses = [pygame.Rect(370, 125 + i*50, 100, 30) for i in range(4)]
active_input_box = None

menu_buttons = [pygame.Rect(150 + (i%3)*70, (i//3)*50 +125, 65, 30) for i in range(4*3)]
menu_button_tekst = ['Normal' if i%3 == 0 else 'Robot' if i%3 == 1 else 'X' for i in range(4*3)]
menu_button_colors = [LGREY]*12

menu_buttons.append(pygame.Rect(152, 320, 200, 40))
menu_button_tekst.append("Start")
menu_button_colors.append(LGREY)
player_types = ["X", "X", "X", "X"]

def draw_buttons():
    font = pygame.font.Font(r'C:\Windows\Fonts\COLONNA.ttf', 35)
    lines = ["  Welcome to the UNO Game.", "Please choice the Players types ", "  before you start The Game"]
    for i, line in enumerate(lines):
        text = font.render(line, False, SKY)
        menu_screen.blit(text, (25, i * font.get_height()))

    for i, button in enumerate(menu_buttons):
        pygame.draw.rect(menu_screen, menu_button_colors[i], button)
        font = pygame.font.Font(r'C:\Windows\Fonts\CENTURY.ttf', 18)
        text = font.render(menu_button_tekst[i], False, BLACK)
        text_rect = text.get_rect(center=button.center)
        menu_screen.blit(text, text_rect)
    for i, box in enumerate(name_inpust_boxses):
        pygame.draw.rect(menu_screen, WHITE, box, 2)
        font = pygame.font.Font(r'C:\Windows\Fonts\CENTURY.ttf', 18)
        text = font.render(player_name[i], False, WHITE)
        menu_screen.blit(text, (box.x+5, box.y+5))
    for i in range(4):
        font = pygame.font.Font(r'C:\Windows\Fonts\COLONNA.ttf', 35)
        text = font.render(f"Player {i+1}:", False, LAVENDER)
        menu_screen.blit(text, (10, i*50 +120))

    font = pygame.font.Font(r'C:\Windows\Fonts\COLONNA.ttf', 20)
    text = font.render("Normal - you play;  Robot - I play;  X - delete", False, SKY)
    menu_screen.blit(text, (50, 375))

def menu_loop():
    global active_input_box
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                active_input_box = None
                for i, box in enumerate(name_inpust_boxses):
                    if box.collidepoint(mouse_pos):
                        active_input_box = i
                        break
                for i, button in enumerate(menu_buttons):
                    if button.collidepoint(mouse_pos):
                        if i < 12:
                            for j in range(i // 3 * 3, i // 3 * 3 + 3):
                                menu_button_colors[j] = LGREY
                            player_types[i // 3] = 'Normal' if i % 3 == 0 else 'Robot' if i % 3 == 1 else 'X'
                            menu_button_colors[i] = LGREEN
                        else:
                            start_game()
                            return
            elif event.type == pygame.KEYDOWN:
                if active_input_box is not None:
                    if event.key == pygame.K_BACKSPACE:
                        player_name[active_input_box] = player_name[active_input_box][:-1]
                    else:
                        player_name[active_input_box] += event.unicode

        menu_screen.fill(DPURPLE)
        draw_buttons()
        pygame.display.flip()


def start_game():
    print("Starting game with the following choices:")
    for i in range(4):
        print(f"Player {i + 1}: {player_types[i]}, Name: {player_name[i]}")

    menu_screen = pygame.display.set_mode((1530, 780))
    # position = pygame.display.Info()
    game_loop(player_types, menu_screen, player_name)


if __name__ == "__main__":
    menu_loop()