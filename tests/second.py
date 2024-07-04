

import warshard
from warshard.game import Game
from warshard.map import Map, HexGrid
from warshard.units import Unit
from warshard.actions import Order


# TODO recreate a game and place units for that
g = Game()  # TODO set headless to True to run tests once on pytest

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


# Now test individual turn functions
"""


g.switch_active_player(new_player_id)

g.first_upkeep_phase()

pending_orders_attacker_movement = [Order(), Order()]
g.movement_phase(pending_orders_attacker_movement)

g.update_supply()

pending_orders_attacker_combat = []
g.attacker_combat_allocation_phase(pending_orders_attacker_combat)

pending_orders_defender_combat = []
g.defender_combat_allocation_phase(pending_orders_defender_combat)

putative_retreats_both_sides = []
g.resolve_fights(putative_retreats_both_sides)

putative_advance_orders_both_sides = []
g.advancing_phase(putative_advance_orders_both_sides)


g.second_upkeep_phase()
"""