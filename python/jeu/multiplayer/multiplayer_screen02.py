import pygame
import pygame_gui

import sys
import math
import random
import json
from collections import deque
import requests
import os
from copy import deepcopy

# WARNING:
# la prochaine L a ete ajoutée au ~/.bashrc
# on a sourcé
# le script maintenant fonctionne
# on a commenté la L ds le ~/.bashrc,
# on a sourcé,
# le script continue de fonctionner
# pourquoi ??? Aucune idée.
# on a pas vérifié que le reste fonctionnait correctement
# export PYTHONPATH="${PYTHONPATH}:/home/sambano/Documents/CDA/PROJET/CDA_project/v0_47/"
from classes.DungeonGame import DungeonGame
from utilitaires import Utilitaires


"""
ecrit ds la collection 'game' de la mongoDB
les documents qui decrivent les stairs d'1 partie multiplayer
"""


class Connect:

    # colors
    TRANSPARENT = pygame.Color(0, 0, 0, 0)
    WHITE = pygame.Color(255, 255, 255)
    BLACK = pygame.Color(0, 0, 0)
    GREEN = pygame.Color(0, 255, 0)
    BLUE = pygame.Color(0, 0, 255)
    YELLOW = pygame.Color(255, 255, 0)
    RED = pygame.Color(255, 0, 0)
    GREY = pygame.Color(128, 128, 128)

    TILE_SIZE = 16

    def __init__(self):

        #
        pygame.init()

        #
        pygame.display.set_caption('multiplayer - screen 02')

        #
        self.screen = pygame.display.set_mode((1000, 800))

        #
        self.manager = pygame_gui.UIManager((1000, 800))

        #
        self.running = False

        #
        self.user_nickname = None
        self.user_tokenForPython = None

        self.response_data = None

        #
        self.dungeon_map = None
        self.map_width = None

        #
        self.game_name = None
        self.white_tiles_array = None
        self.blue_tiles_array = None
        self.total_tiles_array = None
        self.rooms_tiles_array = None
        self.attributes_rooms_array = None

        #
        self.chosen_dict_to_set_exit_tile = None
        self.chosen_dict_to_set_entry_tile = None
        self.white_tiles_array_copy = None
        self.tile_spe_entry_tile_first_stair = None

    # =========================================================================

    def connect(self):
        url = 'https://localhost:8000/test_python'

        # =====================================================================

        # Directory and file checking
        directory = "multiplayer/credentialsToPlay"
        filename = "credentialsToPlay.json"
        filepath = os.path.join(directory, filename)

        # Checking directory existence
        if os.path.exists(directory):
            print("Directory 'multiplayer/credentialsToPlay' exists: yes")
        else:
            print("Directory 'multiplayer/credentialsToPlay' exists: no")

        # Checking file existence
        if os.path.exists(filepath):
            print("File 'multiplayer/credentialsToPlay/credentialsToPlay.json' exists: yes")
        else:
            print(filepath)
            print("File 'multiplayer/credentialsToPlay/credentialsToPlay.json' exists: no")

        # If both directory and file exist, open and read the file
        if os.path.exists(directory) and os.path.exists(filepath):
            with open(filepath, 'r') as file:
                data = json.load(file)
                for key, value in data.items():
                    print(f'{key} => {value}')
                    self.user_nickname = data["user_nickname"]
                    self.user_tokenForPython = data["user_tokenForPython"]

        # =====================================================================

        #
        data = {
            'user_nickname': self.user_nickname,
            'user_tokenForPython': self.user_tokenForPython,
        }

        #
        headers = {'Content-Type': 'application/json'}

        #
        response = requests.post(url,
                                 data=json.dumps(data),
                                 headers=headers,
                                 verify=False)

        print(f'>> Status Code: {response.status_code}')
        print(f'>> Content: {response.content}')

        print(">> valeur de response.text")
        print(response.text)

        #
        self.response_data = response.json()

        #
        if self.response_data['user']['nickname'] == self.user_nickname and \
                self.response_data['user']['tokenForPython'] == self.user_tokenForPython and \
                self.response_data['status']:
            print("CORRESPONDANCE")
            return True

        return False

    # =========================================================================

    """
    Si on arrive a se connecter au controller
    https://localhost:8000/test_python, on fait apparaitre le bouton pr creer
    les variables qui vt contenir les differents stairs au format json
    """
    def ConnectionSuccess(self):
        pygame_gui.elements.UILabel(relative_rect=pygame.Rect((350, 10), (300, 50)),
                                    text='Connection successful!',
                                    manager=self.manager)

        self.btn_to_create_game = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((20, 130), (200, 50)),
                                     text='Create the game',
                                     manager=self.manager)

    # =========================================================================

    """
    Si on n'arrive pas à se connecter
    à https://localhost:8000/test_python
    On fait apparaitre un message
    """
    def ConnectionFailure(self):
        pygame_gui.elements.UILabel(relative_rect=pygame.Rect((350, 10), (300, 50)),
                                    text='A problem occurred.',
                                    manager=self.manager)

    # =========================================================================

    """
    Qd on clique sur le bouton "Create Game"
    """
    def check_entry_text(self):
        print("on cree les variables json pr ensuite les stocker en DB")

        #
        self.game_name = Utilitaires.generate_random_string(self, 20)

        #
        index_fichiers = 1

        # =====================================================================
        # boucle qui genere les stairs et les inscrit ds leur
        # fichier .json respectif
        for i in range(1, 11):
            # print("boucle i:")
            # print(i)

            #
            dungeon_game = DungeonGame(800, 600)

            #
            self.dungeon_map, self.map_width, _ = dungeon_game.generate_next_map()

            #
            self.white_tiles_array, self.blue_tiles_array, self.total_tiles_array = self.get_tile_arrays()

            # fait 1 copie exacte de game.white_tiles_array pr ds la
            # prochaine boucle pvoir definir la tile entree
            # de chacun des stairs
            self.white_tiles_array_copy = deepcopy(self.white_tiles_array)

            #
            self.rooms_tiles_array = self.get_rooms_tiles(self.white_tiles_array)

            #
            self.attributes_rooms_array = self.get_attributes_rooms(self.white_tiles_array)

            # =================================================================
            # ECRITURE DES FICHIERS JSON DE CHAQUE STAIR
            # on decide aussi des differentes tiles qui vt posseder
            # les entrees, les sorties, les items et NPCs
            if self.is_reachable():
                print("stair reachable")

                # Choose a random element to set exit for each stair
                # from self.white_tiles_array
                self.chosen_dict_to_set_exit_tile = random.choice(self.white_tiles_array)
                # print("")
                # print("valeur de chosen_dict_to_set_exit_tile")
                # print(self.chosen_dict_to_set_exit_tile)
                # print("")

                # pr definir l'entree, il faut etre sur que les tiles entree
                # et sortie ne soient pas les memes. Dc pr definir la tile
                # entree, il faut d'abord faire une copie exacte du tableau
                # game.white_tiles_array, (fait au-dessus, en dehors de la
                # boucle, qd on definit les array)
                # supprimer la tile qui a servi a definir la sortie
                # choisir alors 1 tile au hasard pr definir la tile entree
                self.white_tiles_array_copy.remove(self.chosen_dict_to_set_exit_tile)
                self.chosen_dict_to_set_entry_tile = random.choice(self.white_tiles_array_copy)
                # print("")
                # print("valeur de chosen_dict_to_set_entry_tile")
                # print(self.chosen_dict_to_set_entry_tile)
                # print("")

                # on cree 1 variable particuliere pr le 1° stair qui
                # permet de positionner + tard, le joueur au meme
                # emplacement que la "entry_tile"
                if index_fichiers == 1:
                    self.tile_spe_entry_tile_first_stair = self.chosen_dict_to_set_entry_tile
                    # print("")
                    # print("valeur de la self.tile_spe_entry_tile_first_stair")
                    # print(self.tile_spe_entry_tile_first_stair)
                    # print("")

                json_dict = {
                        "game_name": self.game_name,
                        "name": f"stair_{index_fichiers}",
                        "level": f"{index_fichiers}",
                        "exit_tile": self.chosen_dict_to_set_exit_tile,
                        "entry_tile": self.chosen_dict_to_set_entry_tile,
                        "white_tiles_array": self.white_tiles_array,
                        "blue_tiles_array": self.blue_tiles_array,
                        "total_tiles_array": self.total_tiles_array,
                        "rooms_tiles_array": self.rooms_tiles_array,
                        "attributes_rooms_array": self.attributes_rooms_array,
                        }

                # print(json_dict)

                #
                self.send_data_to_symfony(json_dict)

                index_fichiers += 1

            else:
                print("On ne cree pas la variable json")

        # back to previous screen
        self.running = False
        pygame.quit()
        os.system('python3.9 multiplayer/multiplayer_screen01.py')

    # =========================================================================

    def send_data_to_symfony(self, json_dict):

        #
        url = 'http://localhost:8000/test_python_insert_map_to_db'

        #
        headers = {'Content-Type': 'application/json'}

        #
        response = requests.post(url,
                                 data=json.dumps(json_dict),
                                 headers=headers,
                                 verify=False)

        # You can check the status of the request and handle accordingly
        if response.status_code == 200:
            print("Data sent successfully")
        else:
            print("Failed to send data")

    # =========================================================================

    def is_reachable(self):
        if not self.total_tiles_array:
            return False

        # Pick a random tile
        start_tile = random.choice(self.total_tiles_array)

        # Create a set of all tiles for fast lookup
        all_tiles = set((tile["x"], tile["y"]) for tile in self.total_tiles_array)

        # Set of tiles that have been reached
        reached_tiles = set()

        # Queue for the flood fill
        queue = deque([start_tile])

        while queue:
            current_tile = queue.popleft()
            if (current_tile["x"], current_tile["y"]) not in reached_tiles:
                reached_tiles.add((current_tile["x"], current_tile["y"]))

                # Add neighbors to the queue
                for neighbor in self.get_neighbors(current_tile):
                    if (neighbor["x"], neighbor["y"]) in all_tiles:
                        queue.append(neighbor)

        # Check if all tiles were reached
        # return reached_tiles == all_tiles
        if len(reached_tiles) == len(all_tiles):
            return True
        else:
            return False

    # =========================================================================

    def get_neighbors(self, tile):
        x, y = tile['x'], tile['y']
        return [{"x": x - self.TILE_SIZE, "y": y},
                {"x": x + self.TILE_SIZE, "y": y},
                {"x": x, "y": y - self.TILE_SIZE},
                {"x": x, "y": y + self.TILE_SIZE}]

    # =========================================================================

    def get_rooms_tiles(self, white_tiles_array):
        if not white_tiles_array:
            return []

        all_tiles = set((tile["x"], tile["y"]) for tile in white_tiles_array)
        visited_tiles = set()
        rooms = []

        for tile in white_tiles_array:
            if (tile["x"], tile["y"]) not in visited_tiles:
                room_tiles = set()
                queue = deque([tile])
                while queue:
                    current_tile = queue.popleft()
                    if (current_tile["x"], current_tile["y"]) not in visited_tiles:
                        visited_tiles.add((current_tile["x"], current_tile["y"]))
                        room_tiles.add((current_tile["x"], current_tile["y"]))

                        for neighbor in self.get_neighbors(current_tile):
                            if (neighbor["x"], neighbor["y"]) in all_tiles:
                                queue.append(neighbor)

                rooms.append(list(room_tiles))

        return rooms

    # =========================================================================

    def get_attributes_rooms(self, white_tiles_array):
        if not white_tiles_array:
            return []

        all_tiles = set((tile["x"], tile["y"]) for tile in white_tiles_array)
        visited_tiles = set()
        rooms = []

        for tile in white_tiles_array:
            if (tile["x"], tile["y"]) not in visited_tiles:
                room_tiles = set()
                queue = deque([tile])
                while queue:
                    current_tile = queue.popleft()
                    if (current_tile["x"], current_tile["y"]) not in visited_tiles:
                        visited_tiles.add((current_tile["x"], current_tile["y"]))
                        room_tiles.add((current_tile["x"], current_tile["y"]))

                        for neighbor in self.get_neighbors(current_tile):
                            if (neighbor["x"], neighbor["y"]) in all_tiles:
                                queue.append(neighbor)

                min_x = min(tile[0] for tile in room_tiles)
                max_x = max(tile[0] for tile in room_tiles)
                min_y = min(tile[1] for tile in room_tiles)
                max_y = max(tile[1] for tile in room_tiles)

                room_width = max_x - min_x + self.TILE_SIZE
                room_height = max_y - min_y + self.TILE_SIZE

                center_x = min_x + room_width / 2
                center_y = min_y + room_height / 2

                rooms.append({
                    "x": min_x,
                    "y": min_y,
                    "width": room_width,
                    "height": room_height,
                    "center": (center_x, center_y),
                    "tiles": list(room_tiles)
                })

        return rooms

    # =========================================================================

    def get_tile_arrays(self, tile_size=(TILE_SIZE, TILE_SIZE)):
        white_tiles = []
        blue_tiles = []
        total_tiles = []

        for i in range(len(self.dungeon_map)):
            if self.dungeon_map[i] == 0:
                continue

            #
            map_x, map_y = (i % self.map_width, math.trunc(i / self.map_width))

            tile_info = {"x": map_x * tile_size[0],
                         "y": map_y * tile_size[1],
                         "w": tile_size[0],
                         "h": tile_size[1],
                         "center": ((map_x * tile_size[0]) + tile_size[0] / 2,
                                    (map_y * tile_size[1]) + tile_size[1] / 2),
                         }

            if self.dungeon_map[i] == 1:
                tile_info["color"] = "white"
                white_tiles.append(tile_info)
                total_tiles.append(tile_info)
            elif self.dungeon_map[i] == 2:
                tile_info["color"] = "blue"
                blue_tiles.append(tile_info)
                total_tiles.append(tile_info)

        return white_tiles, blue_tiles, total_tiles

    # =========================================================================

    def prepare_GUI(self):

        # =====================================================================

        connection_status = self.connect()

        # =====================================================================

        if connection_status:
            self.ConnectionSuccess()
        else:
            self.ConnectionFailure()

        # =====================================================================

        self.running = True
        while self.running:

            time_delta = pygame.time.Clock().tick(60)/1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.btn_to_create_game:
                        self.check_entry_text()

                self.manager.process_events(event)

            if self.running:
                self.manager.update(time_delta)
                self.screen.fill((0, 0, 0))
                self.manager.draw_ui(self.screen)
                pygame.display.update()


if __name__ == '__main__':
    # print("package value from multiplayer_screen01.py")
    # print(__package__)
    connect_obj = Connect()
    connect_obj.prepare_GUI()
