import pygame
import random
import time
from pygame import Color
from typing import Tuple

from utilitaires_no_player import UtilitairesNoPlayer

# Constants
SURFACE_SIZE = (800, 600)
TRANSPARENT_COLOR = (0, 0, 0, 0)
NPC_COLOR = (128, 128, 128)
TILE_SIZE = 16


class NPC:

    # variable de classe accessible partout ds le programme
    liste_de_tous_npcs = []

    def __init__(self,
                 NPC_type="monstre",
                 strength=random.randint(10, 100),
                 attack=random.randint(10, 100),
                 defense=random.randint(10, 100),
                 life=random.randint(10, 100),
                 position: Tuple[int, int] = (0, 0),
                 color=NPC_COLOR,
                 radius=8,
                 speed=16,
                 allowed_tiles=None) -> None:
        self._NPC_type = NPC_type
        self._strength = strength
        self._attack = attack
        self._defense = defense
        self._life = life
        self._position = pygame.Vector2(*position)
        self._color = color
        self._radius = radius
        self._speed = speed

        self._surface = pygame.Surface((2*self._radius, 2*self._radius), pygame.SRCALPHA)
        self._surface.fill(TRANSPARENT_COLOR)

        #
        self.last_move_time = time.time()

        # Ajoute ttes les instances créees ds cette liste
        NPC.liste_de_tous_npcs.append(self)

        #
        self.infos_stair_from_json_stair = UtilitairesNoPlayer.recuperer_infos_du_stair(self)

        #
        self._allowed_tiles = self.infos_stair_from_json_stair['total_tiles_list']

    # getters
    @property
    def NPC_type(self) -> str:
        return self._NPC_type

    @property
    def strength(self) -> int:
        return self._strength

    @property
    def attack(self) -> int:
        return self._attack

    @property
    def defense(self) -> int:
        return self._defense

    @property
    def life(self) -> int:
        return self._life

    @property
    def position(self) -> Tuple[int, int]:
        return self._position

    @property
    def color(self) -> Color:
        return self._color

    @property
    def radius(self) -> int:
        return self._radius

    @property
    def surface(self):
        return self._surface

    @property
    def speed(self) -> int:
        return self._speed

    # setters
    @NPC_type.setter
    def NPC_type(self, NPC_type: str) -> None:
        self._NPC_type = NPC_type

    @strength.setter
    def strength(self, strength: int) -> None:
        self._strength = strength

    @attack.setter
    def attack(self, attack: int) -> None:
        self._attack = attack

    @defense.setter
    def defense(self, defense: int) -> None:
        self._defense = defense

    @life.setter
    def life(self, life: int) -> None:
        self._life = life

    @position.setter
    def position(self, position: Tuple[int, int]) -> None:
        self._position = position

    @color.setter
    def color(self, color: Tuple[int, int, int, int]) -> None:
        self._color = color

    @radius.setter
    def radius(self, radius: int) -> None:
        self._radius = radius

    @speed.setter
    def speed(self, speed: int) -> None:
        self._speed = speed

    def draw(self) -> None:
        self._surface.fill(TRANSPARENT_COLOR)
        pygame.draw.circle(self._surface, NPC_COLOR, (self._radius, self._radius), self._radius)
        # print(self._position)

    def move(self) -> None:
        if time.time() - self.last_move_time >= 1:  # check if 1 second has passed
            # Define the range of movement
            move_range = TILE_SIZE

            for _ in range(100):  # limit the number of tries to 100
                # Try to randomly change the NPC's position
                new_position = self._position.copy()
                new_position.x += random.randint(-move_range, move_range)
                new_position.y += random.randint(-move_range, move_range)

                # Check if the new position is inside the allowed tiles
                for tile in self._allowed_tiles:
                    if tile['x'] == new_position.x and tile['y'] == new_position.y:
                        # If it is, update the position and the time of the last movement
                        self._position = new_position
                        self.last_move_time = time.time()
                        return

    def move_V2(self, allowed_tiles=None) -> None:
        if time.time() - self.last_move_time >= 1:  # check if 1 second has passed
            if allowed_tiles is None:
                allowed_tiles = self._allowed_tiles

            # Define the range of movement
            move_range = TILE_SIZE

            for _ in range(100):  # limit the number of tries to 100
                # Try to randomly change the NPC's position
                new_position = self._position.copy()
                new_position.x += random.randint(-move_range, move_range)
                new_position.y += random.randint(-move_range, move_range)

                # Check if the new position is inside the allowed tiles
                for tile in allowed_tiles:
                    if tile['x'] == new_position.x and tile['y'] == new_position.y:
                        # If it is, update the position and the time of the last movement
                        self._position = new_position
                        self.last_move_time = time.time()
                        return


    def check_collision_with_player(self, player):
        npc_rect = pygame.Rect(self._position.x - self._radius, self._position.y - self._radius, self._radius * 2, self._radius * 2)
        player_rect = pygame.Rect(player.position.x - player.radius, player.position.y - player.radius, player.radius * 2, player.radius * 2)
        if npc_rect.colliderect(player_rect):
            print(f"{self._NPC_type} collided with a player!")

    def to_dict(self) -> dict:
        NPC_dict = {
            'NPC_type': self.NPC_type,
            'strength': self.strength,
            'attack': self.attack,
            'defense': self.defense,
            'life': self.life,
            'position': (int(self.position.x), int(self.position.y)),
            'color': self.color,
            'radius': self.radius,
            'speed': self.speed,
        }
        return NPC_dict

    def __str__(self):
        return f'NPC_type={self._NPC_type}:\n,\
                strength={self._strength},\n\
                attack={self._attack},\n\
                defense={self._defense},\n\
                life={self._life},\n\
                position={self._position},\n\
                color={self._color},\n\
                radius={self._radius},\n\
                speed={self._speed}'
