
import pygame
from pygame import Surface
from typing import Tuple

# Constants
TILE_SIZE = 16
TRANSPARENT_COLOR = (0, 0, 0, 0)
# blue
ITEM_COLOR = (0, 0, 255)


class Item:
    # variable de classe accessible partout ds le programme
    liste_de_toutes_instances = []

    def __init__(self,
                 type_category: str,
                 attack: int,
                 defense: int,
                 transportable: bool,
                 position: Tuple[int, int] = (0, 0),
                 color=ITEM_COLOR,
                 visible_onto_map: bool = True,
                 equipe: bool = False,
                 tile_coordinates: Tuple[int, int] = (0, 0)) -> None:
        self._type_category = type_category
        self._attack = attack
        self._defense = defense
        self._transportable = transportable
        self._position = position
        self._color = color
        self._visible_onto_map = visible_onto_map
        self._equipe = equipe
        self._tile_coordinates = tile_coordinates

        self._surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        self._surface.fill(self._color)

        # Ajoute ttes les instances créees ds cette liste
        Item.liste_de_toutes_instances.append(self)

    # getters
    @property
    def type_category(self) -> str:
        return self._type_category

    @property
    def attack(self) -> int:
        return self._attack

    @property
    def defense(self) -> int:
        return self._defense

    @property
    def transportable(self) -> bool:
        return self._transportable

    @property
    def position(self) -> Tuple[int, int]:
        return self._position

    @property
    def color(self) -> Tuple[int, int, int]:
        return self._color

    @property
    def surface(self) -> Surface:
        return self._surface

    @property
    def visible_onto_map(self) -> bool:
        return self._visible_onto_map

    @property
    def equipe(self) -> bool:
        return self._equipe

    @property
    def tile_coordinates(self) -> Tuple[int, int]:
        return self._tile_coordinates

    # setters
    @type_category.setter
    def type_category(self, type_category: str) -> None:
        self._type_category = type_category

    @attack.setter
    def attack(self, attack: int) -> None:
        self._attack = attack

    @defense.setter
    def defense(self, defense: int) -> None:
        self._defense = defense

    @transportable.setter
    def transportable(self, transportable: bool) -> None:
        self._transportable = transportable

    @position.setter
    def position(self, position: Tuple[int, int]) -> None:
        self._position = position

    @color.setter
    def color(self, color: Tuple[int, int, int]) -> None:
        self._color = color

    @visible_onto_map.setter
    def visible_onto_map(self, visible_onto_map: bool) -> None:
        self._visible_onto_map = visible_onto_map

    @equipe.setter
    def equipe(self, equipe: bool) -> None:
        self._equipe = equipe

    @tile_coordinates.setter
    def tile_coordinates(self, tile_coordinates: Tuple[int, int]) -> None:
        self._tile_coordinates = tile_coordinates

    def draw(self) -> None:
        self._surface.fill(TRANSPARENT_COLOR)
        pygame.draw.polygon(self._surface, self._color, [(0, TILE_SIZE),
                                                         (TILE_SIZE // 2, 0),
                                                         (TILE_SIZE, TILE_SIZE)])

    def render_not_visible(self):
        if self.visible_onto_map:
            # Get the current screen surface
            screen = pygame.display.get_surface()
            # Draw a rectangle of the background color over the item
            background_color = (255, 255, 255)  # Replace with your background color
            pygame.draw.rect(screen, background_color, (self.position[0], self.position[1], TILE_SIZE, TILE_SIZE))
            # Mark the item as not visible
            self.visible_onto_map = False

    def to_dict(self):
        return {
            "type_category": self._type_category,
            "attack": self._attack,
            "defense": self._defense,
            "transportable": self._transportable,
            "position": self._position,
            "color": self._color,
            "visible_onto_map": self._visible_onto_map,
            "equipe": self._equipe,
            "tile_coordinates": self._tile_coordinates,
        }

    def __str__(self):
        return f"Item(type_category={self._type_category},\n\
                attack={self._attack},\n\
                defense={self._defense},\n\
                position={self._position},\n\
                color={self._color},\n\
                transportable={self._transportable},\n\
                visible_onto_map={self._visible_onto_map},\n\
                equipe={self._equipe},\n\
                tile_coordinates={self._tile_coordinates})"
