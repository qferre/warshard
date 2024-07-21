import pygame
import math
import numpy as np
import pkg_resources

from warshard.map import Map
from warshard.units import Unit

from warshard.config import DisplayConfig, Config


class Displayer:

    def __init__(self) -> None:

        # IMPORTANT : I think the scale and smoothscale methods are eating up a lot of CPU power !
        # So calculate them ONCE AND FOR ALL at the beginning, for all files !

        HEX_SIZE = DisplayConfig.HEX_SIZE

        # Load all assets
        self.assets = {}

        # Hexes
        for hex_type in Config.MOBILITY_COSTS.keys():
            hex_background_path = pkg_resources.resource_filename(
                "warshard", f"assets/hexes/{hex_type}.gif"
            )
            hex_background_image = pygame.image.load(hex_background_path)
            self.assets[f"assets/hexes/{hex_type}.gif"] = pygame.transform.scale(
                hex_background_image, (2 * HEX_SIZE, np.sqrt(3) * HEX_SIZE + 1)
            )

        # Flags
        ALL_FACTIONS = list(DisplayConfig.FACTION_COLORS.keys()) + ["none"] # remember the white flag :)
        for faction in ALL_FACTIONS:

            controller_flag_path = pkg_resources.resource_filename(
                "warshard", f"assets/flags/{faction}.jpg"
            )
            controller_flag = pygame.transform.smoothscale(
                pygame.image.load(controller_flag_path),
                (0.7 * HEX_SIZE, 0.45 * HEX_SIZE),
            )
            self.assets[f"assets/flags/{faction}.jpg"] = controller_flag

        # Unit types
        for unit_type in Config.UNIT_CHARACTERISTICS.keys():
            image_path = pkg_resources.resource_filename(
                "warshard", f"assets/units/{unit_type}.png"
            )
            pawn_image = pygame.image.load(image_path)  # Image.open(image_path)
            pawn_image = pygame.transform.smoothscale(
                pawn_image, (HEX_SIZE, HEX_SIZE * 4 / 6)
            )
            self.assets[f"assets/units/{unit_type}.png"] = pawn_image

        # same for everything that needs scaling and loading

    def draw(self, gamestate_to_draw: Map):

        pygame.init()

        screen = pygame.display.set_mode((DisplayConfig.WIDTH, DisplayConfig.HEIGHT))
        pygame.display.set_caption("WarShard game")
        font_hex = pygame.font.SysFont(None, DisplayConfig.FONT_SIZE_HEX)
        font = pygame.font.SysFont(None, DisplayConfig.FONT_SIZE)
        font_info = pygame.font.SysFont(None, DisplayConfig.FONT_SIZE_INFO)

        clock = pygame.time.Clock()
        running = True

        while running:

            try:

                map_to_draw = gamestate_to_draw.map

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                screen.fill(DisplayConfig.BACKGROUND_COLOR)

                # Draw hexagon grid
                draw_hex_grid(screen, font_hex, map_to_draw, self.assets)

                # Draw pawns
                for unit in gamestate_to_draw.map.all_units.values():
                    draw_unit(unit, screen, font, self.assets)
                    # TODO careful about stacked units

                # Draw information TODO make it programmatic fetch info
                # like {gamestate_to_draw.current_turn_number}
                info_text = f"""
                CURRENT TURN NUMBER:
                66/10
                \n
                CURRENT PHASE:
                XX Advancing Phase
                \n
                CURRENT PLAYER AU TRAIT:
                XX Germany
                \n\n\n\n\n\n
                VICTORY POINTS PER SIDE:
                Germany: XX
                USA: XX
                \n\n
                TOTAL POWER PER SIDE:
                Germany: XX
                USA: XX
                """

                draw_text(
                    screen,
                    text=info_text,
                    position=(DisplayConfig.WIDTH - 160, 50),
                    font=font_info,
                )

                # TODO draw fights
                # draw arrows showing attackers in red and defenders in blue (incl support for both) pointing from unit towards fight hex

                pygame.display.flip()  # Update display
                clock.tick(DisplayConfig.FPS)
            except RuntimeError:
                # If anything we are trying to plot changes during iteration, this can cause a RuntimeError
                # but since we are only a displayer, it does not really matter. We can never modify anything
                # anyway, so we just skip this iteration and try again.
                print(
                    "Gamestate was updated during the rendering. Skipping this rendering frame."
                )


# Set up display


def draw_hex_grid(screen, font, map_to_draw: Map, assets):
    HEX_SIZE = DisplayConfig.HEX_SIZE

    # Draw hexagon grid
    for hexagon in map_to_draw.hexgrid.hexagons.values():

        # Use xy coordinates instead of qr for drawing
        q = hexagon.x
        r = hexagon.y

        top_left_pos = axial_to_pixel(q, r, HEX_SIZE)
        center = (
            top_left_pos[0] + HEX_SIZE,
            top_left_pos[1] + np.sqrt(3) / 2 * HEX_SIZE,
        )

        # Hex background and color
        hex_background_image = assets[f"assets/hexes/{hexagon.type}.gif"]
        screen.blit(hex_background_image, (top_left_pos[0], top_left_pos[1]))

        # Draw hex borders
        corners = draw_hexagon(screen, DisplayConfig.HEX_BORDER_COLOR, center, HEX_SIZE)

        # If the hexagon is a victory point, draw a little flag of the controller
        if hexagon.victory_points > 0:


            try:
                controller_flag = assets[f"assets/flags/{hexagon.controller}.jpg"]
                
            except:
                # If controller is not recognised (usually because it's None), default to a white flag.
                controller_flag = assets["assets/flags/none.jpg"]

            screen.blit(
                                controller_flag,
                                (
                                    top_left_pos[0] + (HEX_SIZE / 2) + 0.15 * HEX_SIZE,
                                    top_left_pos[1] + 1.2 * (HEX_SIZE),
                                ),
                            )

        # TODO also add hexagon name (ie. Marseille, Bastogne, etc.) if applicable

        # Display coordinates at the top part of the hexagon
        text_position = (
            (corners[-1][0] + corners[-2][0]) / 2,
            (corners[-1][1] + corners[-2][1]) / 2 + HEX_SIZE // 5,
        )
        draw_text(
            screen,
            f"{hexagon.q},{hexagon.r}",
            text_position,
            font,
            DisplayConfig.TEXT_COLOR,
        )


def hex_corner(center, size, i):
    angle_deg = 60 * i
    angle_rad = math.pi / 180 * angle_deg
    return (
        center[0] + size * math.cos(angle_rad),
        center[1] + size * math.sin(angle_rad),
    )


def draw_hexagon(surface, color, center, size):
    corners = [hex_corner(center, size, i) for i in range(6)]
    pygame.draw.polygon(surface, color, corners, 1)
    return corners


def draw_text(surface, text, position, font, color=(0, 0, 0)):
    lines = text.splitlines()
    for i, l in enumerate(lines):
        line_surface = font.render(l, True, color)
        line_rect = line_surface.get_rect(center=position)
        surface.blit(
            line_surface, (line_rect[0], line_rect[1] + font.get_linesize() * i)
        )


def axial_to_pixel(q, r, size):
    x = size * 3 / 2 * q
    y = size * math.sqrt(3) * (r + q / 2)
    return (x, y)


#####


def draw_unit(unit: Unit, screen, font, assets):

    HEX_SIZE = DisplayConfig.HEX_SIZE

    q, r = unit.hexagon_position.x, unit.hexagon_position.y
    pixel_x, pixel_y = axial_to_pixel(q, r, size=HEX_SIZE)
    # Add half hexagon offset
    pixel_x += HEX_SIZE // 2
    pixel_y += HEX_SIZE // 2
    height = HEX_SIZE * 4 / 6
    width = HEX_SIZE

    # Faction color
    pygame.draw.rect(
        screen,
        DisplayConfig.FACTION_COLORS[unit.player_side],
        (pixel_x, pixel_y, width, height),
    )

    # Symbol
    pawn_image = assets[f"assets/units/{unit.type}.png"]
    screen.blit(pawn_image, (pixel_x, pixel_y))

    # ID
    pygame.draw.circle(
        screen, (255, 255, 255), (pixel_x, pixel_y), radius=DisplayConfig.FONT_SIZE // 2
    )
    draw_text(screen, str(unit.id), (pixel_x, pixel_y), font, color=(255, 0, 0))

    # TODO Also add name (both in the display and in the actual code) for special units like naming generals for each HQ


# """ TODO
# https://www.reddit.com/r/pygame/comments/v3ofs9/draw_arrow_function/


# import pygame

# def draw_arrow(
#         surface: pygame.Surface,
#         start: pygame.Vector2,
#         end: pygame.Vector2,
#         color: pygame.Color,
#         body_width: int = 2,
#         head_width: int = 4,
#         head_height: int = 2,
#     ):
#     """Draw an arrow between start and end with the arrow head at the end.

#     Args:
#         surface (pygame.Surface): The surface to draw on
#         start (pygame.Vector2): Start position
#         end (pygame.Vector2): End position
#         color (pygame.Color): Color of the arrow
#         body_width (int, optional): Defaults to 2.
#         head_width (int, optional): Defaults to 4.
#         head_height (float, optional): Defaults to 2.
#     """
#     arrow = start - end
#     angle = arrow.angle_to(pygame.Vector2(0, -1))
#     body_length = arrow.length() - head_height

#     # Create the triangle head around the origin
#     head_verts = [
#         pygame.Vector2(0, head_height / 2),  # Center
#         pygame.Vector2(head_width / 2, -head_height / 2),  # Bottomright
#         pygame.Vector2(-head_width / 2, -head_height / 2),  # Bottomleft
#     ]
#     # Rotate and translate the head into place
#     translation = pygame.Vector2(0, arrow.length() - (head_height / 2)).rotate(-angle)
#     for i in range(len(head_verts)):
#         head_verts[i].rotate_ip(-angle)
#         head_verts[i] += translation
#         head_verts[i] += start

#     pygame.draw.polygon(surface, color, head_verts)

#     # Stop weird shapes when the arrow is shorter than arrow head
#     if arrow.length() >= head_height:
#         # Calculate the body rect, rotate and translate into place
#         body_verts = [
#             pygame.Vector2(-body_width / 2, body_length / 2),  # Topleft
#             pygame.Vector2(body_width / 2, body_length / 2),  # Topright
#             pygame.Vector2(body_width / 2, -body_length / 2),  # Bottomright
#             pygame.Vector2(-body_width / 2, -body_length / 2),  # Bottomleft
#         ]
#         translation = pygame.Vector2(0, body_length / 2).rotate(-angle)
#         for i in range(len(body_verts)):
#             body_verts[i].rotate_ip(-angle)
#             body_verts[i] += translation
#             body_verts[i] += start

#         pygame.draw.polygon(surface, color, body_verts)


# ----------------- EXAMPLE


# import pygame

# from arrow import draw_arrow

# pygame.init()

# CLOCK = pygame.time.Clock()
# FPS = 60

# WIDTH = 1280
# HEIGHT = 720
# RESOLUTION = (WIDTH, HEIGHT)
# SCREEN = pygame.display.set_mode(RESOLUTION)

# while True:
#     CLOCK.tick(FPS)

#     for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 exit()

#     SCREEN.fill(pygame.Color("black"))

#     center = pygame.Vector2(WIDTH / 2, HEIGHT / 2)
#     end = pygame.Vector2(pygame.mouse.get_pos())
#     draw_arrow(SCREEN, center, end, pygame.Color("dodgerblue"), 10, 20, 12)

#     pygame.display.flip()
# """
