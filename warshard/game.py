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
        self.map = Map(yaml_file=yaml_file_path)
        self.current_active_player = 0
        self.current_turn_phase = None
        self.current_turn_number

        # Display
        if not headless:
            logging.debug("Starting display thread")
            self.display_thread = threading.Thread(
                target=partial(display.Displayer.draw, gamestate_to_draw=self)
            )
            self.display_thread.start()

    def run_a_turn(self, pending_orders):
        """_summary_

        Args:
            pending_orders (_type_): allows my framework to be easily used with AI ! a list containing pairs of (Unit, Hexagon). When requesting orders, we first check if any pending orders are present and try to execute those first. Orders are executed in FIFO, meaning you can queue movement orders for the same unit.
	        note that we will iterate over pending_orders multiple times : first for the movement, then for the attacker combat, then for the defender allocation (the idea being that defender can pre-allocate support by order of priority, we simply skip an allocation if it is not necessary meaning no fight takes place here), etc.

        Raises:
            NotImplementedError: _description_
        """
        raise NotImplementedError
    
        # TODO REMEMBER TO PRINT LOG OF ALL OF THIS (noting every order, every dice roll, etc., AND HAVE A logger OBJECT TO OUTPUT ALL INTO A TEXT FILE)

        # by default, always send the same pending_orders and ignore all non applicable
        # orders when processing

        # TODO check that self.current_turn_number < scenario_max_turns

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
        # Iterate over each unit : for each, check in pending orders to a nearby hex from user (which can be the same hex as current to make them “stay” even though it's useless) until MP are exhausted 
        for order in orders:
            order.unit_ref.attempt_move_to(order.hexagon_ref)
        # TODO Any stacked units are destroyed starting with the last arrived ones

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
        # TODO if no explicit order was given in pending_orders, retreat hexes are chosen at random if multiple are applicable

    """ TODO
    
    def first_upkeep_phase():
        Refresh mobility for all units OF THE CURRENT PLAYER

    def advancing_phase()
        # We ask player to pre-specify potential advances
        Iterate over each fight won and let attacker pick one unit to move there.
		if no explicit orders were given : if the attacker won, the attacker unit with strongest defensive power will be moved there and ties are broken at random. If the defender won, defending units don't budge without explicit orders

    def second_upkeep_phase()
        Then destroy all Fights and set mobility of all units to 0


    """





class Order:
    # TODO use in pending_orders, as an automatic casting of what is entered (allow the user to enter orders
    # as (unit_hex, hex_x, hex_y) where each is a string

    def __init__(unit_id, hex_coordinates, map):
        self.map = map
        self.unit_id = unit_id
        self.hex_x, self.hex_y = hex_coordinates

        # Find unit with same ID
        self.unit_ref = map.fetch_unit_by_id(self.unit_id)

        # Find hexagon with same coordinates
        self.hexagon_ref = map.fetch_hex_by_coordinate(self.hex_x, self.hex_y)
