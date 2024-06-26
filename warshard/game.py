import threading
import time
from functools import partial
import logging


from warshard import display
from warshard.map import Map
from warshard.units import Unit
from warshard.actions import Order


class Game:

    global self  # Necessary so the Game object can be passed to the display thread

    def __init__(
        self,
        scenario_yaml_file_path: str = "",
        log_file_path: str = "./example.log",
        headless=False,
    ) -> None:

        # Logging
        log_format = "%(asctime)s - %(name)s:%(levelname)s -- %(message)s"
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(logging.Formatter(log_format))
        logging.basicConfig(
            encoding="utf-8",
            level=logging.DEBUG,
            handlers=[
                logging.FileHandler(log_file_path),
                console_handler,
            ],  # Also log to terminal
            format=log_format,
        )
        self.logger = logging.getLogger(__name__)

        # The gamestate/map for this game
        self.map = Map(yaml_file=scenario_yaml_file_path)
        self.current_active_player = 0
        self.current_turn_phase = None  # TODO Use this in asserts : checking the last phase which was run to ensure we cannot, for example, run attacker_combat_allocation_phase if movement_phase was not run before
        self.current_turn_number = 0

        # Display
        self.display_thread = None
        if not headless:
            logging.debug("Starting display thread")

            self.displayer = display.Displayer()

            self.display_thread = threading.Thread(
                target=partial(self.displayer.draw, gamestate_to_draw=self)
            )
            self.display_thread.start()

    def run_a_turn(self, pending_orders: list[Order]):
        """_summary_

        Args:
            pending_orders (_type_): allows my framework to be easily used with AI ! a list containing pairs of (Unit, Hexagon). When requesting orders, we first check if any pending orders are present and try to execute those first. Orders are executed in FIFO, meaning you can queue movement orders for the same unit.
                note that we will iterate over pending_orders multiple times : first for the movement, then for the attacker combat, then for the defender allocation (the idea being that defender can pre-allocate support by order of priority, we simply skip an allocation if it is not necessary meaning no fight takes place here), etc.
                TODO : add a way to flag the type of orders as they are given inside the pending_orders list. Relevant notably to pre-plan retreats : we don't want the unit to retreat during its movement phase because it thought it was a regular movement order. Also relevant for putative advances, to ensure they are not just seen as a regular attack order. Probably these two "putative" orders are the problematic ones, so the flag could simply be "order.is_putative_order". TBD.

        Raises:
            NotImplementedError: _description_
        """
        raise NotImplementedError

        # TODO remember all orders given, but write in doc that this does not necessarily let one redo the entire game since there are some dice rolls and random events. However if the random seed is fixed, it should be possible :)
        # self.all_orders_ever_given[self.current_turn_number] += pending_orders

        # TODO REMEMBER TO PRINT LOG OF ALL OF THIS (noting every order, every dice roll, etc., AND HAVE A logger OBJECT TO OUTPUT ALL INTO A TEXT FILE)
        # This will likely necessitate passing the logger object to all functions.

        # by default, always send the same pending_orders and ignore all non applicable
        # orders when processing

        # TODO remember to update self.current_turn_phase when necessary

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
        # TODO Does this do anything currently ? I'm not sure it really works.
        if self.display_thread is not None:
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
        # TODO Once movements have been resolved, units that are still stacked will start being destroyed until only one remains, beginning with the lower Power units and with ties broken randomly

    def attacker_combat_allocation_phase(orders):
        for order in orders:
            order.unit_ref.attempt_attack_on_hex(order.hexagon_ref)

    def defender_combat_allocation_phase(orders):
        for order in orders:
            order.unit_ref.attempt_join_defence_on_hex(order.hexagon_ref)

    def resolve_fights(putative_retreats):
        # NOTE Here, we ask the player to pre-specify retreats that would happen
        # if they lost
        for fight in self.all_fights:
            fight.resolve(putative_retreats)
        # TODO if no explicit order was given in pending_orders, retreat hexes are chosen at random if multiple are applicable

    """ TODO
    def first_upkeep_phase():
        Refresh mobility for all units OF THE CURRENT PLAYER

    def advancing_phase()
        # We ask player to pre-specify potential advances
        Iterate over each fight won try to see if there is an advance specified for the attacker, meaning an unit that wants to occupy the fight hex.
        Do not allow moving more than one unit per fight obviously. This move is allowed regardless of remaining mobility (so use force_move_to())
		if no explicit orders were given : if the attacker won, the attacker unit with strongest defensive power will be moved there and ties are broken at random. If the defender won, defending units don't budge without explicit orders

    def second_upkeep_phase()
        Then destroy all Fights (set map.ongoing_fights = {})
        set mobility of all units to 0 just in case
        increment turn number
        Change controllers of victory point hexes depending on who is standing on it (careful about stacked units, even though they should all belong to the same player)
    """
