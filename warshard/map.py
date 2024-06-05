class Map:
    """
    Contains the entire gamestate
    """

    def __init__(self, yaml_file=None, max_q=21, max_r=15) -> None:
        self.hexgrid = HexGrid(max_q, max_r)


class Hexagon:
    def __init__(self, q: int, r: int) -> None:
        # q and r are the hex coordinates
        self.q = q
        self.r = r

        # x and y, are another set of coordinates
        # used to ensure the final hex grid looks
        # more like a rectangle
        # x is the same as q, but y is r shift by one every two columns so the final grid looks square-like
        # TODO in the yaml, decide which to use !
        self.x = self.q
        self.y = self.r - self.q // 2


class HexGrid:
    def __init__(self, max_q, max_r) -> None:
        self.hexagons = {}
        for q in range(max_q):
            for r in range(max_r):
                #rtrue = (
                #    r - q // 2
                #) 
                self.hexagons[(q, r)] = Hexagon(q, r)
