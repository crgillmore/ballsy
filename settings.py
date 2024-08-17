# settings.py

# Container settings
CONTAINER_RADIUS = 200
CONTAINER_COLOR = (255, 255, 255)
CONTAINER_BORDER_WIDTH = 5
CONTAINER_ROTATION_ENABLED = True
CONTAINER_ROTATION_SPEED = 0.02

# Ball Settings
INITIAL_BALL_COUNT = 8  # Initial number of balls to spawn
BALL_COLORS = [
    (0, 0, 255),
    (0, 128, 128),
    (255, 255, 0),
    (255, 165, 0),
]  # Blue, Teal, Yellow, Orange
BALL_RADIUS = 10  # Radius of each ball
BALL_SPEED = 5  # Speed of the balls

# Bounce Settings
BOUNCE_LOSS = (
    0.9  # Coefficient of restitution (1.0 = perfect bounce, <1.0 = loss of energy)
)
BALL_BALL_BOUNCE_SENSITIVITY = (
    1.0  # Sensitivity of bounce when balls collide with each other
)
BALL_WALL_BOUNCE_SENSITIVITY = (
    1.0  # Sensitivity of bounce when balls collide with the container wall
)

# Interaction Settings
MAX_BALL_COUNT = 250  # Maximum number of balls allowed in the container
BALL_MULTIPLICATION_ON_COLLISION = True  # Whether balls multiply when they collide
MULTIPLICATION_FACTOR = (
    1  # How many new balls to spawn on collision if multiplication is enabled
)
MULTIPLICATION_DELAY = 0.5  # Delay between each new ball spawn (in seconds)

# Respawn location options
RESPAWN_LOCATION = (
    "random"  # Options: "random", "middle", "left", "right", "top", "bottom"
)
COLLISION_RESPAWN_LOCATION = (
    "middle"  # Options: "random", "middle", "left", "right", "top", "bottom"
)

# Simulation Settings
FPS = 60  # Frames per second for the simulation

# Additional Settings
GRAVITY_ENABLED = True  # Enable gravity in the simulation
GRAVITY_FORCE = 0.5  # Strength of gravity if enabled

# Rotation Settings
ROTATION_ENABLED = True  # Enable rotation of the container
ROTATION_SPEED = 1.0  # Speed at which the container rotates

# Export/Import Settings (for saving and loading game states)
SAVE_STATE_FILE = "game_state.json"  # File to save the game state
LOAD_STATE_FILE = "game_state.json"  # File to load the game state
