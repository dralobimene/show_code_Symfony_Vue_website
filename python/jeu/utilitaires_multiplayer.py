# utilitaires_multiplayer.py

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


class UtilitairesMultiplayer:

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

        if not os.path.exists("multiplayer/save/player.json"):
            print("")
            print("multiplayer/save/player.json does not seem exist")
            print("10002: Exit program")

            pygame.quit()
            sys.exit()

        # Open the JSON file
        with open("multiplayer/save/player.json", 'r') as file:
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
        # print("depuis utilitaires_multiplayer.py")
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
