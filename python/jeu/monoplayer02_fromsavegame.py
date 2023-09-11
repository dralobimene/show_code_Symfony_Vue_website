import pygame
import pygame_gui

import sys
import os
import json

from classes.Player import Player
from classes.Item import Item
from classes.items.protections.Protection import Protection
from classes.items.protections.Shield import Shield
from classes.items.weapons.Weapon import Weapon
from classes.items.weapons.Sword import Sword

from utilitaires import Utilitaires
from utilitaires import EventManager
from utilitaires_no_player import UtilitairesNoPlayer

from classes.FileProcessor import FileProcessor
from classes.KeyHandler import KeyHandler

from utilitaires import EventManager
from classes.InformationsPanel import InformationsPanel
from classes.StartMenuFromSavedGame import StartMenuFromSavedGame


class GameFromSavedGame:
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
        pygame.display.set_caption('Monoplayer: you are playing the game from saved game')

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
        self.liste_items = None

        #
        self.liste_item_instances = None

    # =========================================================================

    """
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
    """

    # =========================================================================

    """
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

            if self.player is not None:
                print("")
                print("monoplayer02.py, game_start()")
                print("player pas None")
            else:
                print("")
                print("monoplayer02.py, game_start()")
                print("player None")

        else:
            print("No files found in the directory 'save/stairs_json'.")
            print("04: exit program")
            pygame.quit()
            sys.exit()

        # print("")
        # print("fin execution start_game")
        # print("")
    """

    # =========================================================================

    def monoplayer02_generation_from_save_game(self):

        # verifier que le dossier "save" existe
        if os.path.exists("save"):
            print("The 'save' directory exists.")
        else:
            print("The 'save' directory does not exist.")
            print("01: exit program")
            pygame.quit()
            sys.exit()

        # Check if save/player.json exists
        if os.path.isfile("save/player.json"):
            print("File save/player.json already exists.")
        else:
            print("File save/player.json does not exist.")
            print("02: exit program")
            pygame.quit()
            sys.exit()

        # verifier que le dossier "save/stairs_json" existe
        if os.path.exists("save/stairs_json"):
            print("The 'save/stairs_json' directory exists.")
        else:
            print("The 'save/stairs_json' directory does not exist.")
            print("03: exit program")
            pygame.quit()
            sys.exit()

        # effacer les eventuels fichiers presents
        # ds save/stairs_json
        # List elements in "save" folder
        files_in_save_folder = os.listdir('save/stairs_json')

        if len(files_in_save_folder) == 0:
            print("Save/stairs_json folder is empty.")
            print("no good, we ran from a saved game")
            print("10300: Exit program")

            pygame.quit()
            sys.exit()

        # Obtain a list of files in the directory
        json_files = os.listdir("save/stairs_json")

        #
        game.json_files_sorted = sorted(json_files, key=Utilitaires.sort_by_numeric_part)

        print("")
        print("la liste triée des fichiers qui se trouvent ds save/stairs_json")
        print(game.json_files_sorted)
        print("")

        # Check if there is at least one file in the directory
        if json_files:
            print("")
            print("au moins 1 fichier present ds le dossier save/stairs_json")

        else:
            print("No files found in the directory 'save/stairs_json'.")
            print("04: exit program")
            pygame.quit()
            sys.exit()

        """
        #
        game.niveau_visite = game.player.stair_actuel

        print("")
        print("attribut de game.player.stair_actuel:")
        print("normalement cet attribut est = à la valeur trouvée")
        print("ds le fichier de sauvegarde save/player.json")
        print(game.niveau_visite)
        print("")
        """

        #
        game.content_json_file_stair = UtilitairesNoPlayer.recuperer_infos_du_stair(self)

        #
        if game.content_json_file_stair == "save/stairs_json/No previous element":
            game.content_json_file_stair = "save/stairs_json/stair_1.json"

        game.stair_actuel = game.content_json_file_stair['stair_actuel']
        game.exit_tile = game.content_json_file_stair['exit_tile']
        game.entry_tile = game.content_json_file_stair['entry_tile']
        game.white_tiles = game.content_json_file_stair['white_tiles_list']
        game.blue_tiles = game.content_json_file_stair['blue_tiles_list']
        game.total_tiles_list = game.content_json_file_stair['total_tiles_list']
        game.rooms_tiles_list = game.content_json_file_stair['rooms_tiles_list']
        game.attributes_rooms_list = game.content_json_file_stair['attributes_rooms_list']

        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        """
        if game.niveau_visite != game.stair_actuel:
            print("")
            print("14730: Exit program")
            print("valeur de la variable game.niveau_visite:")
            print(game.niveau_visite)
            print("valeur de la variable stair_actuel:")
            print(game.stair_actuel)
            print("")

            pygame.quit()
            sys.exit()
        """

        # =====================================================================

        # DEBUG
        # print("")
        # print("valeur de stair_actuel")
        # print(stair_actuel)

        # print("")
        # print("elts ds le dict exit_tile")
        # print(exit_tile)

        # print("")
        # print("elts ds white_tiles")
        # print(white_tiles)

        # print("")
        # print("valeur de white_tiles[0]")
        # print(white_tiles[0])

        # print("")
        # print("elts ds blue_tiles")
        # print(blue_tiles)

        # print("")
        # print("elts ds total_tiles_list")
        # print(total_tiles_list)

        # print("")
        # print("elts ds rooms_tiles_list")
        # print(rooms_tiles_list)

        # print("")
        # print("elts ds attributes_rooms_list")
        # print(attributes_rooms_list)

        # =====================================================================

        print("on lit l'attribut game.stair_actuel")
        print("depuis le fichier save/player.json")
        game.stair_actuel = UtilitairesNoPlayer.getStairActuelFromSavePlayerJson(self)
        print(game.stair_actuel)

        #
        if game.stair_actuel == "save/stairs_json/No previous element":
            print("game.stair_actuel is 'No previous element'")
            print("redefinition de la variable game.stair_actuel")
            game.stair_actuel = "save/stairs_json/stair_1.json"

        #
        print("re impression de game.stair_actuel pr verif")
        print(game.stair_actuel)


        print("liste des fichiers ds save/stairs_json")
        game.liste_fichiers_stairs_json = game.utilitairesNoPlayer.get_all_stair_files()

        print("il faut couper cet attribut pr ne")
        print("retenir que le nom du fichier")
        print(os.path.basename(game.stair_actuel))

        print("on sort, previous_element, current_element, next_element")
        print("grace au File Processor")
        print("game.elt contient, par exemple")
        print("('No previous element', 'stair_1.json', 'stair_2.json')")
        game.elt = FileProcessor.process_next_v2(self,
                                            game.liste_fichiers_stairs_json,
                                            os.path.basename(game.stair_actuel))

        print("la liste des 3 elts renvoyés par le FP")
        print(game.elt)

        print("on recupere le nom du fichier qui")
        print("represente le current_element")
        print(game.elt[1])

        print("on le prefixe avec le nom des dossiers")
        print("c-a-d 'save/stairs_json'")
        print("on l'imprime")
        game.complete_path = os.path.join('save/stairs_json', game.elt[1])
        print(game.complete_path)

        # print("actualiser le fichier save/player.json")
        # UtilitairesNoPlayer.update_json_file_player(self, "stair_actuel", game.complete_path)

        print("lire le fichier qui represente le current stair")
        with open(game.complete_path, 'r') as f:
            data = json.load(f)

        # print("obtenir la valeur de la clé 'exit_tile'")
        game.exit_tile
        # print(game.exit_tile)

        # print("obtenir la valeur de la clé 'entry_tile'")
        game.entry_tile
        # print(game.entry_tile)

        # print("on va definir")
        # print("la liste des NPCs et la liste des Items")

        # print("pr cela , il faut d'abord redefinir")
        # print("game.white_tiles")
        # print("on placera npcs et items la-dessus")
        game.white_tiles = Utilitaires.getWhiteTiles(self, game.complete_path)
        # print(game.white_tiles)

        # print("on definit la liste des NPCs")
        # print("on remplit la game.liste_npcs")
        game.liste_npcs = Utilitaires.create_NPCs(self, game.complete_path)
        # print(game.liste_npcs)

        # print("on nettoie les canvas et on dessine")
        # print("le nveau stair")
        game.canvas01_maps.fill((0, 0, 0))
        game.canvas05_items.fill((0, 0, 0))
        game.canvas04_npcs.fill((0, 0, 0))

        UtilitairesNoPlayer.draw_map_from_json(self,
                                               game.complete_path,
                                               game.canvas01_maps)

        game.player = Utilitaires.create_player_from_saved_player_json(game.canvas01_maps, self)

        # print("definir la liste des allowed_tiles")
        game.allowed_tiles = game.utilitairesNoPlayer.getAllowedTiles(game.complete_path)
        # print("valeur de la liste des allowed tiles")
        # print(game.allowed_tiles)

        # =====================================================================

        # trouver le nbre de x ou il y a la clé 'tile_item_XXX' ds le
        # dictionnaire 'liste_tiles_pr_placer_instances_item' du fichier
        # json spécifié en parametre
        game.combien_de_tile_item_ds_le_dictionnaire = Utilitaires.count_tile_items(self, game.stair_actuel)
        # print("valeur de game.combien_de_tile_item_ds_le_dictionnaire")
        # print(game.combien_de_tile_item_ds_le_dictionnaire)

        # compte le nbre de x ou la clé 'tile_coordinates' est présente
        # ou pas ds
        # la clé 'weapon, de la clé 'tile_item_X' du dictionnaire
        # 'liste_tiles_pr_placer_instances_item'
        game.count_with_key, game.count_without_key = Utilitaires.check_tile_coordinates_key(self, game.stair_actuel)
        # print("valeur de game.count_with_key")
        # print(game.count_with_key)
        # print("valeur de game.count_without_key")
        # print(game.count_without_key)

        if game.combien_de_tile_item_ds_le_dictionnaire == game.count_with_key:
            print("le fichier avait deja ete lu et les clés")
            print("tile_coordinates ajoutées")

            # print("effacer la game.liste_items pr ensuite")
            # print("la remplir avec les nvelles valeurs")
            # print("faire de meme avec la game.liste_item_instances")
            # print("et la game.liste_des_tiles_qui_ont_un_item")
            game.liste_items = []
            game.liste_item_instances = []
            game.liste_des_tiles_qui_ont_un_item = []

            """
            la game.liste_items et les instances de item créees
            dans la boucle for qui suit doivent avoir les memes
            attributs et il doit y en avoir autant
            """

            # print("liste des tiles qui ont des items")
            game.liste_des_tiles_qui_ont_un_item = Utilitaires.getListeTilesPrPlacerInstancesItem(self, game.stair_actuel)
            # print("la valeur de game.liste_des_tiles_qui_ont_un_item")
            # print(game.liste_des_tiles_qui_ont_un_item)

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
                # print(item)

            # print("reimpression de la game.liste_des_tiles_qui_ont_un_item")
            # print("il doit y avoir l'attribut 'tile_position'")
            # print("ds chaque nested OrderedDict 'weapon'")
            # print(game.liste_des_tiles_qui_ont_un_item)

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

            # print("dessiner le player")
            game.player.draw()

            # print("actualiser le fichier save/player.json")
            # UtilitairesNoPlayer.update_json_file_player(self, "stair_actuel", game.complete_path)

        else:
            print("le fichier n'a pas été lu et les clés 'tiles_coordinates")
            print("n'ont pas été ajoutées'")
            print("cas qui ne doit pas exister ici, puisqu'on charge une partie sauvegardée")

        # =====================================================================

        # Assign the player to the key handler
        game.key_handler = KeyHandler(game.player)

        #
        game.informations_panel.add_message("game loaded")

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

                # =============================================================

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == game.start_menu_from_saved_game.button3:
                        print("Button3 clicked! depuis monoplayer02_fromsavegame.py")

                # =============================================================

                if event.type == pygame.KEYUP:
                    game.key_handler.handle_key_up(event.key)
                    # check if the key is one of the special function keys
                    if event.key in game.key_handler.func_key_methods:
                        # call the corresponding method
                        game.key_handler.func_key_methods[event.key]()

                    elif event.key == pygame.K_SPACE:
                        print("================================================")
                        print("SPACE key pressed")
                        print("event from monoplayer02_fromsavegame.py")
                        print(f"Player position: {game.player.position}")
                        if game.player is not None:

                            # etant donné qu'on va creer une nvelle instance
                            # de la classe Player, on ne peut pas lire
                            # l'attribut game.player.stair_actuel
                            print("Le player visite d'apres")
                            print("game.stair_actuel, le stair:")
                            print(game.stair_actuel)

                            print("le fichier " + game.stair_actuel)
                            print("est logiquement le fichier qui decrit le stair")

                            # print("on redefinit game.exit_tile")
                            # print("et la cle game.entry_tile")
                            with open(game.player.stair_actuel, 'r') as f:
                                data = json.load(f)
                            # print("obtenir la valeur de la clé 'exit_tile'")
                            game.exit_tile = data.get('exit_tile', 'Key not found')
                            # print("valeur de game.exit_tile")
                            # print(game.exit_tile)
                            # print("obtenir la valeur de la clé 'entry_tile'")
                            game.entry_tile = data.get('entry_tile', 'Key not found')
                            # print("valeur de game.entry_tile")
                            # print(game.entry_tile)

                            # print("coordonnées de l'actuelle exit_tile")
                            game.exit_tile_coords = [game.exit_tile['x'], game.exit_tile['y']]
                            # print(game.exit_tile_coords)

                            # print("coordonnées de l'actuelle entry_tile")
                            game.entry_tile_coords = [game.entry_tile['x'], game.entry_tile['y']]
                            # print(game.entry_tile_coords)

                            if game.player_position == game.exit_tile_coords:

                                print("Player is on the exit tile.")
                                print("on lit l'attribut game.player.stair_actuel")
                                print(game.player.stair_actuel)

                                # print("on lit le nom des fichiers qui se trouvent")
                                # print("dans save/stairs_json")
                                # print(game.liste_fichiers_stairs_json)

                                # print("il faut couper cet attribut pr ne")
                                # print("retenir que le nom du fichier")
                                # print(os.path.basename(game.player.stair_actuel))

                                # print("on sort, previous_element, current_element, next_element")
                                # print("grace au File Processor")
                                # print("game.elt contient, par exemple")
                                # print("('No previous element', 'stair_1.json', 'stair_2.json')")
                                game.elt = FileProcessor.process_next_v2(self,
                                                                    game.liste_fichiers_stairs_json,
                                                                    os.path.basename(game.player.stair_actuel))

                                # print("la liste des 3 elts renvoyés par le FP")
                                # print(game.elt)

                                # print("on recupere le nom du fichier qui")
                                # print("represente le next_element")
                                # print(game.elt[2])

                                # print("on le prefixe avec le nom des dossiers")
                                # print("c-a-d 'save/stairs_json'")
                                # print("on l'imprime")
                                game.complete_path = os.path.join('save/stairs_json', game.elt[2])
                                # print(game.complete_path)

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

                                # =============================================

                                # print("on fait apparaitre les NPCs")
                                # print("pr cela , il faut d'abord redefinir")
                                # print("game.white_tiles")
                                game.white_tiles = Utilitaires.getWhiteTiles(self, game.complete_path)
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

                                # print("creer 1 instance de la classe Player")
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

                                # print("XXX: Affichage des attributs du player")
                                # print(str(game.player))

                                # =============================================

                                # print("definir la liste des allowed_tiles")
                                game.allowed_tiles = game.utilitairesNoPlayer.getAllowedTiles(game.complete_path)
                                # print("valeur de la liste des allowed tiles")
                                # print(game.allowed_tiles)

                                # =============================================

                                # trouver le nbre de x ou il y a la clé 'tile_item_XXX' ds le
                                # dictionnaire 'liste_tiles_pr_placer_instances_item' du fichier
                                # json spécifié en parametre
                                game.combien_de_tile_item_ds_le_dictionnaire = Utilitaires.count_tile_items(self, game.complete_path)
                                # print("valeur de game.combien_de_tile_item_ds_le_dictionnaire")
                                # print(game.combien_de_tile_item_ds_le_dictionnaire)

                                # compte le nbre de x ou la clé 'tile_coordinates' est présente
                                # ou pas ds
                                # la clé 'weapon, de la clé 'tile_item_X' du dictionnaire
                                # 'liste_tiles_pr_placer_instances_item'
                                game.count_with_key, game.count_without_key = Utilitaires.check_tile_coordinates_key(self, game.complete_path)
                                # print("valeur de game.count_with_key")
                                # print(game.count_with_key)
                                # print("valeur de game.count_without_key")
                                # print(game.count_without_key)

                                if game.combien_de_tile_item_ds_le_dictionnaire == game.count_with_key:
                                    print("le fichier avait deja ete lu et les clés")
                                    print("'tile_coordinates' ajoutées")

                                    # print("effacer la game.liste_items pr ensuite")
                                    # print("la remplir avec les nvelles valeurs")
                                    # print("faire de meme avec la game.liste_item_instances")
                                    # print("et la game.liste_des_tiles_qui_ont_un_item")
                                    game.liste_items.clear()
                                    # on redefinit la game.liste_item_instances qui etait à None
                                    game.liste_item_instances = []
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

                                    # print("on lit la paire cle => valeur")
                                    # print("'tile_position' => (x, y)")
                                    # print("ds chaque OrderedDict 'weapon' de chaque")
                                    # print("'tile_weapon_X'")
                                    for key, item in game.liste_des_tiles_qui_ont_un_item.items():
                                        x = item['x']
                                        y = item['y']
                                        game.liste_items.append(item['weapon'])

                                    # print("Impression 01, des attributs des items")
                                    # print("ecrite ds le fichier json du stair")
                                    # print("APRES creat° de la nvelle paire cle => valeur")
                                    # for item in game.liste_items:
                                        # print(item)

                                    # print("reimpression de la game.liste_des_tiles_qui_ont_un_item")
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

                                else:
                                    print("le fichier n'a pas été lu et les clés 'tiles_coordinates")
                                    print("n'ont pas été ajoutées")

                                    # print("effacer la game.liste_items pr ensuite")
                                    # print("la remplir avec les nvelles valeurs")
                                    # print("faire de meme avec la game.liste_item_instances")
                                    # print("et la game.liste_des_tiles_qui_ont_un_item")
                                    game.liste_items.clear()
                                    # on redefinit la game.liste_item_instances qui etait à None
                                    game.liste_item_instances = []
                                    game.liste_des_tiles_qui_ont_un_item.clear()
                                    game.liste_des_tiles_qui_ont_un_item = Utilitaires.getListeTilesPrPlacerInstancesItem(self, game.complete_path)
                                    # print(game.liste_des_tiles_qui_ont_un_item)

                                    # on lit le fichier save/stairs_json/stair_X.json
                                    # on va ajouter une nvelle paire clé => valeur
                                    # nommée 'tile_position' qui se trouvera ds chaque nested
                                    # dictionnaire, sect°: 'liste_tiles_pr_placer_instances_item'
                                    # 'weapon', cette nvelle paire prend la valeur des
                                    # coordonnées de la tile qui possede l'item
                                    with open(game.complete_path, 'r') as f:
                                        data = json.load(f)

                                    # print("on cree la nvelle paire clé => valeur")
                                    # print("'tile_position' => (x, y)")
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

                                    # print("Impression 01, des attributs des items")
                                    # print("ecrite ds le fichier json du stair")
                                    # print("APRES creat° de la nvelle paire cle => valeur")
                                    # print("on imprime d'apres la game.liste_items")
                                    # for item in game.liste_items:
                                        # print(item)

                                    # print("reimpression de la game.liste_des_tiles_qui_ont_un_item")
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
                                #game.start_game()

                                print("actualiser le fichier save/player.json")
                                UtilitairesNoPlayer.update_json_file_player(self, "stair_actuel", game.complete_path)

                            elif game.player_position == game.entry_tile_coords:

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
                                # print("valeur de game.next_exit_tile_value")
                                # print(game.next_exit_tile_value)

                                # print("obtenir la valeur de la clé 'entry_tile'")
                                game.next_entry_tile_value = data.get('entry_tile', 'Key not found')
                                # print("valeur game.next_entry_tile_value")
                                # print(game.next_entry_tile_value)

                                # print("on fait apparaitre les NPCs")
                                # print("pr cela , il faut d'abord redefinir")
                                # print("game.white_tiles")
                                game.white_tiles = Utilitaires.getWhiteTiles(self, game.complete_path)
                                # print("on remplit la game.liste_npcs")
                                game.liste_npcs = Utilitaires.create_NPCs(self, game.complete_path)

                                # print("on nettoie les canvas et on dessine")
                                # print("le stair precedent")
                                game.canvas01_maps.fill((0, 0, 0))
                                game.canvas04_npcs.fill((0, 0, 0))

                                UtilitairesNoPlayer.draw_map_from_json(self,
                                                                       game.complete_path,
                                                                       game.canvas01_maps)

                                # print("creer 1 instance de la classe Player")
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

                                # print("definir la liste des allowed_tiles")
                                game.allowed_tiles = game.utilitairesNoPlayer.getAllowedTiles(game.complete_path)
                                # print("valeur de la liste des allowed tiles")
                                # print(game.allowed_tiles)

                                # =============================================
                                # trouver le nbre de x ou il y a la clé 'tile_item_XXX' ds le
                                # dictionnaire 'liste_tiles_pr_placer_instances_item' du fichier
                                # json spécifié en parametre
                                game.combien_de_tile_item_ds_le_dictionnaire = Utilitaires.count_tile_items(self, game.player.stair_actuel)
                                # print("valeur de game.combien_de_tile_item_ds_le_dictionnaire")
                                # print(game.combien_de_tile_item_ds_le_dictionnaire)

                                # compte le nbre de x ou la clé 'tile_coordinates' est présente
                                # ou pas ds
                                # la clé 'weapon, de la clé 'tile_item_X' du dictionnaire
                                # 'liste_tiles_pr_placer_instances_item'
                                game.count_with_key, game.count_without_key = Utilitaires.check_tile_coordinates_key(self, game.player.stair_actuel)
                                # print("valeur de game.count_with_key")
                                # print(game.count_with_key)
                                # print("valeur de game.count_without_key")
                                # print(game.count_without_key)

                                if game.combien_de_tile_item_ds_le_dictionnaire == game.count_with_key:
                                    print("le fichier avait deja ete lu et les clés")
                                    print("tile_coordinates ajoutées")

                                    # print("effacer la game.liste_items pr ensuite")
                                    # print("la remplir avec les nvelles valeurs")
                                    # print("faire de meme avec la game.liste_item_instances")
                                    # print("et la game.liste_des_tiles_qui_ont_un_item")
                                    game.liste_items.clear()
                                    # on redefinit la game.liste_item_instances qui etait à None
                                    game.liste_item_instances = []
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

                                    # print("on ajoute la paire cle => valeur")
                                    # print("'tile_position' => (x, y)")
                                    # print("ds chaque OrderedDict 'weapon' de chaque")
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

                                    # print("reimpression de la game.liste_des_tiles_qui_ont_un_item")
                                    # print("il doit y avoir l'attribut 'tile_position'")
                                    # print("ds chaque nested OrderedDict 'weapon'")
                                    # print(game.liste_des_tiles_qui_ont_un_item)

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

                                else:
                                    print("le fichier n'a pas été lu et les clés 'tiles_coordinates")
                                    print("n'ont pas été ajoutées")
                                    print("ce cas ne doit pas exister")

                                # =============================================

                                # print("dessiner le player")
                                game.player.draw()

                                # print("executer la methode start_game")
                                #game.start_game()

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
                    # check if the key is one of the special function keys
                    if event.key in game.key_handler.func_key_methods:
                        # call the corresponding method
                        game.key_handler.func_key_methods[event.key]()

                    elif event.key == pygame.K_SPACE:
                        print("SPACE key pressed")
                        print("event from monoplayer02_fromsavegame.py")
                        print(f"Player position: {game.player.position}")
                        # print(f"Exit tile: {game.exit_tile}")
                        # print(f"Entry tile: {game.entry_tile}")
                        if game.player is not None:
                            """
                            print("")
                            print("player pas None")
                            print("liste des fichiers ds save/stairs_json")
                            game.liste_fichiers_stairs_json = game.utilitairesNoPlayer.get_all_stair_files()
                            print(game.liste_fichiers_stairs_json)
                            print("le previous stair est: ")
                            game.previous_stair = game.utilitairesNoPlayer.get_previous_file()
                            print(game.previous_stair)
                            print("le next stair est: ")
                            game.next_stair = game.utilitairesNoPlayer.get_next_file()
                            print(game.next_stair)
                            """
                            # Check if the player is on the exit_tile or entry_tile
                            game.player_position = [round(game.player.position.x), round(game.player.position.y)]
                            # Create lists for exit_tile and entry_tile coordinates.
                            game.exit_tile_coords = [game.exit_tile['x'], game.exit_tile['y']]
                            game.entry_tile_coords = [game.entry_tile['x'], game.entry_tile['y']]

                            if game.player_position == game.exit_tile_coords:
                                print("Player is on the exit tile.")
                            elif game.player_position == game.entry_tile_coords:
                                print("Player is on the entry tile.")
                                print("NOTE")
                                print("pas execute si on est au 1° stair")
                                print("car il n'y a pas de previous file")
                            else:
                                print("Player is on a regular tile.")

                        else:
                            print("player None")
                            print("86303: Erreur program")

                            pygame.quit()
                            sys.exit()

                for npc in game.liste_npcs:
                    npc.check_collision_with_player(game.player)

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

                #game.manager.draw_ui(game.screen)

                pygame.display.update()


if __name__ == '__main__':
    game = GameFromSavedGame()
    game.monoplayer02_generation_from_save_game()
