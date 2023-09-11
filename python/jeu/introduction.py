# introduction.py
import pygame
import pygame_gui
import sys
import os


def introduction():
    pygame.init()

    screen = pygame.display.set_mode((640, 480))

    pygame.display.set_caption('Introduction')

    clock = pygame.time.Clock()

    manager = pygame_gui.UIManager((640, 480))

    button_multiplayer_game = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((225, 175), (250, 50)),
                                                text='Start Multiplayer Game',
                                                manager=manager)

    button_monoplayer_game = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((225, 250), (250, 50)),
                                                text='Start Monoplayer Game',
                                                manager=manager)

    button_internet_post_comment = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((225, 325), (250, 50)), text='Internet, post a comment', manager=manager)



    button_quit_game = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((225, 400), (250, 50)),
                                                text='Quit Game',
                                                manager=manager)

    running = True
    while running:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == button_multiplayer_game:
                    pygame.quit()
                    os.system('python3.9 multiplayer_game.py')
                    running = False
                if event.ui_element == button_monoplayer_game:
                    pygame.quit()
                    os.system('python3.9 monoplayer_game.py')
                    running = False
                if event.ui_element == button_quit_game:
                    pygame.quit()
                    sys.exit()
                if event.ui_element == button_internet_post_comment:
                    pygame.quit()
                    os.system('python3.9 internet_post_comment.py')
                    running = False

            manager.process_events(event)

        if running:
            manager.update(time_delta)
            screen.fill((0, 0, 0))
            manager.draw_ui(screen)
            pygame.display.update()


if __name__ == '__main__':
    introduction()
