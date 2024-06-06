from warshard.map import Hexagon

UNIT_CHARACTERISTICS = {
    "infantry": (1, 2, 1, 1),
    "mechanised": (3, 3, 4, 1),
    "armor": (6, 3, 6, 1),
    "artillery": (3, 0, 2, 3),
    "air_wing": (2, 0, 9, 9),
    "hq": (0, 0, 2, 0),
}


class Unit:

    def __init__(self, hexagon_position: Hexagon, type: str) -> None:
        assert type in UNIT_CHARACTERISTICS.keys()
        self.type = type

        stats = UNIT_CHARACTERISTICS[self.type]
        self.power, self.defense, self.mobility, self.range = stats

        self.hexagon_position = hexagon_position


    def _force_move_to(self, hex: Hexagon):
        self.hexagon_position = hex