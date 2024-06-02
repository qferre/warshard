from warshard.map import Map
import threading
import time


class Game:

    global self

    def display_func(self):
        while True:
            print(self.map)
            time.sleep(1)

    def __init__(
        self, yaml_file_path: str = "", log_file_path: str = "", headless=False
    ) -> None:

        pass

        # The gamestate/map for this game
        self.map = Map()

        if not headless:
            self.display_thread = threading.Thread(target=self.display_func)
            self.display_thread.start()

    def run_a_turn(pending_orders):
        pass

    def __del__(self):
        pass
        self.display_thread.join()
