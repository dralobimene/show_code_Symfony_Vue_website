# utilitaires.py

import pygame
import pygame_gui
import random
import string
import os
import json
import cv2
import sys
import shutil
from copy import deepcopy
from collections import OrderedDict


from classes.Player import Player

from classes.Item import Item
from classes.items.weapons.Weapon import Weapon
from classes.items.weapons.Sword import Sword
from classes.items.protections.Protection import Protection
from classes.items.protections.Shield import Shield

from classes.Sortie import Sortie
from classes.Entree import Entree

from classes.NPC import NPC


"""
N'oubliez pas que lorsque vous utilisez des méthodes statiques, vous n'aurez pas accès aux variables
d'instance ou aux autres méthodes d'instance de la classe dans ces méthodes. Si vous avez besoin
d'accéder à des données spécifiques à l'instance, vous devez envisager d'utiliser des méthodes
d'instance à la place.
"""


class Utilitaires:

    # =========================================================================

    # trouve le nbre de formes d'1 certaine couleur
    @staticmethod
    def find_shapes(image, color_lower, color_upper):
        """
        Cette méthode détecte et renvoie les formes d'une certaine couleur dans une image.

        Paramètres:
        - image: Image d'entrée dans laquelle chercher les formes.
        - color_lower: Tuple ou liste représentant la limite inférieure de la
        plage de couleurs à détecter (dans l'espace colorimétrique HSV).
        - color_upper: Tuple ou liste représentant la limite supérieure de la
        plage de couleurs à détecter (dans l'espace colorimétrique HSV).

        Renvoie une liste de rectangles. Chaque rectangle est un tuple de
        quatre éléments (x, y, largeur, hauteur) où (x, y) sont les coordonnées
        du coin supérieur gauche du rectangle.
        """

        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, color_lower, color_upper)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        rectangles = []
        for contour in contours:
            x, y, width, height = cv2.boundingRect(contour)
            rectangles.append((x, y, width, height))

        return rectangles

    # =========================================================================

    #
    @staticmethod
    def create_save_button(manager):
        """
        Cette méthode crée et renvoie un bouton de sauvegarde.

        Paramètre:
        - manager: Le gestionnaire d'interface utilisateur qui contrôle le bouton.

        Renvoie un objet UIButton qui représente le bouton de sauvegarde.
        """

        save_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((850, 50), (100, 50)),
            text='Save',
            manager=manager)

        return save_button

    # =========================================================================

    # method de tri
    # TUs ecrits
    @staticmethod
    def sort_by_numeric_part(filename):
        """
        Cette méthode extrait la partie numérique d'un nom de fichier et la renvoie.

        Paramètre:
        - filename: Le nom de fichier à partir duquel extraire la partie numérique.

        Renvoie la partie numérique du nom de fichier en tant qu'entier.
        """

        # Extract the numeric part from the file name
        numeric_part = int(filename.split("_")[1].split(".")[0])
        return numeric_part

    # =========================================================================

    # methode de tri
    # TUs ecrits
    @staticmethod
    def get_file_number(file_path):
        """
        Cette méthode extrait le numéro du nom de fichier à partir d'un
        chemin de fichier et le renvoie.

        Paramètre:
        - file_path: Le chemin du fichier à partir duquel extraire le numéro
        du nom de fichier.

        Renvoie le numéro du nom de fichier en tant qu'entier.
        """

        # Extract the number from the file name
        file_name = os.path.basename(file_path)
        file_number = int(file_name.split("_")[1].split(".")[0])
        return file_number

    # =========================================================================

    #
    @staticmethod
    def copy_files(source_folder, destination_folder):
        """
        Cette méthode copie tous les fichiers d'un dossier source vers un
        dossier de destination.

        Paramètres:
        - source_folder: Le chemin du dossier source à partir duquel les
        fichiers doivent être copiés.
        - destination_folder: Le chemin du dossier de destination dans lequel
        les fichiers doivent être copiés.

        Si le dossier source ou le dossier de destination n'existent pas,
        la méthode affiche un message d'erreur et arrête le programme.

        Ne renvoie rien.
        """
        if not os.path.exists(source_folder):
            print("")
            print(f"{source_folder} does not seem exist")
            print("10002: Exit program")

            pygame.quit()
            sys.exit()

        if not os.path.exists(destination_folder):
            print("")
            print(f"{destination_folder} does not seem exist")
            print("10003: Exit program")

            pygame.quit()
            sys.exit()

        # Get the list of files in the source folder
        files = os.listdir(source_folder)

        # Iterate over the files and copy them to the destination folder
        for file in files:
            source_path = os.path.join(source_folder, file)
            destination_path = os.path.join(destination_folder, file)
            shutil.copy2(source_path, destination_path)

    # =========================================================================

    # TUs ecrits
    # sélectionne 1 certain nbre d'elements contenus ds 1 copie
    # parfaite d'1 tableau
    # les stocke ds 1 autre tableau qui sera renvoyé
    # supprime du tableau d'origine (celui en parametre) les elements
    # sélectionnés
    def choose_random_elements_from_array(array, iterations):
        """
        Cette méthode sélectionne un certain nombre d'éléments aléatoires
        d'un tableau sans remplacement.

        Paramètres:
        - array: Le tableau d'où les éléments sont choisis.
        - iterations: Le nombre d'éléments à sélectionner.

        Renvoie une liste des éléments sélectionnés. 
        """

        # Make a deep copy of the original array
        array_copy = deepcopy(array)

        # tableau qui stocke les elts sélectionnés du tableau
        # passé en parametre. C'est ce tableau qui est retourné
        # par la methode
        chosen_elements = []

        for i in range(iterations):
            # choose a random element from the array
            chosen_element = random.choice(array_copy)
            chosen_elements.append(chosen_element)

            # remove the chosen element from the array_copy
            array_copy.remove(chosen_element)

        # nettoyer & supprimer le array_copy

        return chosen_elements

    # =========================================================================

    #
    # canvas = parametre defini aussi ds le constructeur de Player
    # pr pvoir blitter l'instance weapon_instance definie ds la classe
    # Player
    @staticmethod
    def create_player_from_saved_player_json(canvas,
                                             self,
                                             position_override=None,
                                             stair_actuel_override=None):
        """
        Cette méthode crée et renvoie un objet Player à partir des données
        enregistrées dans un fichier JSON.

        Paramètres:
        - canvas: Le canevas sur lequel le joueur sera dessiné.
        - self: Une référence à l'objet qui appelle cette méthode (normalement,
        un objet de la classe qui contient cette méthode).
        - position_override: Si fourni, cette position sera utilisée pour le
        joueur au lieu de la position enregistrée dans le fichier.

        Si le fichier "save/player.json" n'existe pas, la méthode affiche un
        message d'erreur et arrête le programme.

        Renvoie un objet Player initialisé avec les données du fichier.
        """

        if not os.path.exists("save/player.json"):
            print("")
            print("save/player.json does not seem exist")
            print("10002: Exit program")

            pygame.quit()
            sys.exit()

        # Open the JSON file
        with open("save/player.json", 'r') as file:
            # Load the JSON data
            player_data = json.load(file)

        # If a position_override is provided, use it; otherwise use the position from the file
        position = position_override if position_override is not None else player_data['position']

        #
        stair_actuel = stair_actuel_override if stair_actuel_override is not None else player_data['stair_actuel']


        # Initialize a Player object with the data from the file
        player = Player(
            player_data['name'],
            player_data['strength'],
            player_data['attack'],
            player_data['defense'],
            player_data['life'],
            player_data['magic'],
            position,
            player_data['color'],
            player_data['radius'],
            player_data['speed'],
            stair_actuel,
        )

        # print("")
        # print("===============================================")
        # print("depuis utilitaires.py")
        # print("methode: create_player_from_saved_player_json")
        # print("valeur de position")
        # print(position)
        # print("")
        # print("valeur de data_player['position']")
        # print(player_data["position"])
        # print("===============================================")

        # print("valeur DE PLAYER DEPUIS CREATE_PLAYER_FROM_SAVED_PLAYER_JSON")

        return player

    # =========================================================================

    def create_directory_if_not_exists(self, directory):
        """
        Cette méthode crée un répertoire s'il n'existe pas déjà.

        Paramètre:
        - directory: Le chemin du répertoire à créer.

        Si le répertoire existe déjà, la méthode affiche un message indiquant
        que rien n'a été fait.

        Ne renvoie rien.
        """

        print("")
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"{directory} created successfully.")
        else:
            print(f"{directory} already exists, nothing to do")
            print("")

    # =========================================================================

    def count_files_in_folder(self, folder_path):
        """
        count number of file(s) into the folder param

        Args:
            folder_path (str): Path of folder to check

        Returns:
            -1: folder does not exist
            int: number of files into the param folder
        """

        if not os.path.isdir(folder_path):
            # folder does not exist
            print("")
            print("folder save/stairs_json does not exist")
            print("12365: Exit program")
            print("")

            pygame.quit()
            sys.exit()
        else:
            # print("il y a: " +
                  # str(len([f for f in os.listdir(folder_path)])) +
                  # "fichier(s)")

            return len([f for f in os.listdir(folder_path)
                        if os.path.isfile(os.path.join(folder_path, f))])

    # =========================================================================

    # retourne la liste des fichiers trouvés ds le directory
    def list_files(directory):
        """
        Cette méthode renvoie une liste des fichiers dans un répertoire.

        Paramètre:
        - directory: Le chemin du répertoire dont lister les fichiers.

        Renvoie une liste des noms des fichiers dans le répertoire,
        triés par la partie numérique de leur nom.
        """

        file_paths = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                # Ignore directories, only consider files
                if os.path.isfile(os.path.join(root, file)):
                    # Extract the filename without path
                    filename = os.path.basename(file)
                    file_paths.append(filename)

        ordered_file_paths = sorted(file_paths, key=Utilitaires.sort_by_numeric_part)
        return ordered_file_paths

    # =========================================================================

    def create_NPCs(self, stair_actuel):
        """
        Cette méthode crée et renvoie une liste de PNJ (personnages non-joueurs).

        Paramètres:
        - self: Une référence à l'objet qui appelle cette méthode
        (normalement, un objet de la classe qui contient cette méthode).
        - stair_actuel: Le chemin du fichier JSON contenant les données de
        l'escalier actuel.

        La méthode crée entre 3 et 8 PNJ à des positions aléatoires sur des
        carreaux blancs de l'escalier.

        Renvoie une liste d'objets NPC.
        """

        player_data = Utilitaires.get_data_from_json("save/player.json")
        stair_data = Utilitaires.get_data_from_json(stair_actuel)
        # print("STAIR_DATA")
        # print(stair_data)
        tile_player = stair_data['entry_tile']
        tiles_blanches = stair_data['white_tiles_array']
        tiles_blanches_copy = deepcopy(tiles_blanches)
        monsters_number = random.randint(3, 8)
        liste_npcs = []
        liste_npcs.clear()

        if tile_player not in tiles_blanches:
            print("la tile_player n'est pas ds tiles_blanches")
            print("32651: Erreur program")

            pygame.quit()
            sys.exit()

        for i in range(monsters_number):
            # Choose a random element
            element_chosen = random.choice(tiles_blanches_copy)

            # perform actions
            # Extract tile 'x' and 'y'
            x = element_chosen['x']
            y = element_chosen['y']

            # print("=======")
            # print(f"Creating NPC at: {x}, {y}")

            # npc = NPC(position=pygame.Vector2(x, y))
            npc = NPC(position=(x, y))

            # print("***")
            # print(npc.position)

            # Remove the chosen element from the list
            tiles_blanches_copy.remove(element_chosen)

            #
            liste_npcs.append(npc)

        return liste_npcs

    # =========================================================================

    def createItems(self, stair):
        """
        Cette méthode génère des informations pour les instances d'objets
        Item, Sword et Protection 
        dans chaque fichier "save/stairs_json/stair_X.json" lors de la
        génération de ces fichiers. 
        Elle n'instancie pas réellement ces objets, mais écrit seulement leurs
        informations dans les fichiers.

        Paramètres:
        - self: Une référence à l'objet qui appelle cette méthode.
        - stair: Le chemin du fichier JSON contenant les données de l'escalier actuel.

        Retourne une liste vide, puisque cette méthode n'instancie pas réellement d'objets.
        """

        """
        Appellée à la generation des fichiers save/stairs_json pr ecrire
        ds chaque fichier json les infos des instances Item, Sword,
        Protection... qui + tard seront créees lorsqu'on passera d'1 stair à
        l'autre. Ne crée dc aucune instance, seulement des infos ds
        les fichiers save/stairs_json/stair_X.json.
        la V2, elle, creera a proprement parler les instances
        """
        # print("")
        # print("execution de la methode createItems")
        # print("")

        #
        liste_items = []
        liste_items.clear()

        # Load the JSON data
        stair_data = Utilitaires.get_data_from_json(stair)

        # Load the tiles
        tiles = stair_data['liste_tiles_pr_placer_instances_item']

        # For each tile
        for tile_key, tile_value in tiles.items():
            # Generate a random number, 0 (for Sword) or 1 (for Shield)
            random_choice = random.randint(0, 1)

            if random_choice == 0:
                weapon_dict = {
                        'type_category': 'sword',
                        'attack': random.randint(2, 20),
                        'defense': 1,
                        'transportable': True,
                        'is_ranged': True,
                        'position': (0, 0),
                        'color': (255, 0, 0),
                        'visible_onto_map': True,
                        'equipe': False,
                    }

            else:
                weapon_dict = {
                        'type_category': 'shield',
                        'attack': 1,
                        'defense': random.randint(2, 20),
                        'transportable': True,
                        'is_ranged': False,
                        'position': (0, 0),
                        'color': (100, 126, 0),
                        'visible_onto_map': True,
                        'equipe': False,
                    }

            # Now, tiles is updated with the new items. We save it back to the JSON file.
            with open(stair, 'r+') as file:
                data = json.load(file)

                # Add the weapon data to the 'tile_with_item' dictionary
                data['liste_tiles_pr_placer_instances_item'][tile_key]['weapon'] = weapon_dict

                # Move the cursor back to the beginning of the file
                file.seek(0)

                # Write the updated JSON data back to the file
                json.dump(data, file, indent=4)

                # Truncate the file in case the new data is shorter than the original
                file.truncate()

        return liste_items

    # =========================================================================

    def createItems_V2(self, stair):
        """
        Cette méthode crée des instances d'objets Item, Sword et Protection
        en utilisant les informations 
        dans le fichier "save/stairs_json/stair_X.json" correspondant.

        Paramètres:
        - self: Une référence à l'objet qui appelle cette méthode.
        - stair: Le chemin du fichier JSON contenant les données de l'escalier actuel.

        Retourne une liste des objets instanciés.
        """

        print("\nexecution de la methode createItem_V2\n")

        liste_items = []

        # Load the JSON data
        stair_data = Utilitaires.get_data_from_json(stair)

        # Load the tiles
        tiles = stair_data.get('liste_tiles_pr_placer_instances_item', {})

        # Iterate over tiles and select only the ones with visible weapons
        for tile, attributes in tiles.items():
            # Safely get 'weapon' attribute
            weapon = attributes.get('weapon')

            # If weapon exists and is visible on the map
            if weapon and weapon.get('visible_onto_map'):
                type_category = weapon.get('type_category')
                print(f"--- type_category: {type_category}")

                # Depending on weapon type, create an appropriate instance
                if type_category == "Sword":
                    sword = Sword(10, 1, True, True)
                    liste_items.append(sword)
                elif type_category == "Shield":
                    shield = Shield(1, 10, True, False)
                    liste_items.append(shield)

        return liste_items

    # =========================================================================

    def createItems_V3(self, stair):
        """
        Cette méthode est une version améliorée de createItems_V2. 
        Elle ajoute les coordonnées de tuile à chaque objet instancié.

        Paramètres:
        - self: Une référence à l'objet qui appelle cette méthode.
        - stair: Le chemin du fichier JSON contenant les données de l'escalier actuel.

        Retourne un dictionnaire ordonné, avec les clés étant les tuiles et
        les valeurs étant les objets instanciés.
        """

        stair_data = Utilitaires.get_data_from_json(stair)
        tiles_with_items = stair_data.get('liste_tiles_pr_placer_instances_item', {})
        liste_items = OrderedDict()
        for tile, attributes in tiles_with_items.items():
            weapon = attributes.get('weapon')
            if weapon and weapon.get('visible_onto_map'):
                type_category = weapon.get('type_category')
                if type_category == "Sword":
                    sword = Sword(10, 1, True, True)
                    sword.tile_coordinates = (attributes['x'], attributes['y'])
                    liste_items[tile] = sword
                elif type_category == "Shield":
                    shield = Shield(1, 10, True, False)
                    shield.tile_coordinates = (attributes['x'], attributes['y'])
                    liste_items[tile] = shield
        return liste_items

    # =========================================================================

    # Utilise OrderedDict, pr conserver l'ordre des paires clés => valeurs
    # chargées depuis le fichier json
    # return an OrderedDict with datas from Json file
    @staticmethod
    def get_data_from_json(file_path):
        """
        Cette méthode charge des données à partir d'un fichier JSON.

        Paramètre:
        - file_path: Le chemin du fichier JSON à charger.

        Si le fichier n'existe pas, la méthode affiche un message d'erreur
        et arrête le programme.

        Retourne un dictionnaire ordonné contenant les données du fichier JSON.
        """

        if not os.path.exists(file_path):
            print("")
            print(f"{file_path} does not seem exist")
            print("10006: Exit program")

            pygame.quit()
            sys.exit()

        with open(file_path, 'r') as file:
            data = json.load(file, object_pairs_hook=OrderedDict)
        return data

    # =========================================================================

    def getWhiteTiles(self, stair):
        """
        Cette méthode récupère les tuiles blanches (libres) à partir
        des données de l'escalier actuel.

        Paramètres:
        - self: Une référence à l'objet qui appelle cette méthode.
        - stair: Le chemin du fichier JSON contenant les données de l'escalier actuel.

        Retourne une liste des tuiles blanches.
        """

        # Construct the full path to the JSON file
        # json_file_path = os.path.join('save/stairs_json', stair)

        # Get the data from the JSON file
        stair_data = Utilitaires.get_data_from_json(stair)

        # Get the white tiles from the data
        tiles_blanches = stair_data['white_tiles_array']

        return tiles_blanches

    # =========================================================================

    def getListeTilesPrPlacerInstancesItem(self, stair):
        """
        Cette méthode récupère les tuiles qui contiennent des items dont
        l'attribut 'visible_onto_map' est à True.
        """

        """
        Recupere les tiles qui ont des items dt l'attribut 'visible_onto_map'
        est à True
        """

        # Get the data from the JSON file
        stair_data = Utilitaires.get_data_from_json(stair)

        # tiles_item = dictionnaire
        tiles_item = {}
        tiles_item.clear()
        tiles_item = stair_data['liste_tiles_pr_placer_instances_item']

        # Filter the dictionary to only include items where 'visible_onto_map' is True
        tiles_item = {key: value for key, value in tiles_item.items() if value['weapon']['visible_onto_map']}

        return tiles_item

    # =========================================================================

    def getCoordinatesTilesPrPlacerInstancesItem(self, stair):
        """
        Cette méthode récupère les coordonnées des tuiles qui contiennent
        des items dont l'attribut 'visible_onto_map' est à True.
        """

        #
        stair_data = Utilitaires.get_data_from_json(stair)

        # Get the tiles items
        tiles_item = stair_data['liste_tiles_pr_placer_instances_item']

        # Create a new OrderedDict that contains the 'x' and 'y' values
        tile_coordinates = OrderedDict()

        #
        for key, value in tiles_item.items():
            if value['weapon']['visible_onto_map']:
                tile_coordinates[key] = (value['x'], value['y'])

        return tile_coordinates

    # =========================================================================

    """
    verifie ds le fichier json spécifié en parametre si la section:
    'liste_tiles_pr_placer_instances_item', 'weapon', contient la clé
    'tiles_coordinates'. Compte le nbre de x ou elle est présente et le nbre
    de x ou elle n'est pas présente
    Retourne les 2 resultats sous forme de tuple
    """
    def check_tile_coordinates_key(self, file):
        """
        Cette méthode vérifie dans le fichier JSON spécifié si la section
        'liste_tiles_pr_placer_instances_item', 'weapon' contient la clé
        'tiles_coordinates'. Elle compte le nombre de fois où elle est
        présente et le nombre de fois où elle n'est pas présente.
        Elle retourne les deux résultats sous forme de tuple.
        """

        with open(file, 'r') as f:
            data = json.load(f)

        tile_item_dicts = data['liste_tiles_pr_placer_instances_item']

        count_with_key = 0
        count_without_key = 0

        for tile_item_key, tile_item_dict in tile_item_dicts.items():
            if 'tile_coordinates' in tile_item_dict['weapon']:
                count_with_key += 1
            else:
                count_without_key += 1

        return count_with_key, count_without_key

    # =========================================================================

    """
    Compte le nbre de x dans la clé: liste_tiles_pr_placer_instances_item du
    fichier json specifié, il y a de nested dictionnary commançant par:
    'tile_item_'
    """
    def count_tile_items(self, file):
        """
        Cette méthode compte le nombre de dictionnaires imbriqués commençant
        par 'tile_item_' dans la clé 'liste_tiles_pr_placer_instances_item'
        du fichier JSON spécifié.
        """

        with open(file, 'r') as f:
            data = json.load(f)

        tile_item_dicts = data['liste_tiles_pr_placer_instances_item']

        tile_item_count = 0
        for key in tile_item_dicts.keys():
            if key.startswith("tile_item_"):
                tile_item_count += 1

        return tile_item_count

    # =========================================================================

    def generate_random_string(self, length):
        """
        return a random string with 20 characters

        Args: length (int):
            number of characters to compose the string

        Returns:
            the random string
        """

        # Define the possible characters to choose from
        characters = string.ascii_letters + string.digits

        # Generate a random string by randomly choosing characters from the pool
        random_string = ''.join(random.choice(characters) for i in range(length))

        return random_string

    # =========================================================================
    # =========================================================================


class EventManager:

    # =========================================================================

    def __init__(self, game):
        self.game = game
        self.utilitaires = Utilitaires()

    # =========================================================================

    def save_game(self, player_attributes):
        """
        Cette méthode sauvegarde les attributs du joueur dans un fichier JSON.
        """

        # Convert Vector2 position to tuple
        # Check if position is a Vector2 object and convert it to a tuple if needed
        if isinstance(player_attributes['position'], pygame.Vector2):
            position_tuple = (player_attributes['position'].x, player_attributes['position'].y)
            player_attributes['position'] = position_tuple

        # Create a JSON dictionary with player_attributes
        player_data = json.dumps(player_attributes, indent=4)

        try:
            # Write the JSON data to the file
            with open("save/player.json", 'w') as file:
                file.write(player_data)
                print(player_data)
            # print("Player data saved to saved_game/saved_player.json")
            # print("copie des fichiers stairs")
            # print("depuis save/stairs_json")
            # print("vers")
            # print("saved_game/")
            # print("WARNING ne pas se fier a l'horadatage de nautilus")
        except IOError as error:
            print("Error occurred while saving player data:", str(error))
            print("10000: exit program")
            pygame.quit()
            sys.exit()

        # print("")
        # print("FIN de execution de: utilitaires.py, EventManager, save_game()")
        # print("")

    # =========================================================================

    def process_event(self, event, player_attributes):
        """
        Cette méthode gère les événements en fonction de leur type.
        Si l'événement est le bouton 'Save' pressé, elle sauvegarde
        les attributs du joueur.
        """
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if self.game.save_button and event.ui_element == self.game.save_button:
                # print("")
                # print("Execution de utilitaires.py, class EventManager, method: process_event")
                # print("bouton Save clique 01")

                # print("player_attributes depuis process_event")
                # print(player_attributes)
                print("")
                self.save_game(player_attributes)

    def save_game_v2(self, player):
        """
        Cette version de la méthode save_game accepte un objet joueur en
        paramètre, convertit ses attributs en un dictionnaire, puis
        sauvegarde ces attributs dans un fichier JSON.
        """

        player_attributes = player.to_dict()
        player_data = json.dumps(player_attributes, indent=4)
        try:
            with open("save/player.json", 'w') as file:
                file.write(player_data)
        except IOError as error:
            print("")
            print("10128: Exit program")
            print(error)
            print("")

            pygame.quit()
            sys.exit()

    def process_event_v2(self, event, player):
        """
        Cette version de la méthode process_event gère les événements en
        fonction de leur type. Si l'événement est le bouton 'Save'
        pressé, elle sauvegarde les attributs du joueur en utilisant la
        méthode save_game_v2.
        """

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if self.game.start_menu_from_saved_game.button3 and event.ui_element == self.game.start_menu_from_saved_game.button3:
                self.save_game_v2(player)

# =============================================================================
# =============================================================================
# =============================================================================
