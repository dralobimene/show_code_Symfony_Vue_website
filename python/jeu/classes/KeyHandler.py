# classes/KeyHandler.py

import pygame

from utilitaires import Utilitaires
from classes.FileProcessor import FileProcessor
from classes.Item import Item
from classes.items.weapons.Weapon import Weapon
from classes.items.weapons.Sword import Sword
from classes.items.protections.Protection import Protection
from classes.items.protections.Shield import Shield


class KeyHandler:
    def __init__(self, player=None):
        self.player = player
        self.key_state = {
            pygame.K_UP: False,
            pygame.K_DOWN: False,
            pygame.K_LEFT: False,
            pygame.K_RIGHT: False
        }

        self.func_key_methods = {
            pygame.K_F1: self.handle_F1,
            pygame.K_F2: self.handle_F2,
            pygame.K_F3: self.handle_F3,
            pygame.K_F4: self.handle_F4,
            pygame.K_F5: self.handle_F5,
        }

        # Create a FileProcessor instance
        self.processor = FileProcessor(Utilitaires.list_files("save/stairs_json"))

    def handle_key_up(self, key):
        if key in self.key_state:
            self.key_state[key] = False

    def handle_key_down(self, key):
        if key in self.key_state:
            self.key_state[key] = True

    def handle_F1(self):
        print("")
        print("F1 pressed")
        print("")

        # print player attributes
        print("player attributes from class Player.py")
        print(self.player)
        print("")

    def handle_F2(self):
        print("")
        print("F2 pressed")
        print("")

        #
        print("infos du stair actuellement visité")
        print(self.player.print_infos_stair())
        print("")

    def handle_F3(self):
        print("")
        print("F3 pressed")
        print("")

        #
        print("iterateur pr trouver le precedent fichier")
        print("ds le dossier save/stairs_json/stair_X.json")
        self.processor.process_previous()
        print("")

    def handle_F4(self):
        print("")
        print("F4 pressed")
        print("")

        #
        print("iterateur pr trouver le prochain fichier")
        print("ds le dossier save/stairs_json/stair_X.json")
        self.processor.process_next()
        print("")

    def handle_F5(self):
        print("")
        print("F5 pressed")
        print("")

        """
        for sword_id, sword in Sword.liste_de_toutes_swords.items():
            print(f"Sword ID: {sword_id}")
            print(f"Attack: {sword.attack}")
            print(f"Defense: {sword.defense}")
            print(f"Transportable: {sword.transportable}")
            print(f"Is Ranged: {sword.is_ranged}")
            print(f"Position: {sword.position}")
            print(f"Tile Coordinates: {sword.tile_coordinates}")
            print(f"Color: {sword.color}")
            print(f"Visible onto Map: {sword.visible_onto_map}")
            print(f"Equipe: {sword.equipe}")
            print("------------")
        """

        print(Protection.liste_de_toutes_protections)
