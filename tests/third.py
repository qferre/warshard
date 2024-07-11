# Now test YAML reading

import warshard
from warshard.game import Game
from warshard.map import Map, HexGrid
from warshard.units import Unit
from warshard.actions import Order
from warshard.mapcreation import read_status_from_yaml



yaml_path = "C:/Users/Quentin/Documents/Git/warshard/scenarios/boot_camp.yaml" # TODO "../scenarios/boot_camp.yaml"

new_game = read_status_from_yaml(yaml_path = yaml_path, headless=False)