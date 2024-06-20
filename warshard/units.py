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

        self.id = id  # Unique ID crucial for selection # TODO assert that the id always matches the g.map.all_units[27], ie. the key in the dictionary ? Or permit differences ? I think we should assert it.

    def force_move_to(self, hex: Hexagon):
        # TODO used for retreats
        # (and debug in general)
        self.hexagon_position = hex

    def attempt_move_to(self, hex: Hexagon):
        # check if enough mobility remaining to move there, and if not occupied (using parent_map.is_accessible_to_player_side(self.player_side))
        mobility_cost = Config.MOBILITY_COSTS[hex.type]
        hex_is_clear, hex_not_in_enemy_zoc = hex.is_accessible_to_player_side(
            self.player_side
        )
        is_accessible = hex_is_clear

        if (mobility_cost <= self.mobility_remaining) and is_accessible:
            # substract mobility cost of target hex to our remaining_mobility
            self.mobility_remaining -= mobility_cost
            self.force_move_to(hex)  # move there

            # if in enemy zoc, set remaining mobility to 0
            if not hex_not_in_enemy_zoc:
                self.mobility_remaining = 0

    """ TODO

    self.attempt_attack_on_hex(hex):
        check we are not already involved in a fight
        check if we are within range of desired hex
        check if the hex contains an enemy unit

        if self.parent_map.all_fights does not have a fight on this hex :
            create a fight and join it
        else:
            join existing fight


    self.attempt_join_defense_on_hex(hex, map):
        check we are not already involved in a fight
        check a fight exists at destination
        check we are within range to join it and that we are not a melee unit
        join the fight as support
    """
