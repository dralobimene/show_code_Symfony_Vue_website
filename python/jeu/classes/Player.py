
# classes/Player.py

# the @property decorator is used to define getter methods,
# and the @<attribute>.setter decorator is used
# to define setter methods for the private attributes.

# tuples are typically used for heterogeneous data (data of different kinds),
# and lists are used for homogeneous data (data of the same kind)

import pygame
import json
from collections import OrderedDict
from pygame import Color
from typing import Tuple

from utilitaires_no_player import UtilitairesNoPlayer
from classes.Item import Item
from classes.items.weapons.Weapon import Weapon
from classes.items.weapons.Sword import Sword
from classes.items.protections.Protection import Protection
from classes.items.protections.Shield import Shield
from classes.NPC import NPC

# Constants
SURFACE_SIZE = (800, 600)
TRANSPARENT_COLOR = (0, 0, 0, 0)
PLAYER_COLOR = (0, 255, 0)


class Player:
    def __init__(self,
                 name,
                 strength,
                 attack=100,
                 defense=100,
                 life=100,
                 magic=100,
                 position: Tuple[int, int] = (0, 0),
                 color=PLAYER_COLOR,
                 radius=8,
                 speed=16,
                 stair_actuel="save/stairs_json/stair_1.json",
                 id=None) -> None:
        self.__name = name
        self.__strength = strength
        self.__attack = attack
        self.__defense = defense
        self.__life = life
        self.__magic = magic
        self.__position = pygame.Vector2(position[0], position[1])
        self.__color = color
        self.__radius = radius
        self.__speed = speed
        self.__stair_actuel = stair_actuel
        self.__surface = pygame.Surface((2*self.__radius, 2*self.__radius), pygame.SRCALPHA)
        self.__surface.fill(TRANSPARENT_COLOR)

        self.utilitairesNoPlayer = UtilitairesNoPlayer()

        # generate a random string for the id
        # utile pour le multiplayer, pr le management des players ds le
        # fichier server.ts
        # if id is not provided, generate a random string for the id
        self.__id = id if id is not None else self.utilitairesNoPlayer.generate_random_string(20)


        # marque A7
        self.infos_stair_from_json_stair = UtilitairesNoPlayer.recuperer_infos_du_stair_V2(self, self.__stair_actuel)

        self.stair_actuel_from_json_stair = self.infos_stair_from_json_stair['stair_actuel']
        self.exit_tile_from_json_stair = self.infos_stair_from_json_stair['exit_tile']
        self.entry_tile_from_json_stair = self.infos_stair_from_json_stair['entry_tile']
        # self.white_tiles_array_from_json_stair = self.infos_stair_from_json_stair['white_tiles_list']
        # self.blue_tiles_array_from_json_stair = self.infos_stair_from_json_stair['blue_tiles_list']
        self.total_tiles_array_from_json_stair = self.infos_stair_from_json_stair['total_tiles_list']
        # self.rooms_tiles_array_from_json_stair = self.infos_stair_from_json_stair['rooms_tiles_list']
        # self.attributes_rooms_array_from_json_stair = self.infos_stair_from_json_stair['attributes_rooms_list']

        # attribut qui prend la valeur de la variable de classe classes/NPC.py
        self.npcs = NPC.liste_de_tous_npcs

        # attribut qui prend la valeur de la variable de classe classes/Item.py
        # doit denombrer ttes les instances de tous les fichiers stair
        self.items = Item.liste_de_toutes_instances

        # attribut qui prend la valeur de la variable de classe
        # classes/items/weapons/Weapon.py
        # doit denombrer ttes les instances de tous les fichiers stair
        self.weapons = Weapon.liste_de_toutes_weapons

        # attribut qui prend la valeur de la variable de classe
        # classes/items/weapons/Sword.py
        # doit denombrer ttes les instances de tous les fichiers stair
        self.swords = Sword.liste_de_toutes_swords

        # attribut qui prend la valeur de la variable de classe
        # classes/items/protections/Protection.py
        # doit denombrer ttes les instances de tous les fichiers stair
        self.protections = Protection.liste_de_toutes_protections

        # attribut qui prend la valeur de la variable de classe
        # classes/items/weapons/Shield.py
        # doit denombrer ttes les instances de tous les fichiers stair
        self.shields = Shield.liste_de_tous_shields

    # =========================================================================

    # getters
    @property
    def name(self) -> str:
        return self.__name

    @property
    def strength(self) -> int:
        return self.__strength

    @property
    def attack(self) -> int:
        return self.__attack

    @property
    def defense(self) -> int:
        return self.__defense

    @property
    def life(self) -> int:
        return self.__life

    @property
    def magic(self) -> int:
        return self.__magic

    @property
    def position(self) -> Tuple[int, int]:
        return self.__position

    @property
    def color(self) -> Color:
        return self.__color

    @property
    def radius(self) -> int:
        return self.__radius

    @property
    def surface(self) -> pygame.Surface:
        return self.__surface

    @property
    def speed(self) -> int:
        return self.__speed

    @property
    def stair_actuel(self) -> str:
        return self.__stair_actuel

    @property
    def id(self) -> str:
        return self.__id

    # setters
    @name.setter
    def name(self, name: str) -> None:
        self.__name = name

    @strength.setter
    def strength(self, strength: int) -> None:
        self.__strength = strength

    @attack.setter
    def attack(self, attack: int) -> None:
        self.__attack = attack

    @defense.setter
    def defense(self, defense: int) -> None:
        self.__defense = defense

    @life.setter
    def life(self, life: int) -> None:
        self.__life = life

    @magic.setter
    def magic(self, magic: int) -> None:
        self.__magic = magic

    @position.setter
    def position(self, position: Tuple[int, int]) -> None:
        self.__position = position

    @color.setter
    def color(self, color: Tuple[int, int, int, int]) -> None:
        self.__color = color

    @radius.setter
    def radius(self, radius: int) -> None:
        self.__radius = radius

    @speed.setter
    def speed(self, speed: int) -> None:
        self.__speed = speed

    @stair_actuel.setter
    def stair_actuel(self, stair_actuel: str) -> None:
        self.__stair_actuel = stair_actuel

    @id.setter
    def id(self, id: str) -> None:
        self.__id = id

    # =========================================================================

    def handle_events(self, event, npcs, items, ws=None):
        if event.type == pygame.KEYUP:
            new_position = self.__position.copy()
            if event.key == pygame.K_UP:
                new_position.y -= self.speed
            elif event.key == pygame.K_DOWN:
                new_position.y += self.speed
            elif event.key == pygame.K_LEFT:
                new_position.x -= self.speed
            elif event.key == pygame.K_RIGHT:
                new_position.x += self.speed
            elif event.key == pygame.K_SPACE:
                print(" ")
                print("K_SPACE pressed from classe Player.py")
                print("")

                print("valeur de self.items")
                print(self.items)
                print("")

                # self.event_check_if_player_onto_exit_tile()
                # self.event_check_if_player_onto_entry_tile()

                print("les attributs de TOUS les items")
                for item in self.items:
                    print(f"Item: {item.__class__.__name__} with attributes: {item.to_dict()}")
                print("")

                #
                print("valeur de liste_des_tuiles_qui_ont_un_item")
                liste_des_tuiles_qui_ont_un_item = self.get_liste_tiles_pr_placer_instances_item_from_json(self.stair_actuel)
                print(liste_des_tuiles_qui_ont_un_item)
                print("")

                self.get_item_at_position(self.__position, liste_des_tuiles_qui_ont_un_item)

            # Check if the new position is inside total_tiles_array_from_json_stair
            for tile in self.total_tiles_array_from_json_stair:
                if tile['x'] == new_position.x and tile['y'] == new_position.y:
                    self.__position = new_position
                    print(self.position)
                    self.check_collision_with_NPCs(self.npcs)

                    # only send data if ws is provided
                    if ws is not None:

                        # get player data
                        playerData = self.to_dict()

                        # send the updated data to the server
                        ws.send(json.dumps({"event_type": "move", "player": playerData}))

                    break

    # =========================================================================

    def event_check_if_player_onto_exit_tile(self):
        print("")
        print("execution de event_check_if_player_onto_exit_tile method")
        print("")

        exit_tile_coords = [self.exit_tile_from_json_stair['x'], self.exit_tile_from_json_stair['y']]

        if list(self.__position) == exit_tile_coords:
            print("Player on exit_tile")
            print("The player is currently on the stair:")
            print(self.stair_actuel)

            next_stair = self.utilitairesNoPlayer.get_next_file()
            print("The next stair is: ", next_stair)

    # =========================================================================

    def event_check_if_player_onto_entry_tile(self):
        print("")
        print("execution de event_check_if_player_onto_entry_tile method")
        print("")

        entry_tile_coords = [self.entry_tile_from_json_stair['x'], self.entry_tile_from_json_stair['y']]

        if list(self.__position) == entry_tile_coords:
            print("Player on entry_tile")
            print("The player is currently on the stair:")
            print(self.stair_actuel)

            previous_stair = self.utilitairesNoPlayer.get_previous_file()
            print("The previous stair is: ", previous_stair)

    # =========================================================================

    def event_check_if_player_is_onto_item(self, item_list):
        player_coords = [self.__position.x, self.__position.y]

        for item in item_list:
            item_coords = [item._position[0], item._position[1]]
            if player_coords == item_coords:
                print(f"Player is on a {item.__class__.__name__}")
                return item
        return None

    # =========================================================================

    def get_liste_tiles_pr_placer_instances_item_from_json(self, file=None):
        if file is None:
            file = self.__stair_actuel

        #
        if self.__stair_actuel == "save/stairs_json/No previous element":
            print("self.__stair_actuel is 'No previous element'")
            print("il faut redefinir la variable self.__stair_actuel")
            print("il faut lire le fichier    save/player.json")
            print("prendre la cle 'stair_actuel' et l'assiger a l'attribut")
            print("self.__stair_actuel")

        with open('save/player.json', 'r') as f:
            data_player_from_json = json.load(f)
            self.__stair_actuel = data_player_from_json['stair_actuel']
        print("self.__stair_actuel")
        print(self.__stair_actuel)

        with open(self.__stair_actuel, 'r') as f:
            data=json.load(f)

        # Creating an OrderedDict
        ordered_dict=OrderedDict()

        for tile_key, tile_dict in data["liste_tiles_pr_placer_instances_item"].items():
            # Adding to the OrderedDict
            ordered_dict[tile_key]=tile_dict

        return ordered_dict

    # =========================================================================

    def get_item_at_position(self, position, tile_item_dict):
        for key, tile_item in tile_item_dict.items():
            if tile_item['x'] == position.x and tile_item['y'] == position.y:
                print(f"Player is on a {tile_item['weapon']['type_category']} with attributes: {tile_item['weapon']}")
                return tile_item
        return None

    # =========================================================================

    def draw(self) -> None:
        # clear the surface with transparency
        self.__surface.fill(TRANSPARENT_COLOR)
        # Draw the player
        pygame.draw.circle(self.__surface, self.__color, (self.__radius, self.__radius), self.__radius)

    # =========================================================================

    def check_collision_with_NPCs(self, npcs):
        player_rect = pygame.Rect(self.__position.x, self.__position.y, self.__radius * 2, self.__radius * 2)
        for npc in npcs:
            npc_rect = pygame.Rect(npc._position.x, npc._position.y, npc._radius * 2, npc._radius * 2)
            if player_rect.colliderect(npc_rect):
                print("")
                print(f"{self.name} collided with an NPC!")

    # =========================================================================

    # DEBUG
    def print_infos_stair(self) -> None:
        print("")
        print("depuis l'instance du joueur")
        print("on affiche les infos du stair actuellement visité,")
        print("valeur issue du fichier save/stairs_json/stair_X.json")
        # print("valeur de la clé 'name': stair_actuellement visité:")
        # print(self.stair_actuel_from_json_stair)
        print("")
        print("valeurs de la clé 'exit_tile':")
        print(self.exit_tile_from_json_stair)

        print("valeurs de la clé 'entry_tile':")
        print(self.entry_tile_from_json_stair)

        # print("valeurs de la clé 'white_tiles_array':")
        # print(self.white_tiles_array_from_json_stair)

        # print("valeurs de la clé 'blue_tiles_array':")
        # print(self.blue_tiles_array_from_json_stair)

        # print("valeurs de la clé 'total_tiles_array':")
        # print(self.total_tiles_array_from_json_stair)

        # print("valeurs de la clé 'rooms_tiles_array':")
        # print(self.rooms_tiles_array_from_json_stair)

        # print("valeurs de la clé 'attributes_rooms_array':")
        # print(self.attributes_rooms_array_from_json_stair)

    # =========================================================================

    def to_dict(self) -> dict:
        player_dict = {
            'name': self.name,
            'strength': self.strength,
            'attack': self.attack,
            'defense': self.defense,
            'life': self.life,
            'magic': self.magic,
            'position': (int(self.position.x), int(self.position.y)),
            'color': self.color,
            'radius': self.radius,
            'speed': self.speed,
            'stair_actuel': self.stair_actuel,
            'id': self.id
        }
        return player_dict

    # =========================================================================

    def __str__(self):
        return f'name={self.__name}:\n,\
                strength={self.__strength},\n\
                attack={self.__attack},\n\
                defense={self.__defense},\n\
                life={self.__life},\n\
                magic={self.__magic},\n\
                position={self.__position},\n\
                color={self.__color},\n\
                radius={self.__radius},\n\
                speed={self.__speed},\n\
                stair_actuel={self.__stair_actuel},\n\
                id={self.__id}'
