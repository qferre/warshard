from warshard.config import Config


class Fight:

    def __init__(
        self, defending_melee_unit, attacking_units=[], defending_support_units=[]
    ) -> None:
        self.defending_melee_unit = defending_melee_unit
        self.attacking_units = attacking_units
        self.defending_support_units = defending_support_units

    """ TODO
	self.attacking_units
	self.defending_melee_unit
	self.defending_support_units

	def resolveFight( **args, debug_force_dice_roll_to: int 0 to 6):
		check attacker has at least one melee unit
		check who is in supply
		compute total strength
		compute ratio (remember that support units can be 0 so avoid divide-by-zero ; and round in defender favor ; and cap at what exists in the table)
		check strength ratio for attacker is at least 0.5x defender
		determine result
		force retreats
		clear the unit.involved_in_fight flags for everyone

	def check_possible_retreats:
		for all neighbor hexes, check if they are occupied by enemy units/zoc or impassable
	"""
