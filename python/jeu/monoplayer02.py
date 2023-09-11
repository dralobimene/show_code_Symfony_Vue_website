import pygame
import pygame_gui

import sys
import math
import random
import os
import json
from collections import deque
from copy import deepcopy

from classes.DungeonGame import DungeonGame
from utilitaires import Utilitaires
from utilitaires_no_player import UtilitairesNoPlayer

from classes.Player import Player
from classes.Item import Item
from classes.items.protections.Protection import Protection
from classes.items.protections.Shield import Shield
from classes.items.weapons.Weapon import Weapon
from classes.items.weapons.Sword import Sword

from classes.FileProcessor import FileProcessor
from classes.KeyHandler import KeyHandler

from utilitaires import EventManager
from classes.InformationsPanel import InformationsPanel
from classes.StartMenuFromSavedGame import StartMenuFromSavedGame


class Game:
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

    # =========================================================================

    def __init__(self):
        # def de variables de classes
        # et d'instances d'autres classes importées

        #
        pygame.init()

        #
        self.screen = pygame.display.set_mode((1000, 800))

        #
        pygame.display.set_caption('Monoplayer: you are playing the game')

        #
        self.utilitairesNoPlayer = UtilitairesNoPlayer()

        #
        self.player = None

        #
        self.player_attributes = None

        #
        self.manager = pygame_gui.UIManager((1000, 800))

        #
        self.event_manager = EventManager(self)

        # pr les evts clavier qui ne st pas les touches directionnelles
        self.key_handler = KeyHandler(self.player)

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
        self.informations_panel = InformationsPanel(pygame.Rect(0, 600, 800, 200))

        #
        self.start_menu_from_saved_game = StartMenuFromSavedGame(self.canvas02_buttons,
                                                                 self.manager,
                                                                 self.event_manager,
                                                                 self.player)

        #
        self.clock = pygame.time.Clock()

        #
        self.dungeon_map = None

        #
        self.map_width = None

        #
        self.white_tiles_array = []
        self.blue_tiles_array = []
        self.total_tiles_array = []

        #
        self.save_button = None

        #
        self.json_files_sorted = None

        #
        self.chosen_dict_to_set_exit_tile = None
        self.chosen_dict_to_set_entry_tile = None

        # Create a new
        self.liste_npcs = None

        #
        self.liste_items = None

        #
        self.liste_tiles_pr_placer_instances_item = None

        #
        self.liste_des_tiles_qui_ont_un_item = None

        #
        self.instances_array = None

        #
        self.liste_item_instances = None

    # =========================================================================

    def is_reachable(self):
        """
        Cette méthode vérifie si toutes les tuiles dans `total_tiles_array`
        sont atteignables à partir d'une tuile choisie au hasard.
        Elle utilise un algorithme de remplissage par diffusion (flood fill)
        pour parcourir toutes les tuiles atteignables à partir de
        la tuile de départ.

        Retourne:
            True si toutes les tuiles sont atteignables, sinon False.
        """

        if not self.total_tiles_array:
            return False

        # Choisis une tuile au hasard
        start_tile = random.choice(self.total_tiles_array)

        # Crée un ensemble de toutes les tuiles pour une recherche rapide
        all_tiles = set((tile["x"], tile["y"]) for tile in self.total_tiles_array)

        # jeu de tuiles qui ont été atteintes
        # ensemble vide appelé reached_tiles.
        # un ensemble est une collection non ordonnée d'éléments uniques
        reached_tiles = set()

        # File d'attente pour le remplissage par diffusion
        # classe de la bibliothèque collections
        queue = deque([start_tile])

        while queue:
            # supprime le 1° elt de la 'queue'
            current_tile = queue.popleft()
            # si cette tile n'est pas ds le set reached_tile
            # alors elle est ajoutée au set (normal, à la 1° iteration,
            # la 1° tile ne peut pas etre ds le set)
            if (current_tile["x"], current_tile["y"]) not in reached_tiles:
                reached_tiles.add((current_tile["x"], current_tile["y"]))

                # Ajoute les voisins à la file d'attente
                for neighbor in self.get_neighbors(current_tile):
                    # si la tile est bien ds all_tiles alors
                    # on l'ajoute à la queue
                    if (neighbor["x"], neighbor["y"]) in all_tiles:
                        queue.append(neighbor)

        # Verifie si toutes les tuiles ont été atteintes
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

    def start_game(self):
        # print("")
        # print("Execution methode start_game")
        # print("game started")
        # print("")
        self.informations_panel.add_message("game started")

        # Obtain a list of files in the directory
        json_files = os.listdir("save/stairs_json")

        #
        self.json_files_sorted = sorted(json_files, key=Utilitaires.sort_by_numeric_part)

        # print("")
        # print("la liste triée des fichiers qui se trouvent ds save/stairs_json")
        # print(self.json_files_sorted)
        # print("")

        self.informations_panel.add_message("")
        self.informations_panel.add_message("sys: la liste triée des fichiers qui se trouvent ds save/stairs_json")
        self.informations_panel.add_message("")

        # Check if there is at least one file in the directory
        if json_files:

            # Clear the tile arrays
            self.white_tiles_array.clear()
            self.blue_tiles_array.clear()
            self.total_tiles_array.clear()

            #
            self.white_tiles_array, self.blue_tiles_array, self.total_tiles_array = self.get_tile_arrays()

            # Assign the player to the key handler
            self.key_handler = KeyHandler(self.player)

            # Get the first file
            first_json_file = self.json_files_sorted[0]

            #
            # print("")
            # print("le nom du 1° fichier trouvé ds le dossier save/stairs_json")
            # print(f"est: {first_json_file}")
            # print("")

            """
            if self.player is not None:
                print("")
                print("monoplayer02.py, game_start()")
                print("player pas None")
            else:
                print("")
                print("monoplayer02.py, game_start()")
                print("player None")
            """

        else:
            print("No files found in the directory 'save/stairs_json'.")
            print("04: exit program")
            pygame.quit()
            sys.exit()

        # print("")
        # print("fin execution start_game")
        # print("")

    # =========================================================================

    def monoplayer02_generation(self):

        # verifier que le dossier "save" existe
        if os.path.exists("save"):
            # print("The 'save' directory exists.")
            pass
        else:
            print("The 'save' directory does not exist.")
            print("01: exit program")
            pygame.quit()
            sys.exit()

        # Check if save/player.json exists
        if os.path.isfile("save/player.json"):
            # print("File save/player.json already exists.")
            pass
        else:
            # print("File save/player.json does not exist.")
            pass

        # verifier que le dossier "save/stairs_json" existe
        if os.path.exists("save/stairs_json"):
            # print("The 'save/stairs_json' directory exists.")
            pass
        else:
            # print("The 'save/stairs_json' directory does not exist.")
            pass

        # effacer les eventuels fichiers presents
        # ds save/stairs_json
        # List elements in "save" folder
        files_in_save_folder = os.listdir('save/stairs_json')

        if len(files_in_save_folder) == 0:
            # print("Save/stairs_json folder is empty.")
            pass
        else:
            # print("Save/stairs_json folder is not empty, we just deleted files.")

            for file in files_in_save_folder:
                file_path = os.path.join('save', file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            # print("All files have been removed from the 'save/stairs_json' folder.")

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
            game.dungeon_map, game.map_width, _ = dungeon_game.generate_next_map()

            #
            game.white_tiles_array, game.blue_tiles_array, game.total_tiles_array = game.get_tile_arrays()

            # fait 1 copie exacte de game.white_tiles_array pr ds la
            # prochaine boucle pvoir definir la tile entree
            # de chacun des stairs
            game.white_tiles_array_copy = deepcopy(game.white_tiles_array)

            #
            game.rooms_tiles_array = game.get_rooms_tiles(game.white_tiles_array)

            #
            game.attributes_rooms_array = game.get_attributes_rooms(game.white_tiles_array)

            # tableau qui contient un certain nbre (= au 2nd parametre)
            # de tiles issues de game.white_tiles_array
            # sert pr définir le nbre de tiles qui vt chacune contenir
            # 1 instance de la classe Item
            # etape: M1A -> etape: M1B
            game.instances_array = Utilitaires.choose_random_elements_from_array(game.white_tiles_array, 4)

            # stocke le nom des fichiers json stair_X
            # qui seront crées ou pas
            created_files = []
            not_created_files = []

            # =================================================================
            # ECRITURE DES FICHIERS JSON DE CHAQUE STAIR
            # on decide aussi des differentes tiles qui vt posseder
            # les entrees, les sorties, les items et NPCs
            if game.is_reachable():
                # print("stair reachable")

                # Choose a random element to set exit for each stair
                # from game.white_tiles_array
                game.chosen_dict_to_set_exit_tile = random.choice(game.white_tiles_array)
                # print("")
                # print("valeur de chosen_dict_to_set_exit_tile")
                # print(game.chosen_dict_to_set_exit_tile)
                # print("")

                # pr definir l'entree, il faut etre sur que les tiles entree
                # et sortie ne soient pas les memes. Dc pr definir la tile
                # entree, il faut d'abord faire une copie exacte du tableau
                # game.white_tiles_array, (fait au-dessus, en dehors de la
                # boucle, qd on definit les array)
                # supprimer la tile qui a servi a definir la sortie
                # choisir alors 1 tile au hasard pr definir la tile entree
                game.white_tiles_array_copy.remove(game.chosen_dict_to_set_exit_tile)
                game.chosen_dict_to_set_entry_tile = random.choice(game.white_tiles_array_copy)
                # print("")
                # print("valeur de chosen_dict_to_set_entry_tile")
                # print(game.chosen_dict_to_set_entry_tile)
                # print("")

                # on cree 1 variable particuliere pr le 1° stair qui
                # permet de positionner + tard, le joueur au meme
                # emplacement que la "entry_tile"
                if index_fichiers == 1:
                    game.tile_spe_entry_tile_first_stair = game.chosen_dict_to_set_entry_tile
                    # print("")
                    # print("valeur de la game.tile_spe_entry_tile_first_stair")
                    # print(game.tile_spe_entry_tile_first_stair)
                    # print("")

                ##
                # etape: M1B -> etape: M1C ds utilitaires.py, draw_map_from_json()
                game.liste_tiles_pr_placer_instances_item = {}

                for j in range(len(game.instances_array)):
                    # print("boucle j:")
                    # print(j)

                    # print("")
                    # print("game.liste_tiles_pr_placer_instances_item")
                    game.liste_tiles_pr_placer_instances_item[f"tile_item_{(j + 1)}"] = game.instances_array[j]
                    # print(game.liste_tiles_pr_placer_instances_item[f"tile_item_{(j + 1)}"])
                ##

                json_dict = {
                        "file": f"save/stairs_json/stair_{index_fichiers}.json",
                        "name": f"stair_{index_fichiers}",
                        "level": f"{index_fichiers}",
                        "exit_tile": game.chosen_dict_to_set_exit_tile,
                        "entry_tile": game.chosen_dict_to_set_entry_tile,
                        "white_tiles_array": game.white_tiles_array,
                        "blue_tiles_array": game.blue_tiles_array,
                        "total_tiles_array": game.total_tiles_array,
                        "rooms_tiles_array": game.rooms_tiles_array,
                        "attributes_rooms_array": game.attributes_rooms_array,
                        "liste_tiles_pr_placer_instances_item": game.liste_tiles_pr_placer_instances_item,
                        }

                file_name = f'save/stairs_json/stair_{index_fichiers}.json'

                with open(f'save/stairs_json/stair_{index_fichiers}.json', 'w') as f:
                    json.dump(json_dict, f, indent=4)

                # on update chaque json de stair pr y inscrire les données
                # des items que l'on place ds ce stair
                game.liste_items = Utilitaires.createItems(self, file_name)

                #
                created_files.append(file_name)

                index_fichiers += 1
            else:
                not_created_file = f'stair_{index_fichiers}'

                # print(f"Ce stair n'est pas reachable, stair: {not_created_file}")

                not_created_files.append(not_created_file)

        # =====================================================================

        running = True
        while running:
            time_delta = game.clock.tick(60)/1000.0

            for event in pygame.event.get():

                # game = instance de la classe Game
                # event_manager = instance de la classe EventManager
                # definie ds utilitaires.py
                # NOTE
                # si placé ailleurs, pas d'act° avec le bouton Save
                # FONCTIONNE: print("Calling process_event method")
                game.event_manager.process_event(event, game.player_attributes)

                #
                game.informations_panel.handle_event(event)

                # =============================================================

                #
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # =============================================================

                # Handle events for the currently active menu
                if game.start_menu_from_saved_game.active:
                    game.start_menu_from_saved_game.handle_event(event)
                elif game.start_menu_from_saved_game.submenu1_inventory is not None and game.start_menu_from_saved_game.submenu1_inventory.active:
                    game.start_menu_from_saved_game.submenu1_inventory.handle_event(event)
                elif game.start_menu_from_saved_game.submenu2_internet is not None and game.start_menu_from_saved_game.submenu2_internet.active:
                    game.start_menu_from_saved_game.submenu2_internet.handle_event(event)

                # =============================================================

                if game.player is not None:
                    game.player.handle_events(event, game.liste_npcs, game.liste_items)

                    # Update the player_attributes dictionary with the updated position
                    # MAJ la position du player des le debut du jeu
                    game.player_attributes['position'] = (game.player.position.x, game.player.position.y)

                else:

                    # =========================================================

                    # Recupere les infos du fichier save/stairs_json/stair_X.json
                    game.content_json_file_stair = UtilitairesNoPlayer.recuperer_infos_du_stair(self)

                    game.stair_actuel = game.content_json_file_stair['stair_actuel']
                    # print("")
                    # print("valeur de stair_actuel")
                    # print(stair_actuel)

                    game.exit_tile = game.content_json_file_stair['exit_tile']
                    # print("")
                    # print("elts ds le dict exit_tile")
                    # print(exit_tile)

                    game.entry_tile = game.content_json_file_stair['entry_tile']
                    # print("")
                    # print("elts ds le dict entry_tile")
                    # print(entry_tile)

                    game.white_tiles = game.content_json_file_stair['white_tiles_list']
                    # print("")
                    # print("elts ds white_tiles")
                    # print(white_tiles)

                    # print("")
                    # print("valeur de white_tiles[0]")
                    # print("montre comment acceder a l'element")
                    # print(white_tiles[0])

                    # print("")
                    # print("valeur de x ds white_tiles[0]")
                    # print("montre comment acceder à l'element")
                    # print(white_tiles[0]['x'])

                    game.blue_tiles = game.content_json_file_stair['blue_tiles_list']
                    # print("")
                    # print("elts ds blue_tiles")
                    # print(blue_tiles)

                    game.total_tiles_list = game.content_json_file_stair['total_tiles_list']
                    # print("")
                    # print("elts ds total_tiles_list")
                    # print(total_tiles_list)

                    game.rooms_tiles_list = game.content_json_file_stair['rooms_tiles_list']
                    # print("")
                    # print("elts ds rooms_tiles_list")
                    # print(rooms_tiles_list)

                    game.attributes_rooms_list = game.content_json_file_stair['attributes_rooms_list']
                    # print("")
                    # print("elts ds attributes_rooms_list")
                    # print(attributes_rooms_list)

                    # =========================================================

                    # dessine la carte
                    UtilitairesNoPlayer.draw_map_from_json(self,
                                                   game.stair_actuel,
                                                   game.canvas01_maps)

                    # creer le joueur depuis le fichier de sauvegarde
                    # save/player.json
                    # game.canvas01_maps = parametre defini aussi ds le constructeur de Player
                    # pr pvoir blitter l'instance weapon_instance definie ds la classe
                    # Player <<< verifier si l'instance existe tjs? normalement,
                    # elle ne devrait pas
                    game.player = Utilitaires.create_player_from_saved_player_json(game.canvas01_maps, self, position_override=(game.tile_spe_entry_tile_first_stair['x'], game.tile_spe_entry_tile_first_stair['y']))

                    # dessine le player sur la carte
                    game.player.draw()

                    #
                    game.start_game()

                    #
                    game.liste_npcs = Utilitaires.create_NPCs(self, game.player.stair_actuel)

                    # =========================================================

                    """
                    la game.liste_items et les instances de item créees
                    dans la boucle for qui suit doivent avoir les memes
                    attributs et il doit y en avoir autant
                    """
                    # print("")
                    # print("liste des tiles qui ont des items")
                    # print("Lit le fichier json qui decrit le stair")
                    game.liste_des_tiles_qui_ont_un_item = Utilitaires.getListeTilesPrPlacerInstancesItem(self, game.player.stair_actuel)
                    # print(game.liste_des_tiles_qui_ont_un_item)

                    # on lit le fichier save/stairs_json/stair_X.json
                    # on va ajouter une nvelle paire clé => valeur
                    # nommée 'tile_position' qui se trouvera ds chaque nested
                    # dictionnaire, sect°: 'liste_tiles_pr_placer_instances_item'
                    # 'weapon', cette nvelle paire prend la valeur des
                    # coordonnées de la tile qui possede l'item
                    with open(game.player.stair_actuel, 'r') as f:
                        data = json.load(f)

                    # print("on cree la nvelle paire clé => valeur")
                    # print("'tile_position' => (x, y)")
                    # print("ds chaque OrderedDict 'weapon' de chaque")
                    # print("'tile_weapon_X'")
                    for key, item in game.liste_des_tiles_qui_ont_un_item.items():
                        x = item['x']
                        y = item['y']
                        item['weapon'].update({'tile_coordinates': (x, y)})
                        game.liste_items.append(item['weapon'])

                    # update the original 'data' dictionary
                    # (au-dessus de la boucle for)
                    # with your updated 'game.liste_des_tiles_qui_ont_un_item'
                    data['liste_tiles_pr_placer_instances_item'] = game.liste_des_tiles_qui_ont_un_item

                    # Write the modified data back to the file
                    with open(game.player.stair_actuel, 'w') as f:
                        json.dump(data, f, indent=4)

                    # print("Impression 01, des attributs des items")
                    # print("ecrite ds le fichier json du stair")
                    # print("APRES creat° de la nvelle paire cle => valeur")
                    # print("on imprime d'apres la game.liste_items")
                    # for item in game.liste_items:
                        # print(item)

                    # print("reimpression de la game.liste_des_tiles_qui_ont_un_item")
                    # print("il doit y avoir un nvel attribut 'tile_position'")
                    # print("ds chaque nested OrderedDict 'weapon'")
                    # print(game.liste_des_tiles_qui_ont_un_item)

                    # on redefinit la game.liste_item_instances qui etait à None
                    game.liste_item_instances = []

                    # create instances for each item in game.liste_items
                    for item in game.liste_items:
                        if item['type_category'] == 'shield':
                            shield = Shield(
                                attack=item['attack'],
                                defense=item['defense'],
                                transportable=item['transportable'],
                                is_ranged=item['is_ranged'],
                                position=tuple(item['position']),
                                color=tuple(item['color']),
                                visible_onto_map=item['visible_onto_map'],
                                equipe=item['equipe'],
                                tile_coordinates=item['tile_coordinates']
                            )
                            game.liste_item_instances.append(shield)
                        elif item['type_category'] == 'sword':
                            sword = Sword(  # adjust this to match the constructor of the Sword class
                                attack=item['attack'],
                                defense=item['defense'],
                                transportable=item['transportable'],
                                is_ranged=item['is_ranged'],
                                position=tuple(item['position']),
                                color=tuple(item['color']),
                                visible_onto_map=item['visible_onto_map'],
                                equipe=item['equipe'],
                                tile_coordinates=item['tile_coordinates']
                            )
                            game.liste_item_instances.append(sword)

                    # =========================================================

                    # =========================================================
                    # sauvegarde immédiate au lancement du jeu.

                    # ETAPE 01:
                    # permet de passer les infos à la classe EventManager
                    # du fichier utilitaires.py,
                    # methodes save_game et process_event (process_event
                    # communique le parametre a save_game)
                    game.player_attributes = {
                        'name': game.player.name,
                        'strength': game.player.strength,
                        'attack': game.player.attack,
                        'defense': game.player.defense,
                        'life': game.player.life,
                        'magic': game.player.magic,
                        'position': game.player.position,
                        'color': game.player.color,
                        'radius': game.player.radius,
                        'speed': game.player.speed,
                        # ajout du stair actuellement visité pr pvoir lancer
                        # la sauvegarde. Etant que le joueur vient de
                        # debuter 1 nvelle partie, le fichier du stair est
                        # forcement /save...
                        'stair_actuel': 'save/stairs_json/stair_1.json',
                        }

                    # ETAPE 02: ecrire les infos passées ds le fichier
                    # save/player.json
                    game.event_manager.save_game(game.player_attributes)
                    # =========================================================

                    # print("attributs game.player")
                    # print(game.player)

                    # print("liste des fichiers ds save/stairs_json")
                    game.liste_fichiers_stairs_json = game.utilitairesNoPlayer.get_all_stair_files()
                    # print(game.liste_fichiers_stairs_json)

                    # =========================================================

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == game.start_menu_from_saved_game.button3:
                        print("Button3 clicked! depuis monoplayer02.py")

                if event.type == pygame.KEYUP:
                    game.key_handler.handle_key_up(event.key)
                    # check if the key is one of the special function keys
                    if event.key in game.key_handler.func_key_methods:
                        # call the corresponding method
                        game.key_handler.func_key_methods[event.key]()

                    elif event.key == pygame.K_SPACE:
                        print("================================================")
                        print("SPACE key pressed")
                        print("event from monoplayer02.py")
                        print(f"Player position: {game.player.position}")
                        if game.player is not None:

                            print("Le player visite d'apres son attribut")
                            print("game.player.stair_actuel, le stair:")
                            print(game.player.stair_actuel)

                            print("le fichier " + game.player.stair_actuel)
                            print("est logiquement le fichier qui decrit le stair")

                            # print("on redefinit game.exit_tile")
                            # print("et la cle game.entry_tile")
                            with open(game.player.stair_actuel, 'r') as f:
                                data = json.load(f)
                            # print("obtenir la valeur de la clé 'exit_tile'")
                            game.exit_tile = data.get('exit_tile', 'Key not found')
                            # print("valeur de game.exit_tile")
                            # print(game.exit_tile)
                            # print("obtenir la valeur de la clé 'entry_tile'")
                            game.entry_tile = data.get('entry_tile', 'Key not found')
                            # print("valeur de game.entry_tile")
                            # print(game.entry_tile)

                            # print("coordonnées de l'actuelle exit_tile")
                            game.exit_tile_coords = [game.exit_tile['x'], game.exit_tile['y']]
                            # print(game.exit_tile_coords)

                            # print("coordonnées de l'actuelle entry_tile")
                            game.entry_tile_coords = [game.entry_tile['x'], game.entry_tile['y']]
                            # print(game.entry_tile_coords)

                            if game.player.position == game.exit_tile_coords:

                                # print("player sur la game.exit_tile")
                                print("on lit l'attribut game.player.stair_actuel")
                                print(game.player.stair_actuel)

                                print("on lit le nom des fichiers qui se trouvent")
                                print("dans save/stairs_json")
                                print(game.liste_fichiers_stairs_json)

                                print("il faut couper cet attribut pr ne")
                                print("retenir que le nom du fichier")
                                print(os.path.basename(game.player.stair_actuel))

                                print("on sort, previous_element, current_element, next_element")
                                print("grace au File Processor")
                                print("game.elt contient, par exemple")
                                print("('No previous element', 'stair_1.json', 'stair_2.json')")
                                game.elt = FileProcessor.process_next_v2(self,
                                                                    game.liste_fichiers_stairs_json,
                                                                    os.path.basename(game.player.stair_actuel))

                                print("la liste des 3 elts renvoyés par le FP")
                                print(game.elt)

                                print("on recupere le nom du fichier qui")
                                print("represente le next_element")
                                print(game.elt[2])

                                print("on le prefixe avec le nom des dossiers")
                                print("c-a-d 'save/stairs_json'")
                                print("on l'imprime")
                                game.complete_path = os.path.join('save/stairs_json', game.elt[2])
                                print(game.complete_path)

                                print("actualiser le fichier save/player.json")
                                UtilitairesNoPlayer.update_json_file_player(self, "stair_actuel", game.complete_path)

                                print("lire le fichier qui represente le prochain stair")
                                with open(game.complete_path, 'r') as f:
                                    data = json.load(f)

                                # print("obtenir la valeur de la clé 'exit_tile'")
                                game.next_exit_tile_value = data.get('exit_tile', 'Key not found')
                                # print("valeur de game.next_exit_tile_value")
                                # print(game.next_exit_tile_value)

                                # print("obtenir la valeur de la clé 'entry_tile'")
                                game.next_entry_tile_value = data.get('entry_tile', 'Key not found')
                                # print("valeur game.next_entry_tile_value")
                                # print(game.next_entry_tile_value)

                                # =============================================

                                # print("on va definir")
                                # print("la liste des NPCs et la liste des Items")

                                # print("pr cela , il faut d'abord redefinir")
                                # print("game.white_tiles")
                                # print("on placera npcs et items la-dessus")
                                game.white_tiles = Utilitaires.getWhiteTiles(self, game.complete_path)

                                # print("on definit la liste des NPCs")
                                # print("on remplit la game.liste_npcs")
                                game.liste_npcs = Utilitaires.create_NPCs(self, game.complete_path)

                                # =============================================

                                # print("on nettoie les canvas et on dessine")
                                # print("le nveau stair")
                                game.canvas01_maps.fill((0, 0, 0))
                                game.canvas05_items.fill((0, 0, 0))
                                game.canvas04_npcs.fill((0, 0, 0))

                                UtilitairesNoPlayer.draw_map_from_json(self,
                                                                       game.complete_path,
                                                                       game.canvas01_maps)

                                # =============================================

                                # print("creer 1 instance de la classe Player")
                                # print(" et la placer sur la game.next_entry_tile_value")
                                game.player = Player(game.player.name,
                                                 game.player.strength,
                                                 game.player.attack,
                                                 game.player.defense,
                                                 game.player.life,
                                                 game.player.magic,
                                                 (game.next_entry_tile_value['x'], game.next_entry_tile_value['y']),
                                                 game.player.color,
                                                 game.player.radius,
                                                 game.player.speed,
                                                 game.complete_path)

                                # =============================================

                                # print("definir la liste des allowed_tiles")
                                game.allowed_tiles = game.utilitairesNoPlayer.getAllowedTiles(game.complete_path)
                                # print("valeur de la liste des allowed tiles")
                                # print(game.allowed_tiles)

                                # =============================================

                                # print("effacer la game.liste_items pr ensuite")
                                # print("la remplir avec les nvelles valeurs")
                                # print("faire de meme avec la game.liste_item_instances")
                                # print("et la game.liste_des_tiles_qui_ont_un_item")
                                game.liste_items.clear()
                                game.liste_item_instances.clear()
                                game.liste_des_tiles_qui_ont_un_item.clear()

                                """
                                la game.liste_items et les instances de item créees
                                dans la boucle for qui suit doivent avoir les memes
                                attributs et il doit y en avoir autant
                                """

                                # print("liste des tiles qui ont des items")
                                game.liste_des_tiles_qui_ont_un_item = Utilitaires.getListeTilesPrPlacerInstancesItem(self, game.complete_path)
                                # print("la valeur de game.liste_des_tiles_qui_ont_un_item")
                                # print(game.liste_des_tiles_qui_ont_un_item)

                                # on lit le fichier le prochain
                                # save/stairs_json/stair_X.json
                                # (defini par la game.complete_path)
                                # on va ajouter une nvelle paire clé => valeur
                                # nommée 'tile_position' qui se trouvera ds chaque nested
                                # dictionnaire, sect°: 'liste_tiles_pr_placer_instances_item'
                                # 'weapon', cette nvelle paire prend la valeur des
                                # coordonnées de la tile qui possede l'item
                                with open(game.complete_path, 'r') as f:
                                    data = json.load(f)

                                # print("on cree la nvelle paire clé => valeur")
                                # print("'tile_position' => (x, y)")
                                # print("ds chaque OrderedDict 'weapon' de chaque")
                                # print("'tile_weapon_X'")
                                for key, item in game.liste_des_tiles_qui_ont_un_item.items():
                                    x = item['x']
                                    y = item['y']
                                    item['weapon'].update({'tile_coordinates': (x, y)})
                                    game.liste_items.append(item['weapon'])

                                # update the original 'data' dictionary
                                # (au-dessus de la boucle for)
                                # with your updated 'game.liste_des_tiles_qui_ont_un_item'
                                data['liste_tiles_pr_placer_instances_item'] = game.liste_des_tiles_qui_ont_un_item

                                # Write the modified data back to the file
                                with open(game.complete_path, 'w') as f:
                                    json.dump(data, f, indent=4)

                                # print("Impression 01, des attributs des items")
                                # print("ecrite ds le fichier json du stair")
                                # print("APRES creat° de la nvelle paire cle => valeur")
                                # for item in game.liste_items:
                                    # print(item)

                                # print("reimpression de la game.liste_des_tiles_qui_ont_un_item")
                                # print("il doit y avoir un nvel attribut 'tile_position'")
                                # print("ds chaque nested OrderedDict 'weapon'")
                                # print(game.liste_des_tiles_qui_ont_un_item)

                                # create instances for each item in game.liste_items
                                for item in game.liste_items:
                                    if item['type_category'] == 'shield':
                                        shield = Shield(
                                            attack=item['attack'],
                                            defense=item['defense'],
                                            transportable=item['transportable'],
                                            is_ranged=item['is_ranged'],
                                            position=tuple(item['position']),
                                            color=tuple(item['color']),
                                            visible_onto_map=item['visible_onto_map'],
                                            equipe=item['equipe'],
                                            tile_coordinates=item['tile_coordinates']
                                        )
                                        game.liste_item_instances.append(shield)
                                    elif item['type_category'] == 'sword':
                                        sword = Sword(  # adjust this to match the constructor of the Sword class
                                            attack=item['attack'],
                                            defense=item['defense'],
                                            transportable=item['transportable'],
                                            is_ranged=item['is_ranged'],
                                            position=tuple(item['position']),
                                            color=tuple(item['color']),
                                            visible_onto_map=item['visible_onto_map'],
                                            equipe=item['equipe'],
                                            tile_coordinates=item['tile_coordinates']
                                        )
                                        game.liste_item_instances.append(sword)

                                # =============================================

                                # print("dessiner le player")
                                game.player.draw()

                                # print("executer la methode start_game")
                                game.start_game()

                                print("actualiser le fichier save/player.json")
                                UtilitairesNoPlayer.update_json_file_player(self, "stair_actuel", game.complete_path)

                            elif game.player.position == game.entry_tile_coords:
                                print("Player is on the entry tile.")
                                print("on lit l'attribut game.player.stair_actuel")
                                print(game.player.stair_actuel)

                                print("on lit le nom des fichiers qui se trouvent")
                                print("dans save/stairs_json")
                                print(game.liste_fichiers_stairs_json)

                                print("il faut couper cet attribut pr ne")
                                print("retenir que le nom du fichier")
                                print(os.path.basename(game.player.stair_actuel))

                                print("on sort, previous_element, current_element, next_element")
                                print("grace au File Processor")
                                print("game.elt contient, par exemple")
                                print("('No previous element', 'stair_1.json', 'stair_2.json')")
                                game.elt = FileProcessor.process_previous_v2(self,
                                                                    game.liste_fichiers_stairs_json,
                                                                    os.path.basename(game.player.stair_actuel))

                                print("la liste des 3 elts renvoyés par le FP")
                                print(game.elt)

                                print("on recupere le nom du fichier qui")
                                print("represente le previous_element")
                                print(game.elt[0])

                                print("on le prefixe avec le nom des dossiers")
                                print("c-a-d 'save/stairs_json'")
                                print("on l'imprime")
                                game.complete_path = os.path.join('save/stairs_json', game.elt[0])
                                print(game.complete_path)

                                print("actualiser le fichier save/player.json")
                                UtilitairesNoPlayer.update_json_file_player(self, "stair_actuel", game.complete_path)

                                print("lire le fichier qui represente le prochain stair")
                                with open(game.complete_path, 'r') as f:
                                    data = json.load(f)

                                # print("obtenir la valeur de la clé 'exit_tile'")
                                game.next_exit_tile_value = data.get('exit_tile', 'Key not found')
                                # print("valeur de game.next_exit_tile_value")
                                # print(game.next_exit_tile_value)

                                # print("obtenir la valeur de la clé 'entry_tile'")
                                game.next_entry_tile_value = data.get('entry_tile', 'Key not found')
                                # print("valeur game.next_entry_tile_value")
                                # print(game.next_entry_tile_value)

                                # print("on fait apparaitre les NPCs")
                                # print("pr cela , il faut d'abord redefinir")
                                # print("game.white_tiles")
                                game.white_tiles = Utilitaires.getWhiteTiles(self, game.complete_path)
                                # print("on remplit la game.liste_npcs")
                                game.liste_npcs = Utilitaires.create_NPCs(self, game.complete_path)

                                # print("on nettoie les canvas et on dessine")
                                # print("le stair precedent")
                                game.canvas01_maps.fill((0, 0, 0))
                                game.canvas04_npcs.fill((0, 0, 0))

                                UtilitairesNoPlayer.draw_map_from_json(self,
                                                                       game.complete_path,
                                                                       game.canvas01_maps)

                                # print("creer 1 instance de la classe Player")
                                # print(" et la placer sur la game.next_exit_tile_value")
                                game.player = Player(game.player.name,
                                                 game.player.strength,
                                                 game.player.attack,
                                                 game.player.defense,
                                                 game.player.life,
                                                 game.player.magic,
                                                 (game.next_exit_tile_value['x'], game.next_exit_tile_value['y']),
                                                 game.player.color,
                                                 game.player.radius,
                                                 game.player.speed,
                                                 game.complete_path)

                                # print("definir la liste des allowed_tiles")
                                game.allowed_tiles = game.utilitairesNoPlayer.getAllowedTiles(game.complete_path)
                                # print("valeur de la liste des allowed tiles")
                                # print(game.allowed_tiles)

                                # =============================================

                                # print("effacer la game.liste_items pr ensuite")
                                # print("la remplir avec les nvelles valeurs")
                                # print("faire de meme avec la game.liste_item_instances")
                                # print("et la game.liste_des_tiles_qui_ont_un_item")
                                game.liste_items.clear()
                                game.liste_item_instances.clear()
                                game.liste_des_tiles_qui_ont_un_item.clear()

                                """
                                la game.liste_items et les instances de item créees
                                dans la boucle for qui suit doivent avoir les memes
                                attributs et il doit y en avoir autant
                                """

                                # print("liste des tiles qui ont des items")
                                game.liste_des_tiles_qui_ont_un_item = Utilitaires.getListeTilesPrPlacerInstancesItem(self, game.complete_path)
                                # print("la valeur de game.liste_des_tiles_qui_ont_un_item")
                                # print(game.liste_des_tiles_qui_ont_un_item)

                                # print("on ajoute la paire cle => valeur")
                                # print("'tile_position' => (x, y)")
                                # print("ds chaque OrderedDict 'weapon' de chaque")
                                # print("'tile_weapon_X'")
                                for key, item in game.liste_des_tiles_qui_ont_un_item.items():
                                    x = item['x']
                                    y = item['y']
                                    game.liste_items.append(item['weapon'])

                                # print("Impression 01, des attributs des items")
                                # print("ecrite ds le fichier json du stair")
                                # print("APRES creat° de la nvelle paire cle => valeur")
                                # for item in game.liste_items:
                                    # print(item)

                                # print("reimpression de la game.liste_des_tiles_qui_ont_un_item")
                                # print("il doit y avoir l'attribut 'tile_position'")
                                # print("ds chaque nested OrderedDict 'weapon'")
                                # print(game.liste_des_tiles_qui_ont_un_item)

                                # create instances for each item in game.liste_items
                                for item in game.liste_items:
                                    if item['type_category'] == 'shield':
                                        shield = Shield(
                                            attack=item['attack'],
                                            defense=item['defense'],
                                            transportable=item['transportable'],
                                            is_ranged=item['is_ranged'],
                                            position=tuple(item['position']),
                                            color=tuple(item['color']),
                                            visible_onto_map=item['visible_onto_map'],
                                            equipe=item['equipe'],
                                            tile_coordinates=item['tile_coordinates']
                                        )
                                        game.liste_item_instances.append(shield)
                                    elif item['type_category'] == 'sword':
                                        sword = Sword(
                                            attack=item['attack'],
                                            defense=item['defense'],
                                            transportable=item['transportable'],
                                            is_ranged=item['is_ranged'],
                                            position=tuple(item['position']),
                                            color=tuple(item['color']),
                                            visible_onto_map=item['visible_onto_map'],
                                            equipe=item['equipe'],
                                            tile_coordinates=item['tile_coordinates']
                                        )
                                        game.liste_item_instances.append(sword)

                                # =============================================

                                # print("dessiner le player")
                                game.player.draw()

                                # print("executer la methode start_game")
                                game.start_game()

                                print("actualiser le fichier save/player.json")
                                UtilitairesNoPlayer.update_json_file_player(self, "stair_actuel", game.complete_path)

                            else:
                                print("Player is on a regular tile.")
                        else:
                            print("player None")
                            print("86303: Erreur program")

                            pygame.quit()
                            sys.exit()

                if event.type == pygame.KEYDOWN:
                    game.key_handler.handle_key_down(event.key)

                for npc in game.liste_npcs:
                    npc.check_collision_with_player(game.player)

                # TODO
                # faire 1 liste des instances de Item pr checker
                # les collis° avec le player
                # il faudra ecrire la methode ds la classe Item et peut-etre
                # la surcharger ds les classes enfant

            # Update the InformationsPanel
            game.informations_panel.update()

            #
            if hasattr(event, 'ui_element'):
                game.manager.process_events(event)

            if running:
                game.manager.update(time_delta)

                game.screen.blit(game.canvas01_maps,
                                 (0, 0))

                game.screen.blit(game.canvas02_buttons,
                                 (game.canvas01_maps.get_width(), 0))

                game.screen.blit(game.canvas03_informations,
                                 (0, game.canvas01_maps.get_height()))

                game.screen.blit(game.canvas05_items, (0, 0))
                game.screen.blit(game.canvas04_npcs, (0, 0))

                # Draw the InformationsPanel onto the
                # screen or canvas03_informations
                game.screen.blit(game.informations_panel, (0, 600))

                #
                if game.player is not None:
                    game.screen.blit(game.player.surface, game.player.position)

                # =============================================================

                #
                if game.start_menu_from_saved_game.active:
                    game.start_menu_from_saved_game.set_player(game.player)

                # =============================================================

                game.canvas05_items.fill((0, 0, 0, 0))
                for item in game.liste_item_instances:
                    item.draw()
                    game.canvas05_items.blit(item._surface,
                                             item._tile_coordinates)

                #
                game.canvas04_npcs.fill((0, 0, 0, 0))
                for npc in game.liste_npcs:
                    npc.move_V2(game.white_tiles)
                    npc.draw()
                    game.canvas04_npcs.blit(npc._surface, npc._position)

                # draw UI elements onto the screen
                game.start_menu_from_saved_game.manager.draw_ui(game.screen)

                pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.monoplayer02_generation()
