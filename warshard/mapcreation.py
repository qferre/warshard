import yaml

from warshard.game import Game
from warshard.map import Map


def read_status_from_yaml(yaml_path, game_to_update: Game):
    raise NotImplementedError
    yaml_file_as_dictionary = yaml.load(open(yaml_path))

    new_map = Map()

    """
    DO STUFF
    """

    game_to_update.map = new_map

    # Takes as input a Game object, and will create a new Map and replace the Game's Map with this new Map

    # the yaml contains min and max hex coordinates, the coordinates of hexes with defender bonuses or roads, the list of units at startup, and hexes which will receive reinforcements and at which turns, and which count for victory points
    # then use functions such as spawn_unit, and change hexagon characterisitcs (create empty hexagons first then modify them) to match the scenario
