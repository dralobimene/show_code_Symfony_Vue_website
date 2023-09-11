# monoplayer_game.py
import pygame
import pygame_gui
import sys
import os
import shutil


def monoplayer_game():
    pygame.init()

    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('Monoplayer Game')

    clock = pygame.time.Clock()

    manager = pygame_gui.UIManager((640, 480))

    button_create_character = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((225, 175), (350, 50)),
                                          text='Start Game Creating Your Character',
                                          manager=manager)

    button_run_your_save = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((225, 250), (350, 50)),
                                                text='Run your save',
                                                manager=manager)

    running = True
    while running:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == button_create_character:
                    print("on lance 1 nvelle partie")
                    print("Il faut ecrire la verif du fichier save/player.json")
                    print("qui ne doit pas exister puisqu'on lance 1 nvelle")
                    print("partie")
                    print("")

                    # effacer les eventuels fichiers presents
                    # ds save/stairs_json
                    # List elements in "save" folder
                    if os.path.exists("save/stairs_json"):
                        print("The 'save/stairs_json' directory exists.")

                        files_in_save_folder = os.listdir('save/stairs_json')

                        if len(files_in_save_folder) == 0:
                            print("Save/stairs_json folder is empty.")
                        else:
                            print("Save/stairs_json folder is not empty, we just deleted files.")
                            for file in files_in_save_folder:
                                file_path = os.path.join('save/stairs_json', file)
                                if os.path.isfile(file_path):
                                    os.remove(file_path)
                            print("All files have been removed from the 'save/stairs_json' folder.")

                    pygame.quit()
                    os.system('python3.9 Create_your_character.py')
                    running = False

                # =============================================================

                if event.ui_element == button_run_your_save:
                    pygame.quit()

                    # on verifie que le fichier save/player.json
                    # existe
                    if os.path.exists("save/player.json"):
                        print("")
                        print("le fichier save/player.json existe")
                        print("on peut continuer")
                        print("")
                    else:
                        print("")
                        print("le fichier save/player.json n'existe pas")
                        print("02: Exit program")
                        print("")

                        pygame.quit()
                        sys.exit()

                    # on verifie que le dossier save/stairs_json
                    # existe
                    if os.path.exists("save/stairs_json"):
                        print("")
                        print("le dossier save/stairs_json existe")
                        print("on peut continuer")
                        print("")
                    else:
                        print("")
                        print("le dossier save/stairs_json n'existe pas")
                        print("01: Exit program")
                        print("")

                        pygame.quit()
                        sys.exit()

                    pygame.quit()
                    os.system('python3.9 monoplayer02_fromsavegame.py')
                    running = False

            manager.process_events(event)

        if running:
            manager.update(time_delta)
            screen.fill((0, 0, 0))
            manager.draw_ui(screen)
            pygame.display.update()


if __name__ == '__main__':
    monoplayer_game()
