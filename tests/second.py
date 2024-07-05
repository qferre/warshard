import warshard
from warshard.game import Game
from warshard.map import Map, HexGrid
from warshard.units import Unit
from warshard.actions import Order


# TODO recreate a game and place units for that
g = Game()  # TODO set headless to True to run tests once on pytest


g.map.force_spawn_unit_at_position(
    unit_type="armor", hex_q=2, hex_r=3, player_side="germany", id=16
)



g.map.force_spawn_unit_at_position(
    unit_type="mechanised", hex_q=2, hex_r=4, player_side="usa", id=26
)


# Now test individual turn functions

# TODO : in the turn functions, check player side ! Make sure that only the active player can send movement orders (should already be ok thanks to the mobility points)
# but also need to check that only active player can send attack orders and advance orders, and only the inactive player can send defend orders

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
