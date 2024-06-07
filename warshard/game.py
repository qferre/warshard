import threading
import time
from functools import partial
import logging


from warshard import display
from warshard.map import Map
from warshard.units import Unit


class Game:

    global self  # I think it's necessary so the gamestate can be passed to the display thread

    def __init__(
        self,
        yaml_file_path: str = "",
        log_file_path: str = "example.log",
        headless=False,
    ) -> None:

        # Logging
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(
            encoding="utf-8",
            level=logging.DEBUG,
            handlers=[logging.FileHandler(log_file_path), logging.StreamHandler()],
        )

        # Also log to terminal
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        self.logger.addHandler(console_handler)

        # The gamestate/map for this game
        self.map = Map()

        # Display
        if not headless:
            logging.debug("Starting display thread")
            self.display_thread = threading.Thread(
                target=partial(display.Displayer.draw, gamestate_to_draw=self)
            )
            self.display_thread.start()

    def run_a_turn(self, pending_orders):
        raise NotImplementedError

        # by default, always send the same pending_orders and ignore all non applicable
        # orders when processing

        self.switch_active_player(new_player_id)
        self.first_upkeep_phase()
        self.movement_phase(pending_orders_attacker_movement)
        self.attacker_combat_allocation_phase(pending_orders_attacker_combat)
        self.defender_combat_allocation_phase(pending_orders_defender_combat)
        self.resolve_fights(putative_retreats_both_sides)
        self.advancing_phase(putative_advance_orders_both_sides)
        self.second_upkeep_phase()

    def __del__(self):
        # Does this do anything currently ? I'm not sure it really works.
        self.display_thread.join()

    #############################

    def switch_active_player(self, new_player_id):
        self.logger.debug("This message should go to the log file")
        self.logger.info("So should this")
        self.logger.warning("And this, too")
        self.logger.error("This too.")
        pass

    def movement_phase(orders):
        for order in orders:
            order.unit_ref.attempt_move_to(order.hexagon_ref)

    def attacker_combat_allocation_phase(orders):
        for order in orders:
            order.unit_ref.attempt_attack_on_hex(order.hexagon_ref)

    def defender_combat_allocation_phase(orders):
        for order in orders:
            order.unit_ref.attempt_join_defense_on_hex(order.hexagon_ref)

    def resolve_fights(putative_retreats):
        # Note : here, we ask the player to pre-specify retreats that would happen
        # if they lost
        for fight in self.all_fights:
            fight.resolve(putative_retreats)



class Order:

    def __init__(unit_id, hex_coordinates, map):
        self.map = map
        self.unit_id = unit_id
        self.hex_x, self.hex_y = hex_coordinates

        # Find unit with same ID
        self.unit_ref = self.map.all_units[self.unit_id]

        # Find hexagon with same coordinates
        self.hexagon_ref = self.map.hexgrid.hexagons[(self.hex_x, self.hex_y)]
