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


class UtilitairesMultiplayerNoPlayer:

    """
    NE SERT PLUS, ON SE SERT DE LA METHODE ORIGINELLE QUI SE TROUVE
    DS LE FICHIER: utilitaires_no_player.py
    """
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

    # =========================================================================

