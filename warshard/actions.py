# Format : FIGHT_RESULT_TABLE[rounded attacker_power_total/defender_strength_total][dice_roll]
FIGHT_RESULT_TABLE = table = {
    0.5: {1: "dr", 2: "S", 3: "ar", 4: "ar", 5: "ar", 6: "AE"},
    1: {1: "dr", 2: "dr", 3: "S", 4: "ar", 5: "ar", 6: "ar"},
    2: {1: "dr", 2: "dr", 3: "dr", 4: "dr", 5: "ar", 6: "ar"},
    3: {1: "DE", 2: "dr", 3: "dr", 4: "dr", 5: "dr", 6: "EX"},
    4: {1: "DE", 2: "dr", 3: "dr", 4: "dr", 5: "EX", 6: "EX"},
    5: {1: "DE", 2: "DE", 3: "dr", 4: "dr", 5: "EX", 6: "EX"},
    6: {1: "DE", 2: "DE", 3: "DE", 4: "dr", 5: "dr", 6: "EX"},
}


class Fight:
    raise NotImplementedError
