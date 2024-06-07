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