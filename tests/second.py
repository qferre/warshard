import warshard
from warshard.game import Game
from warshard.map import Map, HexGrid
from warshard.units import Unit
from warshard.actions import Order


# Recreate a game and place units for that
g = Game()  # TODO set headless to True to run tests once on pytest

g.players = ["germany", "usa"]

g.map.force_spawn_unit_at_position(
    unit_type="armor", hex_q=2, hex_r=3, player_side="germany", id=1
)


g.map.force_spawn_unit_at_position(
    unit_type="mechanised", hex_q=2, hex_r=4, player_side="usa", id=2
)


# Now test individual turn functions

# TODO : in the turn functions, check player side ! Make sure that only the active player can send movement orders (should already be ok thanks to the mobility points)
# but also need to check that only active player can send attack orders and advance orders, and only the inactive player can send defend orders


g.switch_active_player()
assert g.current_active_player_id == 1
assert g.current_active_player == "usa"


g.first_upkeep_phase()
assert g.map.all_units[1].mobility_remaining == 0
assert g.map.all_units[2].mobility_remaining > 0

raise NotImplementedError


# TODO remember to add invalid orders and test that they are not executed
pending_orders_attacker_movement = [Order(unit_id=26, hex_x=5, hex_y=5, map=g.map), Order()]
g.movement_phase(pending_orders_attacker_movement)


g.update_supply()

pending_orders_attacker_combat = []
g.attacker_combat_allocation_phase(pending_orders_attacker_combat)

pending_orders_defender_combat = []
g.defender_combat_allocation_phase(pending_orders_defender_combat)

putative_retreats_both_sides = [Order(..., type="putative")]
g.resolve_fights(putative_retreats_both_sides)

putative_advance_orders_both_sides = []
g.advancing_phase(putative_advance_orders_both_sides)


g.second_upkeep_phase()
