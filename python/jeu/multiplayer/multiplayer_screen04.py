import pygame
import pygame_gui
import sys
import requests
import json
import os
from collections import OrderedDict

from utilitaires import Utilitaires
from utilitaires_no_player import UtilitairesNoPlayer
from utilitaires import EventManager

from utilitaires_multiplayer import UtilitairesMultiplayer

from classes.FileProcessor import FileProcessor
from classes.KeyHandler import KeyHandler

from classes.InformationsPanel import InformationsPanel
from classes.StartMenuFromSavedGame import StartMenuFromSavedGame

from classes.Player import Player

from classes.WebSocketClient import WebSocketClient
import threading


"""
Recupere 1 document de la collection 'game' de la mongoDB
l'ecrit ds 1 fichier json (multiplayer/save/stairs_json/)
puis affiche la carte selon ce fichier
creer un player qui doit etre envoyé au server.ts
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
        pygame.display.set_caption('multiplayer - screen 04')

        #
        self.screen = pygame.display.set_mode((1000, 800))

        #
        self.manager = pygame_gui.UIManager((1000, 800))

        #
        self.running = False

        #
        self.user_nickname = None
        self.user_tokenForPython = None

        #
        self.response_data = None

        #
        self.game_id = None

        #
        self.exit_tile = None
        self.entry_tile = None
        self.white_tiles = None
        self.blue_tiles = None
        self.total_tiles_list = None
        self.rooms_tiles_list = None
        self.attributes_rooms_list = None

        #
        self.utilitairesNoPlayer = UtilitairesNoPlayer()

        #
        self.utilitairesMultiplayer = UtilitairesMultiplayer()

        #
        self.event_manager = EventManager(self)

        # pr les evts clavier qui ne st pas les touches directionnelles
        # self.key_handler = KeyHandler(self.player)

        #
        self.canvas01_maps = pygame.Surface((800, 600))
        self.canvas01_maps.fill((0, 0, 0))

        #
        self.canvas02_buttons = pygame.Surface((200, 800))
        self.canvas02_buttons.fill((128, 128, 128))

        #
        self.canvas03_informations = pygame.Surface((800, 200))
        self.canvas03_informations.fill((255, 255, 255))

        #
        self.canvas04_npcs = pygame.Surface((800, 600), pygame.SRCALPHA, 32).convert_alpha()
        self.canvas04_npcs.fill((0, 0, 0))

        #
        self.canvas05_items = pygame.Surface((800, 600), pygame.SRCALPHA, 32).convert_alpha()
        self.canvas05_items.fill((0, 0, 0))

        #
        self.clock = pygame.time.Clock()

        #
        self.dungeon_map = None

        #
        self.map_width = None

        #
        self.save_button = None

        #
        self.json_files_sorted = None

        #
        self.websocket_thread = threading.Thread(target=self.start_websocket)
        self.websocket_thread.start()

        #
        self.player = None

        #
        self.current_player_state = None

        # Initialize previous player state
        self.previous_player_state = None

        #
        self.other_players = None

        #
        self.other_players_instances = {}

        #
        self.previous_other_players = None

        #
        self.liste_npcs = OrderedDict()

        #
        self.liste_items = OrderedDict()

    # =========================================================================

    def start_websocket(self):
        self.websocket_client = WebSocketClient("ws://localhost:8080")
        self.websocket_client.run()

    # =========================================================================

    def connectionSuccess(self):

        # =====================================================================

        #
        file_path = 'gameIWantToJoin.txt'

        #
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                self.game_id = file.read()

            os.remove(file_path)
        else:
            print(f"The file {file_path} does not exist.")

        pygame_gui.elements.UILabel(relative_rect=pygame.Rect((350, 10), (300, 50)),
                                    text='Connection successful!',
                                    manager=self.manager)

        print("valeur de game_id")
        print(self.game_id)

        # =====================================================================

        # Recuperer le document correspondant au 'game_name' et 'name'
        # il faut se connecter a symfony,
        # lui passer cet ID du dongeon (self.game_id) et le stair (vu qu'on
        # demarre le jeu c'est le 1)
        #
        url = 'https://localhost:8000/test_python_render_map_to_python'

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
            'game_name': self.game_id,
            'name': "stair_1",
        }

        #
        headers = {'Content-Type': 'application/json'}

        #
        response = requests.post(url,
                                 data=json.dumps(data),
                                 headers=headers,
                                 verify=False)

        """
        print(f'>> Status Code: {response.status_code}')
        print(f'>> Content: {response.content}')

        print(">> valeur de response.text")
        print(response.text)
        """

        #
        self.response_data = response.json()

        #
        if self.response_data['user']['nickname'] == self.user_nickname and \
                self.response_data['user']['tokenForPython'] == self.user_tokenForPython and \
                self.response_data['status']:

            # =================================================================

            # Check if the "save" directory exists
            save_directory = 'multiplayer/save'
            if os.path.exists(save_directory):
                print(f"The directory {save_directory} exists.")
            else:
                print(f"The directory {save_directory} does not exist.")
                os.makedirs(save_directory)

            # Check if the "stairs_json" directory exists inside the "save" directory
            stairs_json_directory = os.path.join(save_directory, 'stairs_json')
            if os.path.exists(stairs_json_directory):
                print(f"The directory {stairs_json_directory} exists.")
            else:
                print(f"The directory {stairs_json_directory} does not exist.")
                os.makedirs(stairs_json_directory)

            # =====================================================================

            #
            json_dict = {
                    "user_id": self.response_data['user']['id'],
                    "user_nickname": self.response_data['user']['nickname'],
                    "user_email": self.response_data['user']['email'],
                    "user_tokenForPython": self.response_data['user']['tokenForPython'],
                    "user_tokenForPythonExpiration": self.response_data['user']['tokenForPythonExpiration'],
                    "file": 'save/stairs_json/' + self.response_data['gameArray']['name'],
                    "level": self.response_data['gameArray']['level'],
                    "exit_tile": self.response_data['gameArray']['exit_tile'],
                    "entry_tile": self.response_data['gameArray']['entry_tile'],
                    "white_tiles_array": self.response_data['gameArray']['white_tiles_array'],
                    "blue_tiles_array": self.response_data['gameArray']['blue_tiles_array'],
                    "total_tiles_array": self.response_data['gameArray']['total_tiles_array'],
                    "rooms_tiles_array": self.response_data['gameArray']['rooms_tiles_array'],
                    "attributes_rooms_array": self.response_data['gameArray']['attributes_rooms_array'],
                    }

            #
            json_file_path = os.path.join(stairs_json_directory, 'stair_1.json')

            #
            with open(json_file_path, 'w') as json_file:
                json.dump(json_dict, json_file, indent=4)

            print(f"Data written to {json_file_path}")

            return True
        else:
            print("")
            print("Erreur: 54092, exit program")
            return False

    # =========================================================================

    def connectionFailure(self):
        pygame_gui.elements.UILabel(relative_rect=pygame.Rect((350, 10), (300, 50)),
                                    text='A problem occurred.',
                                    manager=self.manager)

    # =========================================================================

    def prepare_GUI(self):

        # =====================================================================

        self.running = True
        while self.running:
            time_delta = pygame.time.Clock().tick(60)/1000.0

            # 1. Handle events
            for event in pygame.event.get():

                # envoie l'événement à un gestionnaire d'événements pour un
                # traitement supplémentaire.
                self.manager.process_events(event)

                # =============================================================

                if event.type == pygame.QUIT:

                    # json qui envoie un eventType 'disconnect'
                    data = {
                        "event_type": "disconnect",
                        "player": self.player.to_dict()
                    }

                    # envoie le json au server,
                    self.websocket_client.ws.send(json.dumps(data))

                    # ferme la connexion WebSocket
                    self.websocket_client.close()

                    # quitte pygame et ferme le programme
                    pygame.quit()
                    sys.exit()

                # =============================================================

                if self.player is not None:

                    #
                    self.player.handle_events(event, self.liste_npcs, self.liste_items)

            # MAJ l'etat du jeu si l'objet player existe
            if self.player is not None:

                # Convertit l'etat du joueur en un objet json
                self.current_player_state = self.player.to_dict()

                # Accéder aux données des autres joueurs
                self.other_players = self.websocket_client.players

                # Envoie les MAJ du joueur si son etat est différent
                if self.current_player_state != self.previous_player_state:

                    #
                    data = {
                            "event_type": "connect",
                            "player": self.player.to_dict()
                            }

                    # le player n'est pas None, on l'envoie vers le server.ts
                    self.websocket_client.ws.send(json.dumps(data))

                    # MAJ de l'etat precedent du joueur
                    self.previous_player_state = self.current_player_state

                # verifie si les données des autres joueurs ont été modifiées
                # depuis la dernière itération (FPS)
                if self.other_players != self.previous_other_players:
                    print("self.other_players sent from WebSocketClient to multiplayer_screen04")
                    print("displayed from multiplayer_screen04")
                    print(self.other_players)

                    # enleve l'instance de Player de CE client python (ce script)
                    self.other_players = {player_id: player_data for player_id, player_data in self.other_players.items() if player_id != self.player.id}

                    # =====================================================

                    # Nettoie la liste des autres joueurs
                    self.other_players_instances.clear()

                    # Recrée les autres joueurs
                    # (1 MAJ aurait été plus indiquée, est ce que c'est au moins
                    # possible?)
                    for player_id, self.player_data in self.other_players.items():
                        player_instance = Player(self.player_data['name'],
                                                 self.player_data['strength'],
                                                 self.player_data['attack'],
                                                 self.player_data['defense'],
                                                 self.player_data['life'],
                                                 self.player_data['magic'],
                                                 tuple(self.player_data['position']),
                                                 tuple(self.player_data['color']),
                                                 self.player_data['radius'],
                                                 self.player_data['speed'],
                                                 self.player_data['stair_actuel'],
                                                 player_id)
                        player_instance.draw()

                        # Ajoute l'instance du joueur à la liste des joueurs
                        self.other_players_instances[player_id] = player_instance

                    # =====================================================

                    # MAJ la précedente liste des autres joueurs avec les
                    # valeurs de l'actuelle liste des joueurs. Cela permet de
                    # conserver un historique de l'état précédent des joueurs
                    # afin de vérifier si leur état a été modifié ou pas.
                    self.previous_other_players = self.other_players

            else:

                # recuperer les variables de la response_data
                self.exit_tile = self.response_data['gameArray']['exit_tile']
                self.entry_tile = self.response_data['gameArray']['entry_tile']
                self.white_tiles = self.response_data['gameArray']['white_tiles_array']
                self.blue_tiles = self.response_data['gameArray']['blue_tiles_array']
                self.total_tiles_list = self.response_data['gameArray']['total_tiles_array']
                self.rooms_tiles_list = self.response_data['gameArray']['rooms_tiles_array']
                self.attributes_rooms_list = self.response_data['gameArray']['attributes_rooms_array']

                # =============================================================

                # dessine la carte
                UtilitairesNoPlayer.draw_map_from_json(self,
                                               "multiplayer/save/stairs_json/stair_1.json",
                                               self.canvas01_maps)

                # creer le joueur depuis le fichier de sauvegarde
                # save/player.json
                # game.canvas01_maps = parametre defini aussi ds le constructeur de Player
                # pr pvoir blitter l'instance weapon_instance definie ds la classe
                # Player <<< verifier si l'instance existe tjs? normalement,
                # elle ne devrait pas
                self.player = self.utilitairesMultiplayer.create_player_from_saved_player_json(self.canvas01_maps, self, position_override=(self.entry_tile['x'], self.entry_tile['y']))

                # dessine le player sur la carte
                self.player.draw()

                # =============================================================

            if self.running:
                self.manager.update(time_delta)

                self.screen.blit(self.canvas01_maps,
                                 (0, 0))

                # =============================================================

                #
                if self.player is not None:
                    self.screen.blit(self.player.surface, self.player.position)

                # Draw the other players
                for player_instance in self.other_players_instances.values():
                    self.screen.blit(player_instance.surface, player_instance.position)

                # =============================================================

                pygame.display.update()


if __name__ == '__main__':
    connect_obj = Connect()

    if connect_obj.connectionSuccess():
        connect_obj.prepare_GUI()

    else:
        print("Failed to establish a connection. Exiting the program.")
        pygame.quit()
        sys.exit()
