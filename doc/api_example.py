import warshard


from warshard.game import Game
from warshard.map import Map, HexGrid
from warshard.units import Unit


g = Game()



# ## API is like this :
# game = warshard.game.create_game(
#     yaml_file,
#     headless = false # If false, another thread is launched which displays the gamestate using pygame
#     log_file_path
#     )
# game.gamestate # You can use this to read the gamestate and even modify it, it is accessible – say so explicitly in documentation

# # Recommended setup for AI
# custom_gamestate_representation_observation = my_function_that_reads_gamestate_and_produces_output_in_correct_format(game.gamestate)
# #reward = reward_function(custom_gamestate_representation_observation OR DIRECTLY game.gamestate)
# pending_orders = my_custom_ai_agent(custom_gamestate_representation_observation)

# # Finally run turn
# game.run_a_turn/step(pending_orders)
# TODO : write EXPLICITLY that you may (and indeed should), instead of calling directly run_a_turn, LOOK INTO THE SOURCE CODE OF RUN_A_TURN AND CALL EACH FUNCTION THAT RUNS A PHASE INDIVIDUALLY. Indeed, these functions have been designed to be run like this, separately : run_a_turn does little more than simply call each function in order !

##### CAPITAL TODO : very likely that the game.run_a_turn will be subdivided into functions that each run a turn phase, and each of these functions will read pending_orders. This means we can run phase and let orders be adjusted by the agent depending on, for example, fights declared.
##### Furthermore, we also need to expose functinos to give individual orders (ie. start a fight here, etc.) so the simulation can be run with granulatiry in
##### a notebook, as if we were playing, and not just entire phase by entire phase. Although for me this is not as critical since all events of an entire phase
##### are supposed to execute simultaneously and without input of the opponent (--> in the rules you make all your attacker declarations before the opponent gets an opportunity to make defender support declarations)
### Howver, make it explicit that there exist funcitons like _debug_force_movement and _debug_force_destruction and _debug_force_spawn
