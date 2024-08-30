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


# ------------- Now test individual turn functions

# TODO : in the turn functions, check player side ! Make sure that only the active player can send movement orders (should already be ok thanks to the mobility points)
# but also need to check that only active player can send attack orders and advance orders, and only the inactive player can send defend orders

# Player switch
g.switch_active_player()
assert g.current_active_player_id == 1
assert g.current_active_player == "usa"

# First upkeep phase
g.first_upkeep_phase()
assert g.map.all_units[1].mobility_remaining == 0
assert g.map.all_units[2].mobility_remaining > 0

# Movement phase
# NOTE there are invalid orders in this list, we also assert that they are not executed!
pending_orders_attacker_movement = [
    Order(unit_id=1, hex_x=3, hex_y=2, map=g.map),
    Order(unit_id=2, hex_x=3, hex_y=4, map=g.map),
    Order(unit_id=2, hex_x=4, hex_y=5, map=g.map),
    Order(unit_id=2, hex_x=4, hex_y=7, map=g.map),
]
g.movement_phase(pending_orders_attacker_movement)

assert g.map.fetch_unit_by_id(1).hexagon_position == g.map.fetch_hex_by_coordinate(2, 3)
assert g.map.fetch_unit_by_id(2).hexagon_position == g.map.fetch_hex_by_coordinate(4, 5)


# Supply update (already tested elsewhere)
g.update_supply()


# Combat units preparation
g.map.force_spawn_unit_at_position(
    unit_type="infantry", hex_q=3, hex_r=4, player_side="germany", id=3
)
g.map.force_spawn_unit_at_position(
    unit_type="artillery", hex_q=3, hex_r=2, player_side="germany", id=4
)
g.map.force_spawn_unit_at_position(
    unit_type="artillery", hex_q=5, hex_r=6, player_side="usa", id=5
)


# Attacker combat allocation phase
# NOTE attack with melee and support
pending_orders_attacker_combat = [
    Order(
        unit_id=2, hex_x=4, hex_y=4, map=g.map
    ),  # invalid order, should not be executed
    Order(unit_id=2, hex_x=3, hex_y=4, map=g.map),
    Order(unit_id=5, hex_x=3, hex_y=4, map=g.map),
]
g.attacker_combat_allocation_phase(pending_orders_attacker_combat)


# Defender combat allocation phase
# NOTE assigning support
pending_orders_defender_combat = [
    Order(unit_id=5, hex_x=3, hex_y=4, map=g.map),
]
g.defender_combat_allocation_phase(pending_orders_defender_combat)


print(g.map.ongoing_fights)  # TODO assert the fight is correct


putative_retreats_both_sides = [
    Order(
        unit_id=3, hex_x=2, hex_y=4, map=g.map, order_type="putative"
    ),  # This Order will not be executed
    Order(unit_id=2, hex_x=5, hex_y=5, map=g.map, order_type="putative"),
]
g.resolve_fights(
    putative_retreats_both_sides, debug_force_rolls=[2]  # Force defender to retreat
)


putative_advance_orders_both_sides = [
    Order(unit_id=2, hex_x=3, hex_y=4, map=g.map, order_type="putative"),
    Order(
        unit_id=2, hex_x=4, hex_y=4, map=g.map, order_type="putative"
    ),  # This Order will not be executed
]
g.advancing_phase(putative_advance_orders_both_sides)


g.second_upkeep_phase()
