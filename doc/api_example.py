import warshard


from warshard.game import Game
from warshard.map import Map, HexGrid


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
