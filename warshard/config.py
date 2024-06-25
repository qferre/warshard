import numpy as np


class Config:

    # Power, Defence, Mobility, Range
    UNIT_CHARACTERISTICS = {
        "infantry": (1, 2, 1, 1),
        "mechanised": (3, 3, 4, 1),
        "armor": (6, 3, 6, 1),
        "artillery": (3, 0, 2, 3),
        "air_wing": (2, 0, 9, 9),
        "hq": (0, 0, 2, 0),
    }

    # Which units are considered melee units ?
    MELEE_UNITS = ["infantry", "mechanised", "armor"]

    DICE_VALUES = [1, 2, 3, 4, 5, 6]
    # Format : FIGHT_RESULT_TABLE[rounded attacker_power_total/defender_strength_total][dice_roll]
    FIGHT_RESULT_TABLE = {
        0.5: {1: "dr", 2: "S", 3: "ar", 4: "ar", 5: "ar", 6: "AE"},
        1: {1: "dr", 2: "dr", 3: "S", 4: "ar", 5: "ar", 6: "ar"},
        2: {1: "dr", 2: "dr", 3: "dr", 4: "dr", 5: "ar", 6: "ar"},
        3: {1: "DE", 2: "dr", 3: "dr", 4: "dr", 5: "dr", 6: "EX"},
        4: {1: "DE", 2: "dr", 3: "dr", 4: "dr", 5: "EX", 6: "EX"},
        5: {1: "DE", 2: "DE", 3: "dr", 4: "dr", 5: "EX", 6: "EX"},
        6: {1: "DE", 2: "DE", 3: "DE", 4: "dr", 5: "dr", 6: "EX"},
    }

    # NOTE defensible == trench ; and elevation == hills
    MOBILITY_COSTS = {
        "plains": 1,
        "dry_plains": 1,
        "snow_plains": 1,
        "city": 2,
        "defensible": 2,
        "forest": 2,
        "elevation": 2,
        "road": 0.5,
        "water": np.inf,
        "impassable": np.inf,
    }

    DEFENDER_MULTIPLIER = {
        "plains": 1,
        "dry_plains": 1,
        "snow_plains": 1,
        "city": 2,
        "defensible": 2,
        "forest": 2,
        "elevation": 2,
        "road": 1,
        "water": 1,
        "impassable": 5,
    }


class DisplayConfig:

    WIDTH, HEIGHT = 1400, 980
    FPS = 5
    HEX_SIZE = 36
    FONT_SIZE_HEX = 14
    FONT_SIZE = 16
    FONT_SIZE_INFO = 20
    BACKGROUND_COLOR = (255, 255, 255)
    HEX_BORDER_COLOR = (0, 0, 0)
    TEXT_COLOR = (0, 0, 0)

    FACTION_COLORS = {
        "britain": (255, 204, 153, 255),  # beige
        "germany": (102, 204, 255, 255),  # pale teal
        "usa": (102, 204, 0, 255),  # green
        "ussr": (255, 153, 0, 255),  # deep orange
    }
