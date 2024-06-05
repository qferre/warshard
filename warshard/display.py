from warshard.map import Map
import time
import pygame
import math


class Displayer:

    @staticmethod
    def draw(map_to_draw: Map):

        # Constants
        WIDTH, HEIGHT = 1920, 1080  # 1024, 768
        FPS = 5
        HEX_SIZE = 40  # 30
        FONT_SIZE = 14
        BACKGROUND_COLOR = (255, 255, 255)
        HEX_COLOR = (0, 0, 0)
        TEXT_COLOR = (255, 0, 0)

        pygame.init()

        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("WarShard game")
        font = pygame.font.SysFont(None, FONT_SIZE)

        # while True:
        #     print(map)
        #     time.sleep(1)

        clock = pygame.time.Clock()
        running = True

        while running:
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
                font,
                TEXT_COLOR,
                map_to_draw,
            )

            # Draw pawns
            # for pawn in blabla:
            #     pawn_coordinates = (pawn_x_pixel, pawn_y_pixel)
            #     screen.blit(pawn1_image, pawn_coordinates)

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
