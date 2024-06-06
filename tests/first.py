import warshard


from warshard.game import Game
from warshard.map import Map, HexGrid
from warshard.units import Unit


g = Game()


# Ensure map can be updated
g.map.all_units.append(
    Unit(
        hexagon_position=g.map.hexgrid.hexagons[(2, 2)],
        type="armor",
        player_side="germany",
    )
)


g.map.all_units.append(
    Unit(
        hexagon_position=g.map.hexgrid.hexagons[(0, 0)],
        type="infantry",
        player_side="germany",
    )
)

# g.map = Map(max_q=5)