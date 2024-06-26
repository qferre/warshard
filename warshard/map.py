import numpy as np

# from __future__ import annotations
# from warshard.units import Unit
from warshard.config import Config


class Map:
    """
    Contains all elements on the board (not quite the same thing as the gamestate) :
    contains self.hexgrid and self.all_units
    """

    def __init__(self, yaml_file=None, max_q=21, max_r=15) -> None:
        assert max_q <= 21
        assert max_r <= 15
        self.hexgrid = HexGrid(max_q, max_r, parent_map=self)

        # self.all_units: dict<int : Unit> = {} # List of all Units currently in play
        # TODO fix typing circular imports
        self.all_units = {}  # a dictionary {unit_id: unit} containing all units in play
        # TODO do not work on self.all_units directly, make functions that add unit by force-checking their ID (see right below)

        # self.ongoing_fights : dictionary<Hexagon : Fight>
        self.ongoing_fights = {}  # dictionary {Hexagon: Fight}

    # TODO use this in the code when relevant, several funtions will necessitate it to replace the dirty workarounds I
    # have coded so far (involving directly looking into the dict, which is ugly)
    def fetch_unit_by_id(self, unit_id):
        """
        Returns a reference to the Unit object with this ID.

        Args:
            unit_id (_type_): _description_

        Returns:
            _type_: _description_
        """
        return self.all_units[unit_id]

    def fetch_hex_by_coordinate(self, x, y):
        """

        Returns a reference to the Hexagon object with this ID.

        Args:
            x (_type_): _description_
            y (_type_): _description_

        Returns:
            _type_: _description_
        """

        return self.hexgrid.hexagons[(x, y)]

    """ TODO
    def force_spawn_unit_at_position(unit_type: str, hex_x:int, hex_y:int, player_side, unit_id)
		remember to check id is not already allocated
        return a reference to the unit
        this does NOT check for stacking

	def force_destruction(unit_id:int)
        use this whenever a unit needs to be destroyed, usually as a consequence of a fight or improper stacking
        also usable in debug, like all "force" functions (need to write this in doc somewhere, that all "force" functions can be used in debug)


    def read_status_from_yaml()
        the yaml contains min and max hex coordinates, the coordinates of hexes with defender bonuses or roads, the list of units at startup, and hexes which will receive reinforcements and at which turns, and which count for victory points
        then use functions such as spawn_unit, and change hexagon characterisitcs (create empty hexagons first then modify them) to match the scenario
    """


class Hexagon:
    def __init__(
        self,
        parent_map: Map,
        q: int,
        r: int,
        type: str = "plains",
        victory_points: int = 0,
        name: str = "",
    ) -> None:
        """_summary_

        Args:
            parent_map
            q (int): _description_
            r (int): _description_
            type (str, optional): _description_. Defaults to "plains".
            victory_points (int, optional): _description_. Defaults to 0.
            name (str, optional): _description_. Defaults to "".
        """

        self.parent_map = parent_map

        # q and r are the hex coordinates
        self.q = q
        self.r = r

        assert type in Config.MOBILITY_COSTS.keys()
        self.type = type

        self.victory_points = victory_points

        self.defender_multiplier = Config.DEFENDER_MULTIPLIER[self.type]
        self.mobility_cost_multiplier = Config.MOBILITY_COSTS[self.type]

        """
        self.controller = whoever last had a unit there
        self.name = name # specified in YAML, something like "Marseille", "Bastogne", etc. ; for display purposes only
        """

        # x and y, are another set of coordinates
        # used to ensure the final hex grid looks
        # more like a rectangle
        # x is the same as q, but y is r shift by one every two columns so the final grid looks square-like
        # TODO in the yaml, decide which to use !
        self.x = self.q
        self.y = self.r - self.q // 2

    def is_accessible_to_player_side(self, player_side):
        # check if the hex contains any unit, or if its or its neighbors contains any unit NOT belonging to the specified side ; return separate flags for that since we may want to check those conditions separately later
        neighbors = self.get_neighbors()

        # Default assumption is that we can move there
        hex_is_clear, hex_not_in_enemy_zoc, hex_is_not_clear_but_friendly_occupied = (
            True,
            True,
            False,
        )

        # If it costs infinity to move there, mark inaccessible
        if Config.MOBILITY_COSTS[self.type] == np.inf:
            hex_is_clear = False

        for unit_id, unit in self.parent_map.all_units.items():
            if (
                unit.hexagon_position == self
            ):  # TODO check equality works between hexagons
                hex_is_clear = False
                if unit.player_side == player_side:
                    hex_is_not_clear_but_friendly_occupied = True
                    # TODO this does not consider alliances

            if unit.hexagon_position in neighbors and unit.player_side != player_side:
                hex_not_in_enemy_zoc = False

        return (
            hex_is_clear,
            hex_not_in_enemy_zoc,
            hex_is_not_clear_but_friendly_occupied,
        )

        # TODO also check if the hex is not inherently impassable (mobility cost of np.inf)

    def get_neighbors(self):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, -1), (-1, 1)]
        coords = [
            (self.q + dq, self.r + dr)
            for dq, dr in directions
            if (self.q + dq, self.r + dr) in self.parent_map.hexgrid.hexagons
        ]
        return [self.parent_map.fetch_hex_by_coordinate(*coord) for coord in coords]
        # TODO change this code to cap to min and max q and r to avoid going offmap (I think it already does with the "in" check)
        # WARNING : use qr, or xy system ?? BE CAREFUL NOT TO MIX THE TWO !!


class HexGrid:
    def __init__(self, max_q, max_r, parent_map) -> None:
        self.hexagons = {}
        self.parent_map = parent_map
        for q in range(max_q):
            for r in range(max_r):
                self.hexagons[(q, r)] = Hexagon(parent_map=self.parent_map, q=q, r=r)

    @staticmethod
    def manhattan_distance_hex_grid(h1: Hexagon, h2: Hexagon):

        # TODO qr or xy coords ? XY I think as is currently done is the correct way
        # TODO Add a test for this in tests !

        x1, y1, x2, y2 = h1.x, h1.y, h2.x, h2.y

        x_distance = abs(x1 - x2)
        y_distance = abs(y1 - y2)
        diagonal_steps = min(x_distance, y_distance)

        remaining_x_distance = x_distance - diagonal_steps
        remaining_y_distance = y_distance - diagonal_steps

        if remaining_x_distance > 0:
            return (remaining_x_distance // 2) + diagonal_steps
        else:
            return remaining_y_distance + diagonal_steps


""" TODO
    def get_total_victory_points_per_players:
        iterate over all my hexes. If a hex has a victory point value, give it to its controller. Return the total.


	# Below : used to trace a route to HQ
	# Hexes containing an enemy or which have a neighbor containing an enemy are considered inaccessible (use the hex.is_accessible_to_player_side() function)
    # TODO to shorten the graph, cap it at a distance of 6 (tbd) since HQs cannot supply more than 6 hexes away
    # TODO This is likely too expensive to run each time for all units. Instead, I think that I can do this : 
    #   at the beginning of each turn, iterate over all hq and mark all its accessible neighbors. Then for each such neighbor, mark its own accessible neighbors and so on so forth up to 6 times. Remember all hexes thus explored and mark them as "in supply". 
	def build_graph(self):
    	G = nx.Graph()
    	for (q, r), hexagon in self.hexagons.items():
        	if not hexagon.accessible: continue
        	for neighbor in self.get_neighbors(q, r):
            	if self.is_accessible(*neighbor):
                	G.add_edge((q, r), neighbor, weight=1)  # Weight can be adjusted if needed
    	return G
    # TODO perhaps also use this to automatically try to deduce partial movement orders if a movement order is given for a hex that is not neighboring (yes probably do that it will facilitate future usage)


	def find_path(self, start, goal):
    	G = self.build_graph()
    	try:
        	path = nx.astar_path(G, start, goal, heuristic= lambda a,b: abs(a[0] - b[0]) + abs(a[1] - b[1]), weight='weight')
        	return path
    	except nx.NetworkXNoPath:
        	return None
	"""
