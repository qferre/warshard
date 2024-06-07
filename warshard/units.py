from warshard.map import Hexagon

from warshard.config import Config

class Unit:

    def __init__(self, hexagon_position: Hexagon, type: str, player_side, id) -> None:
        assert type in Config.UNIT_CHARACTERISTICS.keys()
        self.type = type

        self.player_side = player_side

        stats = Config.UNIT_CHARACTERISTICS[self.type]
        self.power, self.defense, self.mobility, self.range = stats

        self.hexagon_position = hexagon_position

        self.id = id


    def _force_move_to(self, hex: Hexagon):
        self.hexagon_position = hex