"""TODO Dispatch this into individual test files, add asserts (not necessarily use pytest at first, but I do need asserts)
"""

import warshard
from warshard.game import Game
from warshard.map import Map, HexGrid
from warshard.units import Unit
from warshard.actions import Order


g = Game() # TODO set headless to True to run tests once on pytest


# Ensure map can be updated
g.map.all_units[16] = Unit(
    hexagon_position=g.map.hexgrid.hexagons[(2, 2)],
    type="armor",
    player_side="germany",
    id=16,
    parent_map=g.map,
)


g.map.all_units[42] = Unit(
    hexagon_position=g.map.hexgrid.hexagons[(0, 0)],
    type="infantry",
    player_side="germany",
    id=42,
    parent_map=g.map,
)


g.map.all_units[26] = Unit(
    hexagon_position=g.map.hexgrid.hexagons[(2, 4)],
    type="mechanised",
    player_side="usa",
    id=26,
    parent_map=g.map,
)


g.map.fetch_hex_by_coordinate(3, 3).victory_points = 10
g.map.fetch_hex_by_coordinate(3, 3).controller = "germany"
g.map.fetch_hex_by_coordinate(4, 3).controller = "germany"

g.map.fetch_hex_by_coordinate(4, 7).victory_points = 10
g.map.fetch_hex_by_coordinate(4, 7).controller = "usa"

g.map.fetch_hex_by_coordinate(8, 8).victory_points = 10
g.map.fetch_hex_by_coordinate(8, 8).controller = "britain"

g.map.fetch_hex_by_coordinate(9, 9).victory_points = 10
g.map.fetch_hex_by_coordinate(9, 9).controller = "ussr"


g.map.fetch_hex_by_coordinate(16, 1).type = "city"
g.map.fetch_hex_by_coordinate(16, 2).type = "forest"
g.map.fetch_hex_by_coordinate(16, 3).type = "road"
g.map.fetch_hex_by_coordinate(16, 4).type = "impassable"
g.map.fetch_hex_by_coordinate(16, 5).type = "defensible"
g.map.fetch_hex_by_coordinate(16, 6).type = "dry_plains"
g.map.fetch_hex_by_coordinate(16, 7).type = "elevation"
g.map.fetch_hex_by_coordinate(16, 8).type = "snow_plains"
g.map.fetch_hex_by_coordinate(16, 9).type = "water"


g.map.fetch_hex_by_coordinate(3, 3).type = "city"
g.map.fetch_hex_by_coordinate(4, 5).type = "forest"


# Now test interactions like movements and fights

g.map.fetch_unit_by_id(26).force_move_to(g.map.fetch_hex_by_coordinate(4, 5))
g.map.fetch_unit_by_id(16).force_move_to(g.map.fetch_hex_by_coordinate(3, 3))

ur = g.map.fetch_unit_by_id(42)
r_hex = g.map.fetch_hex_by_coordinate(1, 0)
ur.try_to_retreat(r_hex)
assert ur.hexagon_position == r_hex

## Try to move units we created
u_1 = g.map.fetch_unit_by_id(16)
u_1.mobility_remaining = 1000
u_1.attempt_move_to(g.map.fetch_hex_by_coordinate(3, 4))  # assert Should succeed
u_1.attempt_move_to(
    g.map.fetch_hex_by_coordinate(4, 5)
)  # assert Should fail due to being occupied
u_1.attempt_move_to(
    g.map.fetch_hex_by_coordinate(12, 0)
)  # assert Should fail due to being too far


# Test supply system
r = g.map.fetch_hex_by_coordinate(4, 5).recursively_get_distances_continuous_path(
    # player_side="germany", # TODO test this so far this seems to be failing and returning all hexes
    max_rank=3
)

g.map.all_units[99] = Unit(
    hexagon_position=g.map.hexgrid.hexagons[(2, 5)],
    type="hq",
    player_side="germany",
    id=67,
    parent_map=g.map,
)

print(r)
for k, v in r.items():
    print(k)
    print([str(vv) for vv in v])
    # TODO assert something

g.update_supply()
# TODO assert something
print(g.map.hexes_currently_in_supply_per_player)


## Create units close enough for a fight and test it
g.map.all_units[67] = Unit(
    hexagon_position=g.map.hexgrid.hexagons[(4, 4)],
    type="armor",
    player_side="germany",
    id=67,
    parent_map=g.map,
)

g.map.all_units[27] = Unit(
    hexagon_position=g.map.hexgrid.hexagons[(4, 7)],
    type="artillery",
    player_side="usa",
    id=27,
    parent_map=g.map,
)
u_2 = g.map.fetch_unit_by_id(67)
fight_hex = g.map.fetch_hex_by_coordinate(4, 5)
u_1.attempt_attack_on_hex(fight_hex)
u_2.attempt_attack_on_hex(fight_hex)

## assert the fight was created with the proper units
this_fight = g.map.ongoing_fights[fight_hex]
assert this_fight.attacking_units == [u_1, u_2]
assert this_fight.defending_melee_unit == g.map.fetch_unit_by_id(26)


u_3 = g.map.fetch_unit_by_id(27)
u_3.attempt_join_defence_on_hex(g.map.fetch_hex_by_coordinate(4, 5))
assert this_fight.defending_support_units == [u_3]

# attempt to resolve this fight, force the dice roll to a certain value to ensure we are properly testing retreats also
putative_retreats = [Order(unit_id=26, hex_x=5, hex_y=5, map=g.map)]
this_fight.resolve(putative_retreats, debug_force_dice_roll_to=1)
# TODO when the debug_force_dice_roll_to was set to 6, I saw weird attacker retreats ? To double check


# TODO Make more Fights so we can test all possible Fight outcomes


"""
TODO : for all functions that take an hex, make it so if a tuple of coordinates is passed
we try to fetch the hex automatically, this will let us shorten the syntax
    from u_3.attempt_join_defence_on_hex(g.map.fetch_hex_by_coordinate(4, 5))
    to u_3.attempt_join_defence_on_hex((4, 5))
"""


# Now test individual turn functions
"""
g.switch_active_player(new_player_id)
g.first_upkeep_phase()
g.movement_phase(pending_orders_attacker_movement)
g.update_supply()
g.attacker_combat_allocation_phase(pending_orders_attacker_combat)
g.defender_combat_allocation_phase(pending_orders_defender_combat)
g.resolve_fights(putative_retreats_both_sides)
g.advancing_phase(putative_advance_orders_both_sides)
g.second_upkeep_phase()
"""


# Now test the complete run_a_turn


# Now test YAML reading
