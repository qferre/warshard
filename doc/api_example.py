import warshard


from warshard.game import Game
from warshard.map import Map, HexGrid
from warshard.units import Unit


g = Game()


"""
## API is like this :
game = warshard.game.create_game(
    yaml_file,
    headless = True # If false, another thread is launched which displays the gamestate using pygame
    log_file_path
    )


game
game.map # You can use this to read the map/gamestate and even modify it, it is accessible - say so explicitly in documentation

# Example of a recommended setup for AI
custom_gamestate_representation_observation = my_function_that_reads_gamestate_and_produces_output_in_correct_format(game.gamestate)
def reward_function(game): return game.map.hexgrid.get_total_victory_points_per_players()
#reward = reward_function(custom_gamestate_representation_observation OR DIRECTLY game)
pending_orders = my_custom_ai_agent(custom_gamestate_representation_observation)

# Finally run turn
game.run_a_turn/step(pending_orders)
"""


# TODO : write EXPLICITLY that you may (and indeed should), instead of calling directly run_a_turn, LOOK INTO THE SOURCE CODE OF RUN_A_TURN AND CALL EACH FUNCTION THAT RUNS A PHASE INDIVIDUALLY. Indeed, these functions have been designed to be run like this, separately : run_a_turn does little more than simply call each function in order !
# This means we can run phase and let orders be adjusted by the agent depending on, for example, fights declared.

# There are also functions that give individual orders (ie. start a fight here, etc.) so the simulation can be run with granulatiry in  a notebook, as if we were playing, and not just entire phase by entire phase. Although for me this is not as critical since all events of an entire phase are supposed to execute simultaneously and without input of the opponent (--> in the rules you make all your attacker declarations before the opponent gets an opportunity to make defender support declarations)
# Look at the python file of the tests for examples of this


# TODO :also explain that you can and should give multiple orders fo the same units to be executed in sequence for the movement
# Foe example : if you want to move unit 6 from hex 1,2 to hex 1,5, you need to write three move orders IN THE CORRECT ORDER FOR THE SAME UNIT :
# "6 move to 1,3" then "6 move to 1,4" then "6 move to 1,5" and those must be IN THE CORRECT ORDER in the pending_orders list, since we execute orders
# in a FIFO fashion

# TODO : I also have planned to have an order_type so retreat orders are not executed in the movement phase. IMPLEMENT THIS AND ENSURE THE FUNCTIONS THAT PARSE THE pending_orders LIST CHECK FOR THAT !!!