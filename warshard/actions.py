import numpy as np
import random

from warshard.config import Config


class Order:
    # TODO use in pending_orders, as an automatic casting of what is entered (allow the user to enter orders
    # as (unit_id, hex_x, hex_y) where each is a string

    def __init__(self, unit_id, hex_x, hex_y, map):
        self.map = map
        self.unit_id = unit_id
        self.hex_x, self.hex_y = hex_x, hex_y

        # Find unit with same ID
        self.unit_ref = map.fetch_unit_by_id(self.unit_id)

        # Find hexagon with same coordinates
        self.hexagon_ref = map.fetch_hex_by_coordinate(self.hex_x, self.hex_y)

        # TODO Optional : specify an order type. Useful for instance to pre-plan retreats and not have them executed as regular movements in the movement phase
        # for example, you can say that unit 12 should retreat to hex 4,5 if beaten in combat, but you don't wnat it to move during the movement phase
        # and abandon the field!
        # self.order_type


class Fight:

    def __init__(
        self,
        defending_melee_unit,
        fight_hexagon,
        attacking_units=[],
        defending_support_units=[],
    ) -> None:
        self.defending_melee_unit = defending_melee_unit
        self.attacking_units = attacking_units
        self.defending_support_units = defending_support_units
        self.fight_hexagon = fight_hexagon

        self.parent_map = (
            self.fight_hexagon.parent_map
        )  # Deduce parent map from hexagon

    def resolve(self, putative_retreats, debug_force_dice_roll_to: int = None):
        # TODO Specify in typing : putative_retreats should be a list of Orders
        # TODO Specify this whenever we pass lists of Orders

        if debug_force_dice_roll_to is not None:
            assert 1 <= debug_force_dice_roll_to <= 6

        # Check attacker has at least one melee unit
        if not any([u.type in Config.MELEE_UNITS for u in self.attacking_units]):
            return

        # Check who is in supply, and apply penalty if not
        attacker_is_in_supply = all(
            [
                attacking_unit.hexagon_position
                in self.parent_map.hexes_currently_in_supply_per_player[
                    attacking_unit.player_side
                ]
                for attacking_unit in self.attacking_units
            ]
        )
        defender_is_in_supply = (
            self.fight_hexagon
            in self.parent_map.hexes_currently_in_supply_per_player[
                self.defending_melee_unit.player_side
            ]
        )

        print("supply", attacker_is_in_supply, defender_is_in_supply)

        supply_strength_ratio_modifier = 0
        if not attacker_is_in_supply:
            supply_strength_ratio_modifier += -1
        if not defender_is_in_supply:
            supply_strength_ratio_modifier += 1

        # Compute total strength
        # NOTE support units always contribute their power, we only check the defence stat of the defending melee unit
        total_attacker_strength = sum([u.power for u in self.attacking_units])
        defender_melee_strength = (
            self.defending_melee_unit.defence
            * Config.DEFENDER_MULTIPLIER[self.fight_hexagon.type]
        )  # Apply defender terrain modifier
        total_defender_strength = (
            sum([u.power for u in self.defending_support_units])
            + defender_melee_strength
        )

        print(total_attacker_strength, total_defender_strength)

        # Compute ratio (remember that support units can have 0 melee defence so avoid divide-by-zero)
        strength_ratio = total_attacker_strength / total_defender_strength + 1e-10

        # Add supply modifier to the strength_ratio
        strength_ratio += supply_strength_ratio_modifier

        # Check strength ratio for attacker is at least 0.5x defender
        if strength_ratio < 0.5:
            return
        # Round ratio and round in defender favor ; and cap at what exists in the table)
        strength_ratio = max(
            (x for x in Config.FIGHT_RESULT_TABLE.keys() if x <= strength_ratio),
            default=None,
        )

        print(strength_ratio)

        # Determine result
        # Roll dice and fetch result on the table
        if debug_force_dice_roll_to is not None:
            dice_roll = debug_force_dice_roll_to
        else:
            dice_roll = np.random.choice(Config.DICE_VALUES)

        fight_result = Config.FIGHT_RESULT_TABLE[strength_ratio][dice_roll]

        print(dice_roll, fight_result)

        self.fight_result = fight_result  # Remember the result of the fight, we will need it for the advancing phase

        # --------------------- Result of the fight
        units_that_must_retreat = []
        units_to_destroy = []

        # First, in any case, clear the unit.involved_in_fight flags for everyone (set them to None)
        all_units = (
            self.attacking_units
            + self.defending_support_units
            + [self.defending_melee_unit]
        )
        for u in all_units:
            u.involved_in_fight = None

        # Stalemate
        if fight_result == "S":
            return

        # Defender melee unit retreats
        elif fight_result == "dr":
            units_that_must_retreat.append(self.defending_melee_unit)

        # All attacker units retreat (melee only)
        elif fight_result == "ar":
            for attacking_unit in self.attacking_units:
                if attacking_unit.type in Config.MELEE_UNITS:
                    units_that_must_retreat.append(attacking_unit)

        # All defending units eliminated
        elif fight_result == "DE":
            units_to_destroy.append(self.defending_melee_unit)
            for defending_support_unit in self.defending_support_units:
                units_to_destroy.append(defending_support_unit)

        # All attacking units eliminated
        elif fight_result == "AE":
            for attacking_unit in self.attacking_units:
                units_to_destroy.append(attacking_unit)

        # Defending melee unit and least powerful attacking unit eleminated (ties broken randomly)
        elif fight_result == "EX":
            units_to_destroy.append(self.defending_melee_unit)

            min_power_attacker = min(unit.power for unit in self.attacking_units)
            min_power_units = [
                unit for unit in self.attacking_unit if unit.power == min_power_attacker
            ]
            least_powerful_attacker = random.choice(min_power_units)
            units_to_destroy.append(least_powerful_attacker)

        ##### Application of results

        # If applicable, force retreats for units that need to retreat : call unit.try_to_retreat
        for ur in units_that_must_retreat:
            # putative_retreat_order = get the correponding retreat in pending_orders, keeping only first order if multiple
            # NOTE we don't try each retreat order given. We try the first, and if it does not work we pick a random hex. So give only
            # one putative retreat per unit !
            putative_retreat_hex = None
            for order in putative_retreats:
                if order.unit_id == ur.id:
                    putative_retreat_hex = order.hexagon_ref
                    break
            ur.try_to_retreat(putative_retreat_hex)

        # Force destructions of units if applicable
        for ud in units_to_destroy:
            ud.destroy_self()
