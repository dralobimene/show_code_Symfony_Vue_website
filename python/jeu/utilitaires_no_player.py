# utilitaires_no_player.py

import pygame
import pygame_gui
import string
import random
import os
import json
from functools import wraps
from PIL import Image
import psutil
import time
import cv2
import sys
import shutil
from collections import OrderedDict

from classes.Sortie import Sortie
from classes.Entree import Entree


"""
N'oubliez pas que lorsque vous utilisez des méthodes statiques, vous n'aurez pas accès aux variables
d'instance ou aux autres méthodes d'instance de la classe dans ces méthodes. Si vous avez besoin
d'accéder à des données spécifiques à l'instance, vous devez envisager d'utiliser des méthodes
d'instance à la place.
"""


class UtilitairesNoPlayer:

    @staticmethod
    def read_saved_player_json_file_find_actual_stair(file_path):
        """
        Lit un fichier JSON de sauvegarde du joueur et trouve l'escalier actuel.

        :param file_path: Chemin vers le fichier JSON.
        :return: La valeur de l'escalier actuel si elle est présente dans
        le fichier JSON. Sinon, termine le programme.
        """

        """
        Cette méthode lit un fichier JSON de sauvegarde du joueur et trouve
        l'escalier actuel. Elle vérifie d'abord si le fichier existe. Si ce
        n'est pas le cas, elle affiche un message d'erreur et quitte le
        programme. Si c'est le cas, elle ouvre le fichier et vérifie si la
        clé "stair_actuel" existe dans les données JSON. Si c'est le cas,
        elle renvoie la valeur de "stair_actuel". Si ce n'est pas le cas,
        elle affiche à nouveau un message d'erreur et quitte le programme.
        """

        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                json_data = json.load(file)
                if "stair_actuel" in json_data:
                    return json_data["stair_actuel"]
                else:
                    print("")
                    print("depuis la methode")
                    print("utilitaires.py, class: Utilitaires")
                    print("method: read_saved_player_json_file_find_actual_stair")
                    print("la paire 'stair_actuel => valeur' n'a pas été trouvéé")
                    print("13000: Exit program")

                    pygame.quit()
                    sys.exit()
        else:
            print("")
            print("depuis la methode")
            print("utilitaires.py, class: Utilitaires")
            print("method: read_saved_player_json_file_find_actual_stair")
            print("le fichier save/player.json")
            print("est manquant")
            print("12000: Exit program")

            pygame.quit()
            sys.exit()

    # =========================================================================

    # Utilise OrderedDict, pr conserver l'ordre des paires clés => valeurs
    # chargées depuis le fichier json
    # return an OrderedDict with datas from Json file
    def get_data_from_json(self, file_path):
        """
        Récupère les données à partir d'un fichier JSON.

        :param file_path: Chemin vers le fichier JSON.
        :return: Un OrderedDict contenant les données du fichier JSON.
        """

        """
        Cette méthode récupère des données à partir d'un fichier JSON.
        Elle suppose que le fichier existe et elle ne vérifie pas l'existence
        du fichier comme la méthode précédente. Elle ouvre le fichier,
        lit les données JSON dans un OrderedDict pour conserver l'ordre
        des données et renvoie l'OrderedDict.
        """

        """
        if not os.path.exists(file_path):
            print("")
            print(f"{file_path} does not seem exist")
            print("10005: Exit program")

            pygame.quit()
            sys.exit()
        """

        if not os.path.exists(file_path):
            # raise FileNotFoundError(f"No such file or directory: '{file_path}'")
            file_path = "save/stairs_json/stair_1.json"

        with open(file_path, 'r') as file:
            data = json.load(file, object_pairs_hook=OrderedDict)

        return data

    # =========================================================================

    def recuperer_infos_du_stair(self):
        """
        Récupère les informations à partir de l'escalier actuel.

        :return: Un dictionnaire contenant des informations sur les différents
        types de tuiles et les attributs des chambres.
        """

        """
        Cette méthode récupère des informations à partir de l'escalier.
        Elle lit d'abord l'escalier actuel du joueur dans le fichier JSON
        du joueur. Ensuite, elle lit le fichier correspondant stair_X.json.
        Après cela, elle prépare un certain nombre de listes et d'OrderedDicts
        pour stocker les différents types de tuiles
        (blanches, bleues, totales, chambres, sortie, entrée) et les attributs
        des chambres contenus dans le fichier stair_X.json.

        Pour chaque type de tuile ou d'attribut de chambre, elle vérifie si
        les données correspondantes dans le fichier JSON sont du bon type
        (liste de dictionnaires ou dictionnaire), puis elle convertit les
        données dans le format souhaité (OrderedDict ou liste de listes) et
        les stocke dans la variable appropriée.

        Enfin, elle renvoie un dictionnaire contenant toutes les informations
        récupérées. Si à un moment quelconque les données dans le fichier
        JSON ne sont pas du type attendu, elle affiche un message d'erreur
        et quitte le programme.

        Note : Beaucoup de code dans recuperer_infos_du_stair est répété pour
        les différents types de tuiles et d'attributs de chambre.
        Il pourrait être rendu plus concis et maintenable en définissant des
        fonctions auxiliaires qui effectuent les tâches communes.
        """

        # print("")
        # print("Execution method recuperer_infos_du_stair")
        # print("")

        data_du_player = None
        stair_actuel = None

        try:
            with open('save/player.json', 'r') as file:
                data_du_player = json.load(file, object_pairs_hook=OrderedDict)

            stair_actuel = data_du_player['stair_actuel']
        except FileNotFoundError:
            print('File not found. Setting default stair json.')
            stair_actuel = "save/stairs_json/stair_1.json"

        # lire le fichier save/stairs_json/stair_X.json ou
        # stair_X.json correspond a la variable stair_actuel
        script_path = os.path.dirname(os.path.realpath(__file__))
        file_path = script_path + "/" + stair_actuel

        try:
            fichier_stair_json = UtilitairesNoPlayer.get_data_from_json(self, file_path)
        except FileNotFoundError:
            print('File not found. Setting default stair json.')
            default_file_path = script_path + "/save/stairs_json/stair_1.json"
            fichier_stair_json = UtilitairesNoPlayer.get_data_from_json(self,
                                                                        default_file_path)

        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        # creer des arrays (ou OrderedDict) pr stocker les differentes
        # infos contenues ds le fichier save/stairs_json/stair_X.json

        # creer 1 dict pr stocker les infos de la tile "exit_tile"
        # des fichiers save/stairs_json/stair_X.json
        # print("03")
        ordered_exit_tile_dict = None

        # creer 1 dict pr stocker les infos de la tile "entry_tile"
        # des fichiers save/stairs_json/stair_X.json
        # print("04")
        ordered_entry_tile_dict = None

        # creer un list pr stocker les infos de la section  white_tiles_array
        # des fichiers save/stairs_json/stair_X.json
        # print("05")
        white_tiles_list = []

        # creer 1 list pr stocker les infos de la section blue_tiles_array
        # des fichiers save/stairs_json/stair_X.json
        # print("06")
        blue_tiles_list = []

        # creer 1 list pr stocker les infos de la section total_tiles_array
        # des fichiers save/stairs_json/stair_X.json
        # print("07")
        total_tiles_list = []

        # creer 1 list pr stocker les infos de la section rooms_tiles_array
        # des fichiers save/stairs_json/stair_X.json
        # print("08")
        rooms_tiles_list = []

        # creer 1 list pr stocker les infos de la section attributes_rooms_array
        # des fichiers save/stairs_json/stair_X.json
        # print("09")
        attributes_rooms_list = []

        #
        # print("10")
        exit_tile = fichier_stair_json['exit_tile']
        # print("")
        # print("valeur de exit_tile")
        # print(exit_tile)
        # print("")

        #
        entry_tile = fichier_stair_json['entry_tile']
        # print("")
        # print("depuis utilitaires_no_player.py, methode: recuperer_infos_du_stair")
        # print("valeur de entry_tile")
        # print(entry_tile)
        # print("")

        # Ensure that ordered_exit_tile_dict is a dictionary
        if isinstance(fichier_stair_json["exit_tile"], dict):
            # Creating an OrderedDict from exit_tile dictionary
            ordered_exit_tile_dict = OrderedDict(fichier_stair_json["exit_tile"])
            ordered_exit_tile_dict["x"] = int(ordered_exit_tile_dict["x"])
            ordered_exit_tile_dict["y"] = int(ordered_exit_tile_dict["y"])
            ordered_exit_tile_dict["w"] = int(ordered_exit_tile_dict["w"])
            ordered_exit_tile_dict["h"] = int(ordered_exit_tile_dict["h"])
            ordered_exit_tile_dict["center"] = [float(coord) for coord in ordered_exit_tile_dict["center"]]
            ordered_exit_tile_dict["color"] = ordered_exit_tile_dict["color"]
        else:
            print("")
            print("fichier_stair_json['exit_tile'] is not a list, it's a dictionary")
            print("")
            print("12044: Exit program")
            print("")

            pygame.quit()
            sys.exit()

        # Ensure that ordered_entry_tile_dict is a dictionary
        if isinstance(fichier_stair_json["entry_tile"], dict):
            # Creating an OrderedDict from entry_tile dictionary
            ordered_entry_tile_dict = OrderedDict(fichier_stair_json["entry_tile"])
            ordered_entry_tile_dict["x"] = int(ordered_entry_tile_dict["x"])
            ordered_entry_tile_dict["y"] = int(ordered_entry_tile_dict["y"])
            ordered_entry_tile_dict["w"] = int(ordered_entry_tile_dict["w"])
            ordered_entry_tile_dict["h"] = int(ordered_entry_tile_dict["h"])
            ordered_entry_tile_dict["center"] = [float(coord) for coord in ordered_entry_tile_dict["center"]]
            ordered_entry_tile_dict["color"] = ordered_entry_tile_dict["color"]
        else:
            print("")
            print("fichier_stair_json['entry_tile'] is not a list, it's a dictionary")
            print("")
            print("12040: Exit program")
            print("")

            pygame.quit()
            sys.exit()

        # Ensure that white_tiles_list is a list of dictionaries
        if isinstance(fichier_stair_json["white_tiles_array"], list):
            # Iterate over the white_tiles_list and append ordered dictionaries to the OrderedDict
            for tile in fichier_stair_json["white_tiles_array"]:
                ordered_tile = OrderedDict(tile)
                ordered_tile["x"] = int(tile["x"])
                ordered_tile["y"] = int(tile["y"])
                ordered_tile["w"] = int(tile["w"])
                ordered_tile["h"] = int(tile["h"])
                ordered_tile["center"] = [float(coord) for coord in tile["center"]]
                ordered_tile["color"] = tile["color"]
                white_tiles_list.append(ordered_tile)
        else:
            print("")
            print("is not a dictionary but a list of dictionaries")
            print("12045: Exit program")
            print("")

            pygame.quit()
            sys.exit()

        # Ensure that blue_tiles_list is a list of dictionaries
        if isinstance(fichier_stair_json["blue_tiles_array"], list):
            # Iterate over the blue_tiles_list and append ordered dictionaries to the OrderedDict
            for tile in fichier_stair_json["blue_tiles_array"]:
                ordered_tile = OrderedDict(tile)
                ordered_tile["x"] = int(tile["x"])
                ordered_tile["y"] = int(tile["y"])
                ordered_tile["w"] = int(tile["w"])
                ordered_tile["h"] = int(tile["h"])
                ordered_tile["center"] = [float(coord) for coord in tile["center"]]
                ordered_tile["color"] = tile["color"]
                blue_tiles_list.append(ordered_tile)
        else:
            print("")
            print("is not a dictionary but a list of dictionaries")
            print("12046: Exit program")
            print("")

            pygame.quit()
            sys.exit()

        # Ensure that total_tiles_list is a list of dictionaries
        if isinstance(fichier_stair_json["total_tiles_array"], list):
            # Iterate over the total_tiles_list and append ordered dictionaries to the OrderedDict
            for tile in fichier_stair_json["total_tiles_array"]:
                ordered_tile = OrderedDict(tile)
                ordered_tile["x"] = int(tile["x"])
                ordered_tile["y"] = int(tile["y"])
                ordered_tile["w"] = int(tile["w"])
                ordered_tile["h"] = int(tile["h"])
                ordered_tile["center"] = [float(coord) for coord in tile["center"]]
                ordered_tile["color"] = tile["color"]
                total_tiles_list.append(ordered_tile)
        else:
            print("")
            print("is not a dictionary but a list of dictionaries")
            print("12047: Exit program")
            print("")

            pygame.quit()
            sys.exit()

        # Ensure that room_tiles_list is a list of dictionaries
        if isinstance(fichier_stair_json["rooms_tiles_array"], list):
            # Iterate over the rooms_tiles_list and append ordered dictionaries to the OrderedDict
            for room in fichier_stair_json["rooms_tiles_array"]:
                if isinstance(room, list):
                    rooms_tiles_list.append([[int(coord) for coord in tile] for tile in room])
                else:
                    print("")
                    print("is not a dictionary but a list of dictionaries")
                    print("12048: Exit program")
                    print("")

                    pygame.quit()
                    sys.exit()

        # Ensure that attributes_rooms_list is a list of dictionaries
        if isinstance(fichier_stair_json["attributes_rooms_array"], list):
            # Iterate over the attributes_rooms_list and append ordered dictionaries to the OrderedDict
            for room in fichier_stair_json["attributes_rooms_array"]:
                if isinstance(room, dict):
                    ordered_room = OrderedDict(room)
                    ordered_room["x"] = int(room["x"])
                    ordered_room["y"] = int(room["y"])
                    ordered_room["width"] = int(room["width"])
                    ordered_room["height"] = int(room["height"])
                    ordered_room["center"] = [float(coord) for coord in room["center"]]
                    ordered_room["tiles"] = [[int(coord) for coord in tile] for tile in room["tiles"]]
                    attributes_rooms_list.append(ordered_room)
                else:
                    print("")
                    print("is not a dictionary but a list of dictionaries")
                    print("12049: Exit program")
                    print("")

                    pygame.quit()
                    sys.exit()

        # ordered_entry_tile_dict
        entry_tile = fichier_stair_json['entry_tile']
        # print("")
        # print("depuis utilitaires_no_player.py, methode: recuperer_infos_du_stair")
        # print("valeur de entry_tile")
        # print(entry_tile)
        # print("")

        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        #
        return {
                "stair_actuel": stair_actuel,
                "exit_tile": ordered_exit_tile_dict,
                "entry_tile": ordered_entry_tile_dict,
                "white_tiles_list": white_tiles_list,
                "blue_tiles_list": blue_tiles_list,
                "total_tiles_list": total_tiles_list,
                "rooms_tiles_list": rooms_tiles_list,
                "attributes_rooms_list": attributes_rooms_list,
                }

    # =========================================================================

    def get_all_stair_files(self):
        """
        Récupère tous les fichiers d'escalier dans le répertoire
        "save/stairs_json".

        :return: Une liste des noms de tous les fichiers d'escalier,
        triés dans l'ordre numérique.
        """

        """
        Cette méthode récupère tous les fichiers d'escaliers dans le répertoire
        "save/stairs_json". Elle filtre tous les fichiers qui commencent par
        "stair_" et qui se terminent par ".json", puis les trie dans
        l'ordre numérique et les renvoie.
        """

        directory = 'save/stairs_json'
        files_in_directory = os.listdir(directory)
        stair_files = [file for file in files_in_directory if file.startswith('stair_') and file.endswith('.json')]
        # Sort the files
        stair_files_sorted = sorted(stair_files, key=lambda file: int(file.split('_')[1].split('.')[0]))
        return stair_files_sorted

    # =========================================================================

    def get_previous_file(self):
        """
        Récupère le fichier d'escalier précédent dans l'ordre.

        :return: Le nom du fichier d'escalier précédent, ou False si le fichier
        actuel est le premier de la liste.
        """

        """
        Cette méthode récupère le fichier d'escalier précédent dans l'ordre.
        Elle lit d'abord le fichier "player.json", puis extrait la valeur de
        la clé "stair_actuel". Ensuite, elle obtient la liste de tous les
        fichiers d'escalier et trouve l'index du fichier actuel.
        Si le fichier actuel est le premier de la liste, elle affiche un
        message indiquant qu'il n'y a pas de fichier précédent, indique que
        le joueur est sorti du donjon et quitte le jeu. Sinon, elle renvoie
        le fichier précédent.
        """

        # Read "save/player.json"
        with open('save/player.json', 'r') as file:
            data = json.load(file)

        # Extract value from "stair_actuel" key
        current_file = data.get('stair_actuel', '').split('/')[-1]

        # Get list of stair files
        stair_files = self.get_all_stair_files()

        # Find previous file in list
        if current_file in stair_files:
            curr_index = stair_files.index(current_file)
            if curr_index == 0:
                print("Aucun elt precedent")
                print("Vs etes sortis du dongeon")
                print("Vs avez quitté le jeu")

                pygame.quit()
                sys.exit()
            else:
                print("le precedent elt est:")
                return stair_files[curr_index - 1]

        return False

    # =========================================================================

    def get_next_file(self):
        """
        Récupère le fichier d'escalier suivant dans l'ordre.

        :return: Le nom du fichier d'escalier suivant, ou False si le fichier
        actuel est le dernier de la liste.
        """

        """
        Cette méthode est similaire à get_previous_file, mais au lieu de
        chercher le fichier précédent, elle cherche le fichier suivant.
        Si le fichier actuel est le dernier de la liste, elle renvoie False.
        Sinon, elle renvoie le fichier suivant.
        """

        # Read "save/player.json"
        with open('save/player.json', 'r') as file:
            data = json.load(file)

        # Extract value from "stair_actuel" key
        current_file = data.get('stair_actuel', '').split('/')[-1]

        # Get list of stair files
        stair_files = self.get_all_stair_files()

        # Find next file in list
        if current_file in stair_files:
            curr_index = stair_files.index(current_file)
            if curr_index == len(stair_files) - 1:
                # print("Aucun elt suivant")
                return False
            else:
                # print("le suivant elt est:")
                return stair_files[curr_index + 1]

        return False

    # =========================================================================

    @staticmethod
    def suppress_key_from_json_stair_file(filename: str,
                                          first_key: str,
                                          second_key: str):
        """
        Supprime une clé d'un fichier JSON d'escalier.

        :param filename: Le nom du fichier JSON.
        :param first_key: La première clé à vérifier.
        :param second_key: La deuxième clé à supprimer.
        """

        """
        Cette méthode supprime une clé d'un fichier JSON d'escalier.
        Elle prend en paramètre le nom du fichier, la première clé et la
        deuxième clé. Elle vérifie d'abord si la première clé existe dans le
        fichier. Si c'est le cas, elle vérifie ensuite si la deuxième clé
        existe dans la valeur de la première clé. Si c'est le cas, elle
        supprime la deuxième clé et sauvegarde le fichier. Si l'une ou l'autre
        des clés n'existe pas, elle affiche un message indiquant que la clé
        n'existe pas.
        """

        print("")
        print("Execution methode: suppress_key_fromjson_stair_file()")
        print("")

        # Load the JSON file
        with open(filename, 'r') as f:
            data = json.load(f)

        # Check if the first key exists in the data
        if first_key in data:
            # Check if the second key exists in the first key's value
            if second_key in data[first_key]:
                # Remove the second key
                del data[first_key][second_key]
                print(f"The '{second_key}' key has been deleted from '{first_key}'.")
            else:
                print(f"'{second_key}' key doesn't exist in '{first_key}'.")
        else:
            print(f"'{first_key}' doesn't exist in data.")

        # Save the JSON file
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    import json

    # =========================================================================

    @staticmethod
    def update_json_file_player(self, key, new_value):
        """
        Met à jour une clé dans le fichier "player.json" avec une nouvelle valeur.

        :param key: La clé à mettre à jour.
        :param new_value: La nouvelle valeur à définir.
        """

        """
        Cette méthode met à jour une clé dans le fichier "player.json" avec
        une nouvelle valeur. Elle vérifie d'abord si la clé existe dans le
        fichier. Si c'est le cas, elle met à jour la valeur de la clé et
        sauvegarde le fichier. Si la clé n'existe pas, elle affiche un message
        indiquant que la clé n'existe pas.
        """

        # Lire le fichier 'player.json'
        with open('save/player.json', 'r') as file:
            data = json.load(file)

        # Vérifier si la clé existe
        if key in data:
            # Mettre à jour la valeur de la clé
            data[key] = new_value

            # Réécrire le fichier 'player.json' avec la nouvelle valeur
            with open('save/player.json', 'w') as file:
                json.dump(data, file, indent=4)
                print(f"'{key}' a été mis à jour avec la nouvelle valeur : {new_value}")
        else:
            print(f"La clé '{key}' n'existe pas dans 'player.json'.")


    # =========================================================================

    @staticmethod
    def draw_map_from_json(self, file_path, canvas):
        """
        Dessine une carte à partir d'un fichier JSON.

        :param file_path: Le chemin du fichier JSON à lire.
        :param canvas: Le canvas sur lequel dessiner la carte.
        """

        """
        Cette méthode dessine une carte à partir d'un fichier JSON.
        Elle vérifie d'abord si le dossier et le fichier spécifiés existent.
        Si ce n'est pas le cas, elle affiche un message d'erreur et quitte
        le programme. Ensuite, elle lit les données du fichier JSON et les
        dessine sur le canvas. Si des tuiles spécifiques "exit_tile" et
        "entry_tile" sont présentes dans le fichier JSON, elle crée des
        instances de classes Sortie et Entree respectivement, et les dessine
        également sur le canvas.
        """

        folder_path = os.path.dirname(file_path)

        if not os.path.exists(folder_path):
            print("")
            print(f"The folder '{folder_path}' does not exist.")
            print("14101: Exit program")

            pygame.quit()
            sys.exit()

        if not os.path.exists(file_path):
            print("")
            print(f"The file '{file_path}' does not exist.")
            print("14050: Exit program")

            pygame.quit()
            sys.exit()

        with open(file_path, 'r') as file:
            data = json.load(file)

        #
        self.total_tiles_array = data["total_tiles_array"]

        for tile in self.total_tiles_array:
            x = tile['x']
            y = tile['y']
            w = tile['w']
            h = tile['h']
            if tile['color'] == 'white':
                pygame.draw.rect(canvas, self.WHITE, pygame.Rect(x, y, w, h))
            elif tile['color'] == 'blue':
                pygame.draw.rect(canvas, self.BLUE, pygame.Rect(x, y, w, h))

        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # definir des tiles particulieres
        # et les instances des classes Item, Weapon, Sword, Protection ou Shield
        # qui se trouvent sur ces tiles

        # tile sortie qui permet de passer au prochain stair
        # la methode pr passer au prochain stair devrait etre definie
        # ds la classes/Sortie.py je pense
        # Check if "exit_tile" is in the data
        if "exit_tile" in data:
            exit_tile = data["exit_tile"]
            # print("")
            # print("01: exit_tile found in stair json file")
            # print("exit_tile keys and values:")
            # for key, value in exit_tile.items():
                # print(f"{key} => {value}")

            # Extract 'x' and 'y' from JSON
            x = data['exit_tile']['x']
            y = data['exit_tile']['y']

            # Create a Sortie instance
            sortie = Sortie((x, y))

            # Draw sortie
            sortie.draw()
            canvas.blit(sortie.surface, sortie.position)
        else:
            print("")
            print("no exit_tile found in stair json file")
            print("13451: Exit program")

            pygame.quit()
            sys.exit()

        # tile entry qui permet de revenir au précédent stair
        # la methode pr passer au precedent stair devrait etre definie
        # ds la classes/Entree.py je pense
        # Check if "entry_tile" is in the data
        if "entry_tile" in data:
            entry_tile = data["entry_tile"]
            # print("")
            # print("entry_tile found in stair json file")
            # print("entry_tile keys and values:")
            # for key, value in entry_tile.items():
                # print(f"{key} => {value}")

            # Extract 'x' and 'y' from JSON
            x = data['entry_tile']['x']
            y = data['entry_tile']['y']

            # Create a Entree instance
            entree = Entree((x, y))

            # Draw entree
            entree.draw()
            canvas.blit(entree.surface, entree.position)
        else:
            print("")
            print("no entry_tile found in stair json file")
            print("13452: Exit program")

            pygame.quit()
            sys.exit()
        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # =========================================================================

    def getEntryTile(self, stair):
        """
        Récupère la tuile d'entrée d'un escalier à partir du fichier JSON correspondant.

        :param stair: Le nom du fichier JSON de l'escalier.
        :return: La tuile d'entrée.
        """

        # Construct the full path to the JSON file
        # json_file_path = os.path.join('save/stairs_json', stair_actuel)

        # Get the data from the JSON file
        stair_data = UtilitairesNoPlayer.get_data_from_json(self, stair)

        # Get the entry_tile from the data
        tile_entry = stair_data['entry_tile']

        return tile_entry

    # =========================================================================

    def getExitTile(self, stair):
        """
        Récupère la tuile de sortie d'un escalier à partir du fichier JSON correspondant.

        :param stair: Le nom du fichier JSON de l'escalier.
        :return: La tuile de sortie.
        """

         # Construct the full path to the JSON file
        # json_file_path = os.path.join('save/stairs_json', stair_actuel)

        # Get the data from the JSON file
        stair_data = UtilitairesNoPlayer.get_data_from_json(self, stair)

        # Get the exit_tile
        tile_exit = stair_data['exit_tile']

        return tile_exit

    # =========================================================================

    def get_next_exit_tile(self, next_file):
        """
        Récupère la tuile de sortie du prochain fichier dans l'ordre.

        :param next_file: Le nom du prochain fichier.
        :return: Les coordonnées de la tuile de sortie.
        """

        # print("depuis get_next_exit_tile")
        # print("affichage de la valeur du p next_file")
        # print(next_file)

        coords_next_exit_tile = None

        with open(next_file, 'r') as file:
            data = json.load(file)
            coords_next_exit_tile = data.get('exit_tile')

        return coords_next_exit_tile

    # =========================================================================

    def get_next_entry_tile(self, next_file):
        """
        Cette méthode extrait les coordonnées de l'entrée suivante à
        partir d'un fichier JSON.

        :param next_file: Le nom du fichier JSON contenant l'entrée suivante.
        :type next_file: str
        :return: Les coordonnées de l'entrée suivante.
        :rtype: dict
        """

        """
        Define a variable coords_next_entry_tile and initialize it to None.
        Open the file specified by next_file in read mode.
        Load the JSON data from the file.
        Get the value associated with key entry_tile and assign it to
        coords_next_entry_tile.
        Return coords_next_entry_tile.
        """

        # print("depuis get_next_entry_tile")
        # print("affichage de la valeur du p next_file")
        # print(next_file)

        coords_next_entry_tile = None

        with open(next_file, 'r') as file:
            data = json.load(file)
            coords_next_entry_tile = data.get('entry_tile')

        return coords_next_entry_tile

    # =========================================================================

    def getAllowedTiles(self, stair):
        """
        Cette méthode récupère toutes les tuiles autorisées pour un certain
        escalier à partir d'un fichier JSON.

        :param stair: Le nom de l'escalier.
        :type stair: str
        :return: La liste des tuiles autorisées pour l'escalier spécifié.
        :rtype: list
        """

        """
        Construct the full path to the JSON file (code for this is commented out).
        Get the data from the JSON file using get_data_from_json method.
        Get the value associated with key total_tiles_array and assign it to allowed_tiles.
        Return allowed_tiles.
        """

         # Construct the full path to the JSON file
        # json_file_path = os.path.join('save/stairs_json', stair_actuel)

        # Get the data from the JSON file
        stair_data = UtilitairesNoPlayer.get_data_from_json(self, stair)

        # Get the exit_tile
        allowed_tiles = stair_data['total_tiles_array']

        return allowed_tiles

    # =========================================================================

    def recuperer_infos_du_stair_V2(self, stair_actuel):
        """
        Cette méthode récupère diverses informations sur l'escalier actuel à
        partir d'un fichier JSON.

        :param stair_actuel: Le nom de l'escalier actuel.
        :type stair_actuel: str
        :return: Un dictionnaire contenant diverses informations sur l'escalier,
        y compris la tuile de sortie, la tuile d'entrée, la liste des tuiles
        blanches, la liste des tuiles bleues, la liste des tuiles totales,
        la liste des tuiles de la pièce et la liste des attributs de la pièce.
        :rtype: dict
        """

        """
        Initialize variable data_du_player to None.
        Open the player.json file in read mode.
        Load the JSON data from the file.
        Construct the path to the stair JSON file based on stair_actuel.
        Load the data from the stair JSON file.
        Create empty dictionaries and lists to hold the various stair information.
        Check the type of data in exit_tile, entry_tile, white_tiles_array,
        blue_tiles_array, total_tiles_array, rooms_tiles_array, and
        attributes_rooms_array keys. If they are as expected, store their
        values in the corresponding dictionaries and lists.
        If they are not as expected, print error message and exit the program.
        Return a dictionary containing all the stored stair information.
        """

        # print("")
        # print("Execution method recuperer_infos_du_stair")
        # print("")

        data_du_player = None

        with open('save/player.json', 'r') as file:
            data_du_player = json.load(file, object_pairs_hook=OrderedDict)

        # lire le fichier save/stairs_json/stair_X.json ou
        # stair_X.json correspond a la variable stair_actuel
        script_path = os.path.dirname(os.path.realpath(__file__))
        file_path = script_path + "/" + stair_actuel
        fichier_stair_json = UtilitairesNoPlayer.get_data_from_json(self, file_path)

        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        # creer des arrays (ou OrderedDict) pr stocker les differentes
        # infos contenues ds le fichier save/stairs_json/stair_X.json

        # creer 1 dict pr stocker les infos de la tile "exit_tile"
        # des fichiers save/stairs_json/stair_X.json
        # print("03")
        ordered_exit_tile_dict = None

        # creer 1 dict pr stocker les infos de la tile "entry_tile"
        # des fichiers save/stairs_json/stair_X.json
        # print("04")
        ordered_entry_tile_dict = None

        # creer un list pr stocker les infos de la section  white_tiles_array
        # des fichiers save/stairs_json/stair_X.json
        # print("05")
        white_tiles_list = []

        # creer 1 list pr stocker les infos de la section blue_tiles_array
        # des fichiers save/stairs_json/stair_X.json
        # print("06")
        blue_tiles_list = []

        # creer 1 list pr stocker les infos de la section total_tiles_array
        # des fichiers save/stairs_json/stair_X.json
        # print("07")
        total_tiles_list = []

        # creer 1 list pr stocker les infos de la section rooms_tiles_array
        # des fichiers save/stairs_json/stair_X.json
        # print("08")
        rooms_tiles_list = []

        # creer 1 list pr stocker les infos de la section attributes_rooms_array
        # des fichiers save/stairs_json/stair_X.json
        # print("09")
        attributes_rooms_list = []

        #
        # print("10")
        exit_tile = fichier_stair_json['exit_tile']
        # print("")
        # print("valeur de exit_tile")
        # print(exit_tile)
        # print("")

        #
        entry_tile = fichier_stair_json['entry_tile']
        # print("")
        # print("depuis utilitaires_no_player.py, methode: recuperer_infos_du_stair")
        # print("valeur de entry_tile")
        # print(entry_tile)
        # print("")

        # Ensure that ordered_exit_tile_dict is a dictionary
        if isinstance(fichier_stair_json["exit_tile"], dict):
            # Creating an OrderedDict from exit_tile dictionary
            ordered_exit_tile_dict = OrderedDict(fichier_stair_json["exit_tile"])
            ordered_exit_tile_dict["x"] = int(ordered_exit_tile_dict["x"])
            ordered_exit_tile_dict["y"] = int(ordered_exit_tile_dict["y"])
            ordered_exit_tile_dict["w"] = int(ordered_exit_tile_dict["w"])
            ordered_exit_tile_dict["h"] = int(ordered_exit_tile_dict["h"])
            ordered_exit_tile_dict["center"] = [float(coord) for coord in ordered_exit_tile_dict["center"]]
            ordered_exit_tile_dict["color"] = ordered_exit_tile_dict["color"]
        else:
            print("")
            print("fichier_stair_json['exit_tile'] is not a list, it's a dictionary")
            print("")
            print("12044: Exit program")
            print("")

            pygame.quit()
            sys.exit()

        # Ensure that ordered_entry_tile_dict is a dictionary
        if isinstance(fichier_stair_json["entry_tile"], dict):
            # Creating an OrderedDict from entry_tile dictionary
            ordered_entry_tile_dict = OrderedDict(fichier_stair_json["entry_tile"])
            ordered_entry_tile_dict["x"] = int(ordered_entry_tile_dict["x"])
            ordered_entry_tile_dict["y"] = int(ordered_entry_tile_dict["y"])
            ordered_entry_tile_dict["w"] = int(ordered_entry_tile_dict["w"])
            ordered_entry_tile_dict["h"] = int(ordered_entry_tile_dict["h"])
            ordered_entry_tile_dict["center"] = [float(coord) for coord in ordered_entry_tile_dict["center"]]
            ordered_entry_tile_dict["color"] = ordered_entry_tile_dict["color"]
        else:
            print("")
            print("fichier_stair_json['entry_tile'] is not a list, it's a dictionary")
            print("")
            print("12040: Exit program")
            print("")

            pygame.quit()
            sys.exit()

        # Ensure that white_tiles_list is a list of dictionaries
        if isinstance(fichier_stair_json["white_tiles_array"], list):
            # Iterate over the white_tiles_list and append ordered dictionaries to the OrderedDict
            for tile in fichier_stair_json["white_tiles_array"]:
                ordered_tile = OrderedDict(tile)
                ordered_tile["x"] = int(tile["x"])
                ordered_tile["y"] = int(tile["y"])
                ordered_tile["w"] = int(tile["w"])
                ordered_tile["h"] = int(tile["h"])
                ordered_tile["center"] = [float(coord) for coord in tile["center"]]
                ordered_tile["color"] = tile["color"]
                white_tiles_list.append(ordered_tile)
        else:
            print("")
            print("is not a dictionary but a list of dictionaries")
            print("12045: Exit program")
            print("")

            pygame.quit()
            sys.exit()

        # Ensure that blue_tiles_list is a list of dictionaries
        if isinstance(fichier_stair_json["blue_tiles_array"], list):
            # Iterate over the blue_tiles_list and append ordered dictionaries to the OrderedDict
            for tile in fichier_stair_json["blue_tiles_array"]:
                ordered_tile = OrderedDict(tile)
                ordered_tile["x"] = int(tile["x"])
                ordered_tile["y"] = int(tile["y"])
                ordered_tile["w"] = int(tile["w"])
                ordered_tile["h"] = int(tile["h"])
                ordered_tile["center"] = [float(coord) for coord in tile["center"]]
                ordered_tile["color"] = tile["color"]
                blue_tiles_list.append(ordered_tile)
        else:
            print("")
            print("is not a dictionary but a list of dictionaries")
            print("12046: Exit program")
            print("")

            pygame.quit()
            sys.exit()

        # Ensure that total_tiles_list is a list of dictionaries
        if isinstance(fichier_stair_json["total_tiles_array"], list):
            # Iterate over the total_tiles_list and append ordered dictionaries to the OrderedDict
            for tile in fichier_stair_json["total_tiles_array"]:
                ordered_tile = OrderedDict(tile)
                ordered_tile["x"] = int(tile["x"])
                ordered_tile["y"] = int(tile["y"])
                ordered_tile["w"] = int(tile["w"])
                ordered_tile["h"] = int(tile["h"])
                ordered_tile["center"] = [float(coord) for coord in tile["center"]]
                ordered_tile["color"] = tile["color"]
                total_tiles_list.append(ordered_tile)
        else:
            print("")
            print("is not a dictionary but a list of dictionaries")
            print("12047: Exit program")
            print("")

            pygame.quit()
            sys.exit()

        # Ensure that room_tiles_list is a list of dictionaries
        if isinstance(fichier_stair_json["rooms_tiles_array"], list):
            # Iterate over the rooms_tiles_list and append ordered dictionaries to the OrderedDict
            for room in fichier_stair_json["rooms_tiles_array"]:
                if isinstance(room, list):
                    rooms_tiles_list.append([[int(coord) for coord in tile] for tile in room])
                else:
                    print("")
                    print("is not a dictionary but a list of dictionaries")
                    print("12048: Exit program")
                    print("")

                    pygame.quit()
                    sys.exit()

        # Ensure that attributes_rooms_list is a list of dictionaries
        if isinstance(fichier_stair_json["attributes_rooms_array"], list):
            # Iterate over the attributes_rooms_list and append ordered dictionaries to the OrderedDict
            for room in fichier_stair_json["attributes_rooms_array"]:
                if isinstance(room, dict):
                    ordered_room = OrderedDict(room)
                    ordered_room["x"] = int(room["x"])
                    ordered_room["y"] = int(room["y"])
                    ordered_room["width"] = int(room["width"])
                    ordered_room["height"] = int(room["height"])
                    ordered_room["center"] = [float(coord) for coord in room["center"]]
                    ordered_room["tiles"] = [[int(coord) for coord in tile] for tile in room["tiles"]]
                    attributes_rooms_list.append(ordered_room)
                else:
                    print("")
                    print("is not a dictionary but a list of dictionaries")
                    print("12049: Exit program")
                    print("")

                    pygame.quit()
                    sys.exit()

        # ordered_entry_tile_dict
        entry_tile = fichier_stair_json['entry_tile']
        # print("")
        # print("depuis utilitaires_no_player.py, methode: recuperer_infos_du_stair")
        # print("valeur de entry_tile")
        # print(entry_tile)
        # print("")

        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        #
        return {
                "stair_actuel": stair_actuel,
                "exit_tile": ordered_exit_tile_dict,
                "entry_tile": ordered_entry_tile_dict,
                "white_tiles_list": white_tiles_list,
                "blue_tiles_list": blue_tiles_list,
                "total_tiles_list": total_tiles_list,
                "rooms_tiles_list": rooms_tiles_list,
                "attributes_rooms_list": attributes_rooms_list,
                }

    # =========================================================================

    def getStairActuelFromSavePlayerJson(self):
        # Open the JSON file
        with open('save/player.json') as f:
            data = json.load(f)

        # Check if the key exists and display the value or a message
        if 'stair_actuel' in data:
            return data['stair_actuel']
        else:
            print('The key "stair_actuel" does not exist in the JSON file.')
            print("65390: erreur program")

            pygame.quit()
            sys.exit()

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

