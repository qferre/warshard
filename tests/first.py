
"""TODO Dispatch this into individual test files, add asserts (not necessarily use pytest at first, but I do need asserts)
"""

import warshard
from warshard.game import Game
from warshard.map import Map, HexGrid
from warshard.units import Unit


g = Game()


# Ensure map can be updated
g.map.all_units[666] = Unit(
    hexagon_position=g.map.hexgrid.hexagons[(2, 2)],
    type="armor",
    player_side="germany",
    id=666,
)


g.map.all_units[42] = Unit(
    hexagon_position=g.map.hexgrid.hexagons[(0, 0)],
    type="infantry",
    player_side="germany",
    id=42,
)


g.map.all_units[26] = Unit(
    hexagon_position=g.map.hexgrid.hexagons[(2, 4)],
    type="mechanised",
    player_side="usa",
    id=26,
)





# Now test interactions like movements and fights

g.map.fetch_unit_by_id(26).force_move_to(g.map.fetch_hex_by_coordinate(4,5))


g.map.fetch_unit_by_id(666).force_move_to(g.map.fetch_hex_by_coordinate(3,3))

## Try to move units we created

## Create units close enough for a fight and test it


# Now test individual turn functions
"""
g.switch_active_player(new_player_id)
g.first_upkeep_phase()
g.movement_phase(pending_orders_attacker_movement)
g.attacker_combat_allocation_phase(pending_orders_attacker_combat)
g.defender_combat_allocation_phase(pending_orders_defender_combat)
g.resolve_fights(putative_retreats_both_sides)
g.advancing_phase(putative_advance_orders_both_sides)
g.second_upkeep_phase()
"""







# Now test YAML reading


# Now test run_a_turn