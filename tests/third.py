from warshard.mapcreation import read_status_from_yaml

# Test YAML reading
# NOTE Here, we intentionally leave headless to False to also test drawing and rendering
yaml_path = "../scenarios/boot_camp.yaml"
new_game = read_status_from_yaml(yaml_path=yaml_path, headless=False)

# Ensure we can kill game and display
new_game.stop()
