import time
import pygame
import math
import numpy as np

from warshard.map import Map
from warshard.units import Unit

# Constants
# TODO move to config.py into the DisplayConfig
WIDTH, HEIGHT = 1200, 820
FPS = 5
HEX_SIZE = 30
FONT_SIZE_HEX = 12
FONT_SIZE = 18
BACKGROUND_COLOR = (255, 255, 255)
HEX_COLOR = (0, 0, 0)
TEXT_COLOR = (0, 0, 0)


class Displayer:

    @staticmethod
    def draw(gamestate_to_draw: Map):

        pygame.init()

        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("WarShard game")
        font_hex = pygame.font.SysFont(None, FONT_SIZE_HEX)
        font = pygame.font.SysFont(None, FONT_SIZE)

        clock = pygame.time.Clock()
        running = True

        while running:

            try:

                map_to_draw = gamestate_to_draw.map

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                screen.fill(BACKGROUND_COLOR)

                # Draw hexagon grid
                draw_hex_grid(
                    screen,
                    WIDTH,
                    HEIGHT,
                    HEX_COLOR,
                    HEX_SIZE,
                    font_hex,
                    TEXT_COLOR,
                    map_to_draw,
                )

                # Draw pawns
                for unit in gamestate_to_draw.map.all_units.values():
                    draw_unit(unit, screen, font)
                    # TODO careful about stacked units

                # Draw information TODO make it programmatic fetch
                info_text = f"""
                Current turn number: 66/10
                \n
                Current phase : XX Advancing Phase
                Current player au trait : XX Germany
                \n\n\n
                Victory points per side:
                Germany: XX
                USA: XX
                \n\n
                Remaining power per side:
                Germany: XX
                USA : XX
                """

                draw_text(
                    screen,
                    text=info_text,
                    position=(WIDTH - 150, 50),
                    font=font,
                )

                pygame.display.flip()  # Update display
                clock.tick(FPS)
            except RuntimeError:
                # If anything we are trying to plotchanges during iteration, this can cause a RuntimeError
                # but since we are only a displayer, it does not really matter. We can never modify anything
                # anyway, so we just skip this iteration and try again.
                print(
                    "Gamestate was updated during the rendering. Skipping this rendering frame."
                )


# Set up display


def draw_hex_grid(
    screen,
    WIDTH,
    HEIGHT,
    HEX_COLOR,
    HEX_SIZE,
    font,
    TEXT_COLOR,
    map_to_draw: Map,
):
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

        # TODO make HEX_COLOR (and later, a cute hex image directly) depend on hexagon.type
        hex_background_path = pkg_resources.resource_filename(
            "warshard", f"assets/hexes/{hexagon.type}.gif"
        )
        hex_background_image = pygame.image.load(hex_background_path)
        hex_background_image = pygame.transform.scale(
            hex_background_image, (2 * HEX_SIZE, np.sqrt(3) * HEX_SIZE + 1)
        )
        screen.blit(hex_background_image, (top_left_pos[0], top_left_pos[1]))

        # Draw grid
        corners = draw_hexagon(screen, HEX_COLOR, center, HEX_SIZE)

        # TODO if the hexagon is a victory point, draw a little flag of the controller

        # TODO also add hexagon name (ie. Marseille, Bastogne, etc.) if applicable

        # Display coordinates at the top part of the hexagon
        text_position = (
            (corners[-1][0] + corners[-2][0]) / 2,
            (corners[-1][1] + corners[-2][1]) / 2 + HEX_SIZE // 5,
        )
        draw_text(screen, f"{hexagon.q},{hexagon.r}", text_position, font, TEXT_COLOR)


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

    # TODO Use this to render multiline text
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

import pkg_resources
from PIL import Image
from warshard.config import DisplayConfig


def draw_unit(unit: Unit, screen, font):
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
    image_path = pkg_resources.resource_filename(
        "warshard", f"assets/units/{unit.type}.png"
    )
    pawn_image = pygame.image.load(image_path)  # Image.open(image_path)
    pawn_image = pygame.transform.scale(pawn_image, (width, height))
    screen.blit(pawn_image, (pixel_x, pixel_y))

    # TODO add color (for faction) and ID
    draw_text(screen, str(unit.id), (pixel_x, pixel_y), font, color=(255, 0, 0))
