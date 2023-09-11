# Create_your_character.py
import pygame
import pygame_gui
import sys
import random
import os
import json


def create_your_character():
    pygame.init()

    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('Monoplayer: Create your character')

    clock = pygame.time.Clock()

    manager = pygame_gui.UIManager((640, 480))

    save_folder = 'save'

    pygame_gui.elements.UILabel(relative_rect=pygame.Rect((225, 50), (350, 30)), 
                                text='Please enter a name for your player',
                                manager=manager)

    player_name_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((225, 85), (250, 30)),
                                manager=manager)

    pygame_gui.elements.UILabel(relative_rect=pygame.Rect((225, 120), (250, 30)), 
                                text='Your life will be 100%',
                                manager=manager)

    pygame_gui.elements.UILabel(relative_rect=pygame.Rect((225, 155), (250, 30)), 
                                text='Your attack will be 100%',
                                manager=manager)

    pygame_gui.elements.UILabel(relative_rect=pygame.Rect((225, 190), (250, 30)), 
                                text='Your defense will be 100%',
                                manager=manager)

    pygame_gui.elements.UILabel(relative_rect=pygame.Rect((225, 225), (250, 30)), 
                                text='Your life will be 100%',
                                manager=manager)

    pygame_gui.elements.UILabel(relative_rect=pygame.Rect((225, 260), (250, 30)), 
                                text='Your magic will be 100%',
                                manager=manager)

    pygame_gui.elements.UILabel(relative_rect=pygame.Rect((225, 295), (250, 30)), 
                                text='Your strength will be:',
                                manager=manager)

    strength_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((225, 330), (250, 30)), 
                                                 text='Please, roll dices',
                                                 manager=manager)

    roll_dice_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((225, 365), (250, 50)),
                                                   text='Roll Dices',
                                                   manager=manager)

    start_game_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((225, 420), (250, 50)),
                                                     text='Start your game',
                                                     manager=manager)
    start_game_button.hide()

    running = True
    while running:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == roll_dice_button:
                    strength_label.set_text(str(random.randint(0, 100)))

                if event.ui_element == start_game_button:
                    if not os.path.exists(save_folder):
                        os.makedirs(save_folder)
                    else:
                        print("Save folder already exists")

                    if os.path.exists("save/stairs_json"):
                        print("")
                        print("le dossier save/stairs_json existe deja")
                        print("")

                        # effacer les eventuels fichiers presents
                        # ds save/stairs_json
                        # List elements in "save" folder
                        files_in_save_folder = os.listdir('save/stairs_json')

                        if len(files_in_save_folder) == 0:
                            print("Save/stairs_json folder is empty.")
                        else:
                            print("Save/stairs_json folder is not empty, we just deleted files.")

                            for file in files_in_save_folder:
                                file_path = os.path.join('save', file)
                                if os.path.isfile(file_path):
                                    os.remove(file_path)
                            print("All files have been removed from the 'save/stairs_json' folder.")
                    else:
                        print("")
                        print("le dossier save/stairs_json n'existe pas")
                        print("il faut le creer")
                        print("")

                        try:
                            os.mkdir("save/stairs_json")
                            print("Directory created successfully.")
                        except OSError as error:
                            print(f"Failed to create directory: {error}")
                            pygame.quit()
                            sys.exit()

                    # Define player dictionary
                    player_data = {
                        'name': player_name_entry.get_text(),
                        'strength': int(strength_label.text),
                        'attack': 100,
                        'defense': 100,
                        'life': 100,
                        'magic': 100,
                        'position': (0, 0),
                        'color': (0, 255, 0),
                        'radius': 8,
                        'speed': 16,
                        'stair_actuel': 'save/stairs_json/stair_1.json'
                    }

                    # Write player data to JSON file
                    with open(os.path.join(save_folder, 'player.json'), 'w') as json_file:
                        json.dump(player_data, json_file, indent=4)

                    pygame.quit()
                    os.system('python3.9 monoplayer02.py')
                    running = False

            manager.process_events(event)

        # Perform the check for both conditions every frame
        if player_name_entry.get_text() != '' and strength_label.text != 'Please, roll dices':
            start_game_button.show()

        if running:
            manager.update(time_delta)
            screen.fill((0, 0, 0))
            manager.draw_ui(screen)
            pygame.display.update()


if __name__ == '__main__':
    create_your_character()
