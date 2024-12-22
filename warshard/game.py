import threading
import time
from functools import partial
import logging
import itertools
from collections import defaultdict
import random
import numpy as np

from warshard import display
from warshard.map import Map
from warshard.units import Unit
from warshard.actions import Order
from warshard.config import Config


class Game:

    global self  # Necessary so the Game object can be passed to the display thread

    def __init__(
        self, log_file_path: str = "./example.log", headless=False, random_seed=42
    ) -> None:
        """_summary_


        Attributes:
            map : stores the gamestate. You can use this to read the map/gamestate and even modify it, it is accessible

        Args:
            log_file_path (str, optional): _description_. Defaults to "./example.log".
            headless (bool, optional): _description_. Defaults to False.
            random_seed (int, optional): _description_. Defaults to 42.
        """

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
        self.map = Map()
        self.players = [None, None]  # Players, in order
        self.current_active_player_id = (
            0  # The ID corresponds to a position in the self.players list
        )
        self.current_turn_phase = None
        self.current_turn_number = 0
        self.scenario_max_turns = 100

        # Display
        self.display_thread = None
        self.display_stopping_event = threading.Event()
        if not headless:
            logging.debug("Starting display thread")

            self.displayer = display.Displayer()

            self.display_thread = threading.Thread(
                target=partial(
                    self.displayer.draw,
                    gamestate_to_draw=self,
                ),
            )
            self.display_thread.start()

        self.all_orders_ever_given = defaultdict(list)
        # Random seeding to ensure that the game is reproducible if we retrieve all the logged
        # orders and pass them again
        self.random_seed = random_seed
        random.seed(random_seed)
        np.random.seed(random_seed)

    def run_a_turn(self, this_turn_orders: list[Order]):
        """_summary_

        Args:
            this_turn_orders (_type_): allows my framework to be easily used with AI ! a list containing pairs of (Unit, Hexagon). When requesting orders, we first check if any pending orders are present and try to execute those first. Orders are executed in FIFO, meaning you can queue movement orders for the same unit.
                note that we will iterate over this_turn_orders multiple times : first for the movement, then for the attacker combat, then for the defender allocation (the idea being that defender can pre-allocate support by order of priority, we simply skip an allocation if it is not necessary meaning no fight takes place here), etc.
                We will also separat them if they are putative or not


        Attributes:
            all_orders_ever_given is a dictionary of all orders by turn number ({turn_number : list of Orders}). If the random seed is the same, results will be the same, so executing the same orders
            would let you essentially re-load a saved game
        """
        # Remember all orders ever given
        if self.current_turn_number not in self.all_orders_ever_given:
            self.all_orders_ever_given[self.current_turn_number] = []
        self.all_orders_ever_given[self.current_turn_number] += this_turn_orders

        # By default, always send the same this_turn_orders and ignore all non applicable
        # orders when processing

        # Split orders into regular and putative
        regular_orders_this_turn = [
            order for order in this_turn_orders if not order.is_putative
        ]
        putative_orders_this_turn = [
            order for order in this_turn_orders if order.is_putative
        ]

        # Check that the current turn number is less than the maximum allowed turns
        if self.current_turn_number >= self.scenario_max_turns:
            self.logger.info("Maximum number of turns reached. Ending game.")
            self.stop()
            return

        # All regular or putative orders are passed at once, since invalid orders should simply be ignored
        # for example, a combat order should be ignored in the movemnt phase since it would be meaningless

        # Do not call this on the first turn
        self.set_active_player()

        self.current_turn_phase = "first_upkeep"
        self.first_upkeep_phase()

        self.current_turn_phase = "movement"
        self.movement_phase(regular_orders_this_turn)

        self.current_turn_phase = "update_supply"
        self.update_supply()

        self.current_turn_phase = "attacker_combat_allocation"
        self.attacker_combat_allocation_phase(regular_orders_this_turn)

        self.current_turn_phase = "defender_combat_allocation"
        self.defender_combat_allocation_phase(regular_orders_this_turn)

        self.current_turn_phase = "resolve_fights"
        self.resolve_fights(putative_orders_this_turn)

        self.current_turn_phase = "advancing"
        self.advancing_phase(putative_orders_this_turn)

        self.current_turn_phase = "second_upkeep"
        self.second_upkeep_phase()

    def stop(self):
        self.display_stopping_event.set()

        self.logger.info("Game has ended.")

    #############################

    def set_active_player(self):
        self.logger.info(f"Current turn is {self.current_turn_number}")
        self.current_active_player_id = self.current_turn_number % len(self.players)
        self.current_active_player = self.players[self.current_active_player_id]

        self.logger.debug(f"Switching active player to {self.current_active_player}")
        self.logger.info(f"Switching active player to {self.current_active_player}")
        self.logger.warning(f"Switching active player to {self.current_active_player}")
        self.logger.error(f"Switching active player to {self.current_active_player}")

    def first_upkeep_phase(self):
        # Refresh mobility for all units OF THE CURRENT PLAYER
        for unit_id, unit in self.map.all_units.items():
            if unit.player_side == self.current_active_player:
                unit.mobility_remaining = unit.mobility

    def movement_phase(self, orders):
        # Iterate over each unit : for each, check in pending orders to a nearby hex from user (which can be the same hex as current to make them “stay” even though it's useless) until MP are exhausted
        for order in orders:
            order.unit_ref.attempt_move_to(order.hexagon_ref)
        # TODO Once movements have been resolved, units that are still stacked will start being destroyed until only one remains, beginning with the lower Power units and with ties broken randomly

    def update_supply(self):
        # Now that all movements have been done, update supply
        # Iterate over all HQs of all players, and tag all hexes in supply for this
        # player in the hex.in_supply_for_player list (remember to empty it before so supply does not stay between turns)
        self.map.hexes_currently_in_supply_per_player = defaultdict(list)
        for unit in self.map.all_units.values():
            if unit.type == "hq":

                # Get all hexes within SUPPLY_RANGE of this hq
                dist_dict = unit.hexagon_position.get_all_hexes_within_continuous_path(
                    max_rank=Config.SUPPLY_RANGE
                )

                ldv = list(dist_dict.values())
                hexes_supplied_by_this_hq = itertools.chain.from_iterable(ldv)
                self.map.hexes_currently_in_supply_per_player[
                    unit.player_side
                ] += hexes_supplied_by_this_hq

        # Now make all unique:
        for k, v in self.map.hexes_currently_in_supply_per_player.items():
            # print(v)
            self.map.hexes_currently_in_supply_per_player[k] = set(v)

    def attacker_combat_allocation_phase(self, orders):
        for order in orders:
            order.unit_ref.attempt_attack_on_hex(order.hexagon_ref)

    def defender_combat_allocation_phase(self, orders):
        for order in orders:
            order.unit_ref.attempt_join_defence_on_hex(order.hexagon_ref)

    def resolve_fights(self, putative_retreats, debug_force_rolls=None):

        for order in putative_retreats:
            assert order.is_putative

        # NOTE Here, we ask the player to pre-specify retreats that would happen
        # if they lost
        for i, fight in enumerate(self.map.ongoing_fights.values()):

            if debug_force_rolls is not None:
                force_roll = debug_force_rolls[i]
            else:
                force_roll = None  # If None, let the roll be random
            fight.resolve(putative_retreats, debug_force_dice_roll_to=force_roll)

    def advancing_phase(self, putative_advance_orders):
        """
        Iterate over each fight won try to see if there is an advance specified for the attacker, meaning an unit that wants to occupy the fight hex.

        We ask player to pre-specify potential advances.

        NOTE if no explicit advance orders were given, attacking units won't budge even if the fight is won


        Args:
            putative_advance_orders (_type_): _description_
        """

        for order in putative_advance_orders:
            assert order.is_putative

        for fight in self.map.ongoing_fights.values():

            fight.an_advance_was_made = False

            if fight.fight_result in Config.ATTACKER_VICTORIES_RESULTS:

                # Only melee units can advance
                potential_advancers = [
                    attacker
                    for attacker in fight.attacking_units
                    if attacker.type in Config.MELEE_UNITS
                ]
                potential_advancers_id = [u.id for u in potential_advancers]

                # Try to execute each proposed advance. An invalid order will be ignored.
                for order in putative_advance_orders:
                    if not fight.an_advance_was_made:
                        if order.unit_id in potential_advancers_id:
                            # Can only advance into the hexagon of a Fight:
                            if order.hexagon_ref == fight.fight_hexagon:
                                try:
                                    unit = self.map.fetch_unit_by_id(order.unit_id)
                                    unit.force_move_to(
                                        order.hexagon_ref
                                    )  # This move is allowed regardless of remaining mobility (so use force_move_to())
                                    fight.an_advance_was_made = True  # ensure we cannot move more than one unit per won fight

                                except KeyError:
                                    # If the unit could not be fetched, it's likely because it was destroyed.
                                    # In that case, we just ignore the order.
                                    pass

    def second_upkeep_phase(self):
        # Then destroy all Fights
        self.map.ongoing_fights = {}

        for unit in self.map.all_units.values():
            # Set mobility of all units to 0 just in case
            unit.mobility_remaining = 0

            # Change controllers of victory point hexes depending on who is standing on it
            unit.hexagon_position.controller = unit.player_side

        # Deploy reinforcements if applicable
        # TODO finish implementing it !
        # NOTE those will pop in even if it implies stacking, which must be corrected in the next movement phase
        """
        for planned_reinforcement in self.planned_reinforcements:
            if planned_reinforcement.turn == self.current_turn_number:
                self.map.force_spawn_unit_at_position(
                    unit_type=planned_reinforcement.type,
                    hex_q=planned_reinforcement.q,
                    hex_r=planned_reinforcement.r,
                    player_side=planned_reinforcement.player_side,
                    id=planned_reinforcement.id,
                )
        """
        # TODO Related to reinforcements, implement remplacements : units that were destroyed may be reconstituted depending on dice roll.
        """
        When destroying an unit with unit.destroy_myself(), change the funciton so that it is placed in a pile
        of destroyed units that may be reconstituted
        """

        # Increment turn number
        self.current_turn_number += 1
