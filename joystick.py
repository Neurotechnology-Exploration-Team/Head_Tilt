import pygame
from pygame.locals import *
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds

# Initialize Pygame
pygame.init()

# Set up colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set up screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Set up joystick dimensions
JOYSTICK_RADIUS = 100
JOYSTICK_COLOR = BLUE
JOYSTICK_DOT_RADIUS = 10
JOYSTICK_DOT_COLOR = BLACK

# Set up tilt sensor dimensions
TILT_SENSOR_SIZE = 20
TILT_SENSOR_COLOR = RED

# Set up font
FONT_SIZE = 24
font = pygame.font.Font(None, FONT_SIZE)

# Set up BoardShim and start streaming data
params = BrainFlowInputParams()
params.serial_port = 'COM8'
board = BoardShim(BoardIds.CYTON_BOARD, params)
board.prepare_session()
board.start_stream()

# Define function to draw text on screen
def draw_text(text, x, y):
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)

# Set up Pygame window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Joystick Demo")

# Keep the program running to continue receiving data and updating the display
while True:
    # Read data from the Cyton
    data = board.get_board_data()

    # Check that data has been received
    if len(data) == 0:
        continue

    # Extract joystick data from the data array
    if len(data[10]) ==0 or len(data[9]) == 0 or len(data[0]) ==0 or len(data[1]) == 0:
        continue

    joystick_x = data[9][0]
    joystick_y = data[10][0]

    # Check that joystick data is valid
    if joystick_x is None or joystick_y is None:
        continue

    # Scale joystick values to screen coordinates
    joystick_pos = (joystick_x * JOYSTICK_RADIUS, joystick_y * JOYSTICK_RADIUS)

    # Extract accelerometer data from the data array
    accel_x = data[9][0]
    accel_y = data[10][0]

    # Check that accelerometer data is valid
    if accel_x is None or accel_y is None:
        continue

    # Detect tilt and set circle color if detected
    if accel_x > 0.5:
        joystick_color = RED
        tilt_direction = "Right"
    elif accel_x < -0.5:
        joystick_color = BLUE
        tilt_direction = "Left"
    elif accel_y > 0.5:
        joystick_color = GREEN
        tilt_direction = "Down"
    elif accel_y < -0.5:
        joystick_color = WHITE
        tilt_direction = "Up"
    else:
        joystick_color = JOYSTICK_COLOR
        tilt_direction = None
    print("ALex")
    # Clear the screen
    screen.fill(BLACK)

    # Draw joystick circle
    pygame.draw.circle(screen, joystick_color, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), JOYSTICK_RADIUS)

    # Draw joystick dot
    dot_pos = (SCREEN_WIDTH // 2 + int(joystick_pos[0]), SCREEN_HEIGHT // 2 + int(joystick_pos[1]))
    pygame.draw.circle(screen, JOYSTICK_DOT_COLOR, dot_pos, JOYSTICK_DOT_RADIUS)

    # Draw tilt sensor
    pygame.draw.rect(screen, TILT_SENSOR_COLOR, (SCREEN_WIDTH - TILT_SENSOR_SIZE, SCREEN_HEIGHT - TILT_SENSOR_SIZE, TILT_SENSOR_SIZE, TILT_SENSOR_SIZE))

    # Display tilt direction if detected
    if tilt_direction is not None:
        draw_text(tilt_direction, SCREEN_WIDTH - TILT_SENSOR_SIZE - 10 - FONT_SIZE, SCREEN_HEIGHT - TILT_SENSOR_SIZE - FONT_SIZE)

    # Update the display
    pygame.display.update()
    # Add a delay to limit the update rate
    pygame.time.delay(50)
    # Check for Pygame events
    for event in pygame.event.get():
        if event.type == QUIT:
            # Stop streaming data and exit
            board.stop_stream()
            board.release_session()
            pygame.quit()
            exit()
