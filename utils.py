import math
import random
from settings import *

def get_safe_spawn_position(location, screen_size, container, BALL_RADIUS):
    if location == "random":
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(0, container.radius - BALL_RADIUS)
        x = container.center[0] + math.cos(angle) * distance
        y = container.center[1] + math.sin(angle) * distance
    elif location == "middle":
        x = screen_size[0] // 2
        y = screen_size[1] // 2
    elif location == "left":
        x = container.center[0] - container.radius + BALL_RADIUS  # Near the left edge
        y = screen_size[1] // 2
    elif location == "right":
        x = container.center[0] + container.radius - BALL_RADIUS  # Near the right edge
        y = screen_size[1] // 2
    elif location == "top":
        x = screen_size[0] // 2
        y = container.center[1] - container.radius + BALL_RADIUS  # Near the top edge
    elif location == "bottom":
        x = screen_size[0] // 2
        y = container.center[1] + container.radius - BALL_RADIUS  # Near the bottom edge
    else:
        # Default to center if the location is not recognized
        x = screen_size[0] // 2
        y = screen_size[1] // 2
    
    return x, y
