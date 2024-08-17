import pygame
import math
from settings import *

class Container:
    def __init__(self, screen_size):
        self.screen_size = screen_size
        self.center = (
            screen_size[0] // 2,
            screen_size[1] // 2,
        )
        self.radius = CONTAINER_RADIUS
        self.color = CONTAINER_COLOR
        self.border_width = CONTAINER_BORDER_WIDTH
        self.opening_angle = 0
        self.opening_width = BALL_RADIUS * 2  # The width of the notch, equal to one ball diameter
        self.rotating = CONTAINER_ROTATION_ENABLED

    def update_opening(self):
        if self.rotating:
            self.opening_angle += CONTAINER_ROTATION_SPEED  # Use the variable speed from settings
            if self.opening_angle >= 2 * math.pi:
                self.opening_angle -= 2 * math.pi

    def draw(self, screen):
        # Draw the full container circle
        pygame.draw.circle(screen, self.color, self.center, self.radius, self.border_width)

        if self.rotating:
            # Draw the arc for the opening (the notch)
            start_angle = self.opening_angle - math.asin(self.opening_width / (2 * self.radius))
            end_angle = self.opening_angle + math.asin(self.opening_width / (2 * self.radius))

            # Create a surface to draw the arc and mask it onto the container
            container_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
            pygame.draw.arc(
                container_surface,
                (0, 0, 0, 0),  # Transparent to create the notch
                (
                    0,
                    0,
                    self.radius * 2,
                    self.radius * 2,
                ),
                start_angle,
                end_angle,
                self.border_width,
            )

            # Mask the notch onto the main screen
            screen.blit(container_surface, (self.center[0] - self.radius, self.center[1] - self.radius), special_flags=pygame.BLEND_RGBA_SUB)
