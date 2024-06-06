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
            encoding="utf-8", level=logging.DEBUG,
            handlers=[
            logging.FileHandler(log_file_path),
            logging.StreamHandler()
        ]
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
        self.logger.debug("This message should go to the log file")
        self.logger.info("So should this")
        self.logger.warning("And this, too")
        self.logger.error("This too.")


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
        pass
        self.display_thread.join()
