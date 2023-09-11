# File: classes/weapons/Sword.py

from typing import Tuple
import random
from collections import OrderedDict

from classes.items.weapons.Weapon import Weapon

# Constants
TILE_SIZE = 16
TRANSPARENT_COLOR = (0, 0, 0, 0)
# red
SWORD_COLOR = (255, 0, 0)


class Sword(Weapon):
    # variable de classe, dc accessible partout ds le programme
    liste_de_toutes_swords = OrderedDict()

    def __init__(self,
                 attack: int = random.randint(2, 20),
                 defense: int = 1,
                 transportable: bool = True,
                 is_ranged: bool = True,
                 position: Tuple[int, int] = (0, 0),
                 color=SWORD_COLOR,
                 visible_onto_map: bool = True,
                 equipe: bool = False,
                 tile_coordinates: Tuple[int, int] = (0, 0)) -> None:
        super().__init__("Sword",
                         attack,
                         defense,
                         transportable,
                         False,
                         position,
                         color,
                         visible_onto_map,
                         equipe,
                         tile_coordinates)

        # Ajoute ttes les instances créees ds cette liste
        self.__class__.liste_de_toutes_swords.update({id(self): self})

    # Override the draw method
    def draw(self) -> None:
        # Call the parent class's draw method
        super().draw()
        # Additional drawing code for Sword (if needed)
        # ...

    def to_dict(self):
        return {
            "type_category": self._type_category,
            "attack": self._attack,
            "defense": self._defense,
            "position": self._position,
            "color": self._color,
            "transportable": self._transportable,
            "visible_onto_map": self._visible_onto_map,
            "equipe": self._equipe,
            "is_ranged": self._is_ranged,
            "tile_coordinates": self._tile_coordinates
        }

    def __str__(self):
        return f"Sword(type_category={self._type_category},\n\
                attack={self._attack},\n\
                defense={self._defense},\n\
                position={self._position},\n\
                color={self._color},\n\
                transportable={self._transportable},\n\
                visible_onto_map={self._visible_onto_map},\n\
                equipe={self._equipe},\n\
                is_ranged={self._is_ranged},\n\
                tile_coordinates={self._tile_coordinates})"
