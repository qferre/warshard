import yaml

from warshard.game import Game
from warshard.map import Map


def read_status_from_yaml(yaml_path, game_to_update: Game):
    raise NotImplementedError

    yaml_path = "C:/Users/Quentin/Documents/Git/warshard/scenarios/boot_camp.yaml"

    with open(yaml_path, "r", encoding="utf-8") as file:
        yaml_file_as_dictionary = yaml.safe_load(file)

    print(yaml_file_as_dictionary)
    yd = yaml_file_as_dictionary  # Shorthand

    # TODO if I update an existing game, remember to erase all prior info. Or more simply, make it
    # that this function creates a new Game and returns it

    """
    DO STUFF
    """
    game_to_update.players = yd.players
    game_to_update.current_turn_number = 0
    game_to_update.current_turn_phase = "TBD"  # TODO
    game_to_update.max_turns = yd.max_turns  # TODO

    game_to_update.map = Map(yd.map.max_q, yd.max.max_r)

    # Hexes
    for hex_type, hex_list_of_this_type in yd.special_hexes.items():
        for hex_definition in hex_list_of_this_type:
            hex_to_update = game_to_update.map.fetch_hex_by_coordinate(
                hex_definition.q, hex_definition.r
            )
            hex_to_update.type = hex_type
            hex_to_update.name = hex_definition.name

    # Unit
    for faction, list_of_units_for_this_faction in yd.units.items():
        for unit_definition in list_of_units_for_this_faction:
            game_to_update.force_spawn_unit_at_position(
                unit_type=i, hex_q=i, hex_r=i, player_side=i, id=i
            )

    # Record reinforcements # TODO

    # Takes as input a Game object, and will create a new Map and replace the Game's Map with this new Map

    # the yaml contains min and max hex coordinates, the coordinates of hexes with defender bonuses or roads, the list of units at startup, and hexes which will receive reinforcements and at which turns, and which count for victory points
    # then use functions such as spawn_unit, and change hexagon characterisitcs (create empty hexagons first then modify them) to match the scenario
