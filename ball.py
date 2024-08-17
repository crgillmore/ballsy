import pygame
import math
import random
from utils import get_safe_spawn_position
from settings import *


class Ball:
    def __init__(self, x, y, radius, color, speed_x, speed_y, screen_size):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.screen_size = screen_size
        self.can_multiply = False
        self.time_since_last_collision = 0

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

        if not self.can_multiply:
            self.time_since_last_collision += 1
            if self.time_since_last_collision > MULTIPLICATION_DELAY * FPS:
                self.can_multiply = True

    def bounce_off_walls(self):
        distance_from_center = math.sqrt(
            (self.x - self.screen_size[0] // 2) ** 2
            + (self.y - self.screen_size[1] // 2) ** 2
        )

        if distance_from_center + self.radius >= CONTAINER_RADIUS:
            angle_of_collision = math.atan2(
                self.y - self.screen_size[1] // 2, self.x - self.screen_size[0] // 2
            )

            self.speed_x = -self.speed_x * BOUNCE_LOSS
            self.speed_y = -self.speed_y * BOUNCE_LOSS

            # Move the ball slightly away from the wall to prevent repeated collisions
            overlap = (distance_from_center + self.radius) - CONTAINER_RADIUS
            self.x -= math.cos(angle_of_collision) * overlap
            self.y -= math.sin(angle_of_collision) * overlap

    def bounce_off_ball(self, other, balls, container):
        dx = other.x - self.x
        dy = other.y - self.y
        distance = math.sqrt(dx**2 + dy**2)

        if distance < self.radius + other.radius:
            # Calculate the angle of collision
            angle = math.atan2(dy, dx)

            # Calculate the speed components along the collision angle
            speed1 = self.speed_x * math.cos(angle) + self.speed_y * math.sin(angle)
            speed2 = other.speed_x * math.cos(angle) + other.speed_y * math.sin(angle)

            # Swap the speeds along the collision angle
            self.speed_x, other.speed_x = (
                speed2 * math.cos(angle) - self.speed_y * math.sin(angle),
                speed1 * math.cos(angle) - other.speed_y * math.sin(angle),
            )
            self.speed_y, other.speed_y = (
                speed2 * math.sin(angle) + self.speed_y * math.cos(angle),
                speed1 * math.sin(angle) + other.speed_y * math.cos(angle),
            )

            # Move the balls slightly apart to prevent overlapping
            overlap = 0.5 * (self.radius + other.radius - distance)
            self.x -= math.cos(angle) * overlap
            self.y -= math.sin(angle) * overlap
            other.x += math.cos(angle) * overlap
            other.y += math.sin(angle) * overlap

            # Check for multiplication condition
            if (
                self.can_multiply
                and other.can_multiply
                and BALL_MULTIPLICATION_ON_COLLISION
                and self.color == other.color
                and len(balls) < MAX_BALL_COUNT
            ):
                for _ in range(MULTIPLICATION_FACTOR):
                    x, y = get_safe_spawn_position(
                        COLLISION_RESPAWN_LOCATION,
                        self.screen_size,
                        container,
                        BALL_RADIUS,
                    )
                    new_ball = Ball(
                        x,
                        y,
                        self.radius,
                        self.color,
                        random.choice([-BALL_SPEED, BALL_SPEED]),
                        random.choice([-BALL_SPEED, BALL_SPEED]),
                        self.screen_size,
                    )
                    balls.append(new_ball)
                # Reset multiplication ability after spawning new balls
                self.can_multiply = False
                other.can_multiply = False

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
