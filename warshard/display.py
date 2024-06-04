from warshard.map import Map
import time
import pygame
import math


class Displayer:

    @staticmethod
    def draw(map: Map):

        # Constants
        WIDTH, HEIGHT = 800, 600
        FPS = 30
        HEX_SIZE = 40
        FONT_SIZE = 12
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
            draw_hex_grid(screen, WIDTH, HEIGHT, HEX_COLOR, HEX_SIZE, font, TEXT_COLOR)

            pygame.display.flip()
            clock.tick(FPS)


# Set up display


def draw_hex_grid(screen, WIDTH, HEIGHT, HEX_COLOR, HEX_SIZE, font, TEXT_COLOR):
    # Draw hexagon grid
    for q in range(-2, 3):
        for r in range(-2, 3):
            center = axial_to_pixel(q, r, HEX_SIZE)
            center = (center[0] + WIDTH // 2, center[1] + HEIGHT // 2)
            corners = draw_hexagon(screen, HEX_COLOR, center, HEX_SIZE)

            # Display coordinates at the top part of the hexagon
            text_position = (
                (corners[0][0] + corners[1][0]) / 2,
                (corners[0][1] + corners[1][1]) / 2,
            )
            draw_text(screen, f"({q},{r})", text_position, font, TEXT_COLOR)


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


def draw_text(surface, text, position, font, color):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=position)
    surface.blit(text_surface, text_rect)


def axial_to_pixel(q, r, size):
    x = size * 3 / 2 * q
    y = size * math.sqrt(3) * (r + q / 2)
    return (x, y)
