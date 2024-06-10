from warshard.config import Config


class Fight:
    raise NotImplementedError

    """ TODO
    self.attacking_player_id
	self.defending_player_id
	self.hexagon
	self.attacking_melee_units
	self.attacking_support
	self.defending_melee_unit
	self.defending_support

	def resolveFight():
		check attacker has at least one melee unit
		check who is in supply
		compute total strength
		compute ratio (remember that support units can be 0 so avoid divide-by-zero)
		check strength ratio for attacker is at least 0.5x defender
		determine result
		force retreats

	def check_possible_retreats:
		for all neighbor hexes, check if they are occupied by enemy units/zoc or impassable
    """
