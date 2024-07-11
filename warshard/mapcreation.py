import yaml

from warshard.game import Game
from warshard.map import Map

from warshard.utils import dotdict


def read_status_from_yaml(
    yaml_path: str,
    log_file_path: str = "./example.log",
    headless=False,
):

    game_to_update = Game(log_file_path, headless)

    with open(yaml_path, "r", encoding="utf-8") as file:
        yaml_file_as_dictionary = yaml.safe_load(file)

    print(yaml_file_as_dictionary)

    # Shorthand and allow using point notation to access items
    yd = dotdict(yaml_file_as_dictionary)
    yd.map = dotdict(yd.map)
    yd.map.special_hexes = dotdict(yd.map.special_hexes)
    yd.units = dotdict(yd.units)

    """
    DO STUFF
    """
    game_to_update.players = yd.players
    game_to_update.current_turn_number = 0
    game_to_update.current_turn_phase = "TBD"  # TODO
    game_to_update.max_turns = yd.max_turns  # TODO

    game_to_update.map = Map(yd.map.max_q, yd.map.max_r)

    # TODO read the biome, and set the default plains to the appropriate color !

    # Hexes
    for hex_type, hex_list_of_this_type in yd.map.special_hexes.items():
        for hex_definition in hex_list_of_this_type:
            hex_definition = dotdict(hex_definition)
            hex_to_update = game_to_update.map.fetch_hex_by_coordinate(
                hex_definition.q, hex_definition.r
            )
            hex_to_update.type = hex_type
            hex_to_update.name = hex_definition.name

            if "victory_points" in hex_definition:
                hex_to_update.victory_points = hex_definition.victory_points
    # Unit
    for faction, list_of_units_for_this_faction in yd.units.items():
        for unit_definition in list_of_units_for_this_faction:
            unitdef = dotdict(unit_definition)
            print(f"{faction} - {unitdef}")
            game_to_update.map.force_spawn_unit_at_position(
                unit_type=unitdef.type,
                hex_q=unitdef.q,
                hex_r=unitdef.r,
                player_side=faction,
                id=unitdef.id,
            )  # TODO implement unit name reading (not just ID) from the YAML

    # Record reinforcements # TODO

    return game_to_update
