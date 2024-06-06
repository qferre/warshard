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
            filename=log_file_path, encoding="utf-8", level=logging.DEBUG
        )

        # The gamestate/map for this game
        self.map = Map()

        self.all_units: list[Unit] = []  # List of all Units currently in play

        # Display
        if not headless:
            logging.debug("Starting display thread")
            self.display_thread = threading.Thread(
                target=partial(display.Displayer.draw, map_to_draw=self.map)
            )
            self.display_thread.start()

    def run_a_turn(self, pending_orders):
        raise NotImplementedError
        self.logger.debug("This message should go to the log file")
        self.logger.info("So should this")
        self.logger.warning("And this, too")
        self.logger.error("This too.")

        self.switch_active_player()
        self.first_upkeep_phase()
        self.movement_phase(pending_orders)

    def __del__(self):
        pass
        self.display_thread.join()
