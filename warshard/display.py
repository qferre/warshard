import time
import pygame
import math

from warshard.map import Map
from warshard.units import Unit

# Constants
WIDTH, HEIGHT = 1200, 820
FPS = 5
HEX_SIZE = 30
FONT_SIZE_HEX = 12
FONT_SIZE = 18
BACKGROUND_COLOR = (255, 255, 255)
HEX_COLOR = (0, 0, 0)
TEXT_COLOR = (255, 0, 0)


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
                    draw_unit(unit, screen)

                # Draw information
                info_text = f"""

                Current turn number
                current phase and player au trait
                
                Victory points per side
                Remaining power per side
                
                other explanations like 'please input orders in terminal'


                """

                draw_text(
                    screen,
                    text=info_text,
                    position=(WIDTH - 200, 50),
                    font=font,
                )

                pygame.display.flip()  # Update display
                clock.tick(FPS)
            except RuntimeError: 
                # If anything changes size during iteration this can cause a RuntimeError: dictionary changed size during iteration
                # but since we are only a displayer, it does not really matter.
                # we can never modify anything anyway, so we just skip this iteration and try again
                print("Gamestate was updated during the rendering. Skipping this rendering frame.")
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
        # center = axial_to_pixel(hexagon.q, hexagon.r, HEX_SIZE)

        # Use xy coordinates instead of qr for drawing
        q = hexagon.x
        r = hexagon.y

        center = axial_to_pixel(q, r, HEX_SIZE)
        center = (center[0] + HEX_SIZE, center[1] + HEX_SIZE)
        corners = draw_hexagon(screen, HEX_COLOR, center, HEX_SIZE)
        # TODO make HEX_COLOR (and later, a cute hex image directly) depend on hexagon.type
        # TODO if the hexagon is a victory point, draw a little flag of the controller
        # TODO also add hexagon name (ie. Marseille, Bastogne, etc.) if applicable

        # Display coordinates at the top part of the hexagon
        text_position = (
            (corners[-1][0] + corners[-2][0]) / 2,
            (corners[-1][1] + corners[-2][1]) / 2 + HEX_SIZE // 5,
        )
        draw_text(screen, f"({hexagon.q},{hexagon.r})", text_position, font, TEXT_COLOR)


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
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=position)
    surface.blit(text_surface, text_rect)


def axial_to_pixel(q, r, size):
    x = size * 3 / 2 * q
    y = size * math.sqrt(3) * (r + q / 2)
    return (x, y)


#####

import pkg_resources
from PIL import Image


def draw_unit(unit: Unit, screen):
    q, r = unit.hexagon_position.x, unit.hexagon_position.y
    pixel_x, pixel_y = axial_to_pixel(q, r, size=HEX_SIZE)
    # Add half hexagon offset
    pixel_x += HEX_SIZE // 2
    pixel_y += HEX_SIZE // 2

    image_path = pkg_resources.resource_filename(
        "warshard", f"assets/units/{unit.type}.png"
    )
    pawn_image = pygame.image.load(image_path)  # Image.open(image_path)
    pawn_image = pygame.transform.scale(pawn_image, (HEX_SIZE, HEX_SIZE * 4 / 6))
    screen.blit(pawn_image, (pixel_x, pixel_y))
