
import pygame
from typing import Tuple
from collections import OrderedDict

from classes.Item import Item

# Constants
TILE_SIZE = 16
TRANSPARENT_COLOR = (0, 0, 0, 0)
# cyan
WEAPON_COLOR = (0, 255, 255)


class Weapon(Item):
    """
    The Weapon class inherits from the Item class and extends it with an additional
    attribute, is_ranged, which specifies whether the weapon is a ranged weapon.
    """

    # variable de classe, dc accessible partout ds le programme
    liste_de_toutes_weapons = OrderedDict()

    def __init__(self,
                 type_category: str,
                 attack: int,
                 defense: int,
                 transportable: bool,
                 is_ranged: bool,
                 position: Tuple[int, int] = (0, 0),
                 color=WEAPON_COLOR,
                 visible_onto_map: bool = True,
                 equipe: bool = False,
                 tile_coordinates: Tuple[int, int] = (0, 0)) -> None:
        super().__init__(type_category,
                         attack,
                         defense,
                         transportable,
                         position,
                         color,
                         visible_onto_map,
                         equipe,
                         tile_coordinates)

        self._is_ranged = is_ranged

        # Ajoute ttes les instances créees ds cette liste
        self.__class__.liste_de_toutes_weapons.update({id(self): self})

    @property
    def is_ranged(self) -> bool:
        return self._is_ranged

    @is_ranged.setter
    def is_ranged(self, is_ranged: bool) -> None:
        self._is_ranged = is_ranged

    def draw(self) -> None:
        self._surface.fill(TRANSPARENT_COLOR)
        pygame.draw.polygon(self._surface, self._color,
                            [(0, TILE_SIZE), (TILE_SIZE // 2, 0), (TILE_SIZE, TILE_SIZE)])

    def to_dict(self):
        item_dict = super().to_dict()
        item_dict["is_ranged"] = self._is_ranged
        return item_dict

    def __str__(self):
        return f"Weapon(type_category={self._type_category},\n\
                attack={self._attack},\n\
                defense={self._defense},\n\
                position={self._position},\n\
                color={self._color},\n\
                transportable={self._transportable},\n\
                visible_onto_map={self._visible_onto_map},\n\
                is_ranged={self._is_ranged},\n\
                tile_coordinates={self._tile_coordinates})"
