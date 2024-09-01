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
g.map.force_spawn_unit_at_position(
    unit_type="infantry", hex_q=3, hex_r=4, player_side="germany", id=3
)
g.map.force_spawn_unit_at_position(
    unit_type="artillery", hex_q=3, hex_r=2, player_side="germany", id=4
)
g.map.force_spawn_unit_at_position(
    unit_type="artillery", hex_q=5, hex_r=6, player_side="usa", id=5
)


# Same order as in the "second" unit test
# NOTE they will be executed in order if all goes well !
all_orders = [
    # Attacker combat -> trying to put them first, they should be ignored during the movement phase
    # but then executed in the combat phase, even though they are first and movement comes first
    # NOTE write this in documentation : this means you can add to the list a movement order for unit 1, then a combat order for unit 1, AND THEN a movement order for unit 2, and it will still work
    Order(
        unit_id=2, hex_x=4, hex_y=4, map=g.map
    ),  # invalid order, should not be executed
    Order(unit_id=2, hex_x=3, hex_y=4, map=g.map),
    Order(unit_id=5, hex_x=3, hex_y=4, map=g.map),
    # Attacker movement
    Order(unit_id=1, hex_x=3, hex_y=2, map=g.map),
    Order(unit_id=2, hex_x=3, hex_y=4, map=g.map),
    Order(unit_id=2, hex_x=4, hex_y=5, map=g.map),
    Order(unit_id=2, hex_x=4, hex_y=7, map=g.map),
    # Defender combat support
    Order(unit_id=5, hex_x=3, hex_y=4, map=g.map),
    # Retreats and advances
    Order(
        unit_id=3, hex_x=2, hex_y=4, map=g.map, order_type="putative"
    ),  # This Order will not be executed
    Order(unit_id=2, hex_x=5, hex_y=5, map=g.map, order_type="putative"),
    Order(unit_id=2, hex_x=3, hex_y=4, map=g.map, order_type="putative"),
    Order(unit_id=2, hex_x=4, hex_y=4, map=g.map, order_type="putative"),
]

"""TODO BUG : the attacking US mechanised division managed to engage in combat even though it was not adjacent ??
Ah no okay, it's because it advanced backwards after the fight because the putative retreat was interpreted as a putative advance. 
TODO I likely need to differentiate putative retreats from putative advances to prevent this !!
Alternatively, just explain this should be handled by the priority system, meaning the advance orders should be ahead in the list of orders if they are more desirable. Indeed, one may wish to reorganise and withdraw even if they win an attack : just needs to be higher priority.
"""


# Run a full turn
g.run_a_turn(this_turn_orders=all_orders)


### Try running a second turn, this time it's Germany's turn and not the USA


all_orders_2 = [
    Order(unit_id=1, hex_x=3, hex_y=4, map=g.map),
    Order(unit_id=1, hex_x=4, hex_y=4, map=g.map),
    Order(unit_id=1, hex_x=5, hex_y=4, map=g.map),
    Order(unit_id=1, hex_x=5, hex_y=5, map=g.map),
    Order(unit_id=4, hex_x=5, hex_y=5, map=g.map),
    Order(unit_id=3, hex_x=2, hex_y=5, map=g.map),
]

g.run_a_turn(this_turn_orders=all_orders_2)
