class Map:
    """
    Contains the entire gamestate
    """

    def __init__(self, yaml_file=None) -> None:
        self.hexgrid = HexGrid(6, 6)


class Hexagon:
    def __init__(self, q: int, r: int) -> None:
        # q and r are the hex coordinates
        self.q = q
        self.r = r


class HexGrid:
    def __init__(self, max_q, max_r) -> None:
        self.hexagons = {}
        for q in range(max_q):
            for r in range(max_r):
                self.hexagons[(q, r)] = Hexagon(q, r)
