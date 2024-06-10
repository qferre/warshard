from warshard.map import Hexagon

from warshard.config import Config


class Unit:

    def __init__(self, hexagon_position: Hexagon, type: str, player_side, id) -> None:

        # TODO self.parent_map = map (we will need to read map functions that check if a move is valid)

        assert type in Config.UNIT_CHARACTERISTICS.keys()
        self.type: str = type  # armor, hq, etc.

        self.player_side = player_side

        stats = Config.UNIT_CHARACTERISTICS[self.type]
        self.power, self.defense, self.mobility, self.range = stats

        self.hexagon_position: Hexagon = hexagon_position
        self.mobility_remaining = 0

        self.id = id  # Unique ID crucial for selection

    def force_move_to(self, hex: Hexagon):
        # TODO used for retreats
        # (and debug in general)
        self.hexagon_position = hex

    """ TODO
	self.attempt_move_to(hex):
		check if enough mobility remaining to move there, and if not occupied (using parent_map.is_accessible_to_player_side(self.side))
		substract mobility cost of target hex to our remainig_mobility
		if in enemy zoc, set remaining mobility to 0

	self.attempt_attack_on_hex(hex, map):
		check if we are within range of desired hex
		check if the hex contains an enemy unit

		if map.all_fights does not have a fight on this hex :
			create a fight and join it
		else:
			join existing fight


	self.attempt_join_defense_on_hex(hex, map):
		check a fight exists at destination
        check we are within range to join it
        join the fight
	"""
