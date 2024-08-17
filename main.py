import pygame
import sys
from settings import *
from ball import Ball
from container import Container
from utils import get_safe_spawn_position
import random
import collections
import math

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = (
    CONTAINER_RADIUS * 2 + CONTAINER_BORDER_WIDTH * 2 + 200
)  # Increased width to accommodate button
screen_height = (
    CONTAINER_RADIUS * 2 + CONTAINER_BORDER_WIDTH * 2 + 200
)  # Increased height to accommodate button
screen_size = (screen_width, screen_height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Ball Simulation")

# Set up the clock for controlling FPS
clock = pygame.time.Clock()

# Create a container instance
container = Container(screen_size)

# Button settings
button_color = (0, 128, 128)  # Teal color
button_hover_color = (0, 200, 200)  # Lighter teal color
button_width = 150
button_height = 50
button_position = (
    screen_size[0] // 2 - button_width // 2,
    screen_size[1] // 2 + CONTAINER_RADIUS + 20,
)
button_font = pygame.font.Font(None, 36)
button_text = "Restart"
button_radius = 10  # Radius for rounded corners

# Global game state variables
game_active = True
balls = []
colors_respawned = {
    color: 0 for color in BALL_COLORS
}  # Track how many times each color has respawned


def draw_rounded_button(screen, position, size, color, text, font, radius):
    rect = pygame.Rect(position, size)
    pygame.draw.rect(screen, color, rect, border_radius=radius)
    text_surf = font.render(text, True, (0, 0, 0))
    screen.blit(
        text_surf,
        (
            position[0] + (size[0] - text_surf.get_width()) // 2,
            position[1] + (size[1] - text_surf.get_height()) // 2,
        ),
    )
    return rect


def check_button_click(position, size, mouse_pos):
    button_rect = pygame.Rect(position, size)
    return button_rect.collidepoint(mouse_pos)


def reset_game():
    global balls, game_active, colors_respawned
    balls = []
    colors_respawned = {color: 0 for color in BALL_COLORS}  # Reset color respawn counts
    for i in range(INITIAL_BALL_COUNT):
        color = BALL_COLORS[i // 2]  # Select color, 2 balls of each color
        x, y = get_safe_spawn_position(
            RESPAWN_LOCATION, screen_size, container, BALL_RADIUS
        )  # Pass required arguments
        speed_x = random.choice(
            [-BALL_SPEED, BALL_SPEED]
        )  # Randomize initial horizontal direction
        speed_y = random.choice(
            [-BALL_SPEED, BALL_SPEED]
        )  # Randomize initial vertical direction
        ball = Ball(x, y, BALL_RADIUS, color, speed_x, speed_y, screen_size)
        balls.append(ball)
    game_active = True
    container.rotating = False
    container.opening_angle = 0  # Reset the opening angle


def check_balls_exiting(balls):
    # Remove balls that exit through the opening
    balls_to_remove = []
    for ball in balls:
        angle_to_ball = math.atan2(
            ball.y - container.center[1], ball.x - container.center[0]
        )
        distance_from_center = math.sqrt(
            (ball.x - container.center[0]) ** 2 + (ball.y - container.center[1]) ** 2
        )

        # Check if the ball is within the opening
        if (
            container.radius - BALL_RADIUS
            <= distance_from_center
            <= container.radius + BALL_RADIUS
        ):
            start_angle = container.opening_angle - math.asin(
                container.opening_width / (2 * container.radius)
            )
            end_angle = container.opening_angle + math.asin(
                container.opening_width / (2 * container.radius)
            )
            if (
                start_angle <= angle_to_ball <= end_angle
                or start_angle <= angle_to_ball + 2 * math.pi <= end_angle
            ):
                balls_to_remove.append(ball)

    for ball in balls_to_remove:
        balls.remove(ball)


def count_balls_by_color(balls):
    color_count = collections.defaultdict(int)
    for ball in balls:
        color_count[ball.color] += 1
    return color_count


def log_and_stop_game(color_count):
    global game_active
    # Find the color with the maximum number of balls
    max_color = max(color_count, key=color_count.get)
    print(
        f"The color with the most balls is: {max_color} with {color_count[max_color]} balls."
    )
    game_active = False  # Stop the game loop but keep the screen visible


def game_loop():
    global game_active
    running = True

    reset_game()

    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_click = True

        # Clear the screen
        screen.fill((0, 0, 0))

        # Update the container opening rotation
        container.update_opening()

        # Draw the container
        container.draw(screen)

        if game_active:
            # Move and draw all balls if the game is still active
            for i, ball in enumerate(balls):
                ball.move()
                ball.bounce_off_walls()

                # Check for collisions with other balls
                for other in balls[i + 1 :]:
                    ball.bounce_off_ball(other, balls, container)

                ball.draw(screen)

            # Check if the ball count has reached MAX_BALL_COUNT
            if len(balls) >= MAX_BALL_COUNT:
                color_count = count_balls_by_color(balls)
                log_and_stop_game(color_count)
        else:
            # If the game is not active, just draw the balls in their last state
            for ball in balls:
                ball.draw(screen)

            # Draw the restart button
            button_color_current = (
                button_hover_color
                if check_button_click(
                    button_position, (button_width, button_height), mouse_pos
                )
                else button_color
            )
            button_rect = draw_rounded_button(
                screen,
                button_position,
                (button_width, button_height),
                button_color_current,
                button_text,
                button_font,
                button_radius,
            )

            # Check for button click
            if mouse_click and button_rect.collidepoint(mouse_pos):
                reset_game()

        # Update the display
        pygame.display.flip()

        # Control the frame rate
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    try:
        game_loop()
    except Exception as e:
        print(f"An error occurred: {e}")
