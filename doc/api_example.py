import warshard


from warshard.game import Game
from warshard.map import Map, HexGrid
from warshard.units import Unit


g = Game()


# Ensure map can be updated
g.map.all_units.append(
    Unit(
        hexagon_position=g.map.hexgrid.hexagons[(2, 2)],
        type="armor",
        player_side="germany",
    )
)


g.map.all_units.append(
    Unit(
        hexagon_position=g.map.hexgrid.hexagons[(0, 0)],
        type="infantry",
        player_side="germany",
    )
)

# g.map = Map(max_q=5)
# yes it can :)


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

##### CAPITAL TODO : very likely that the game.run_a_turn will be subdivided into functions that each run a turn phase, and each of these functions will read pending_orders. This means we can run phase and let orders be adjusted by the agent depending on, for example, fights declared.
##### Furthermore, we also need to expose functinos to give individual orders (ie. start a fight here, etc.) so the simulation can be run with granulatiry in
##### a notebook, as if we were playing, and not just entire phase by entire phase. Although for me this is not as critical since all events of an entire phase
##### are supposed to execute simultaneously and without input of the opponent (--> in the rules you make all your attacker declarations before the opponent gets an opportunity to make defender support declarations)
### Howver, make it explicit that there exist funcitons like _debug_force_movement and _debug_force_destruction and _debug_force_spawn
