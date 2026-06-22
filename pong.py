# RETRO PONG 84' WITH NO EXTRA MATS #
# Imports
import pygame
pygame.init()
import sys
from random import randint
pygame.font.init()

# Constant variables
FPS = 60
WIDTH = 800
HEIGHT = 600

# Game Variables
paddle_height = 100
paddle_width = 15
paddle_speed = 10

# Game Colors
black = (0, 0, 0)
white = (255, 255, 255)

# Game Settings
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RETRO PONG 84'")
clock = pygame.time.Clock()

# Winning Messages
winner1_message = f"Player 1 is the winner!"
winner2_message = f"Player 2 is the winner!"

# Player Positions
player1_pos = [50, (HEIGHT - paddle_height)/2]
player2_pos = [WIDTH - 50 - paddle_width, (HEIGHT - paddle_height)/2]

# Ball Positions
ball_pos = [(WIDTH/2), (HEIGHT/2)]
ball_speed = [7,7]

              # Functions #

# Make a Paddle
def draw_paddle(pos):
    # module.action.thing(where, color, (width, height, x, y))
    pygame.draw.rect(screen, white, (pos[0], pos[1], paddle_width, paddle_height))

# Make a Ball
def draw_ball(pos):
    # module.action.thing(where, color, (width, height, x, y))
    pygame.draw.circle(screen, white, pos, 15)

# Update the ball
def update_ball():
    # Grabs the variables from outside the function and creates the ability to override them
    global ball_pos, ball_speed, player1_score, player2_score
    # balls x position + the ball speed 7
    ball_pos[0] += ball_speed[0]
    # balls y position + the ball speed 7
    ball_pos[1] += ball_speed[1]

    # Ball logic to bounce the ball off top and bottom
    if ball_pos[1] <= 10 or ball_pos[1] >= HEIGHT - 10:
        ball_speed[1] = -ball_speed[1]

    elif ball_pos[0] < player1_pos[0] + paddle_width and player1_pos[1] <= ball_pos[1] <= player1_pos[1] + paddle_height:
        ball_speed[0] = -ball_speed[0]

    elif ball_pos[0] >= player2_pos[0] and player2_pos[1] <= ball_pos[1] <= player2_pos[1] + paddle_height:
        ball_speed[0] = -ball_speed[0]

    # Player Scores
    if ball_pos[0] <= 0:
        # Player 2 scores
        player2_score += 1
        # Calls reset function to start a new round
        reset()

    if ball_pos[0] >= WIDTH:
        # Player 1 scores
        player1_score += 1
        # Calls reset function to start a new round
        reset()

# Reset function for rounds
def reset():
    global ball_pos, ball_speed
    ball_pos = [(WIDTH / 2), (HEIGHT / 2)]
    num = randint(0, 1)
    # Randomizes which way the ball starts in the direction of at the beginning
    if num == 0:
        ball_speed = [-7, -7]
    else:
        ball_speed = [7, 7]

# Scores
player1_score = 0
player2_score = 0

# Initializes the Font class in the variable "style"
style = pygame.font.Font(None, 45)

# Main Game Loop
bob = True
while bob:

    # Event Handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Program the keyboard to be the player's controls
    keys = pygame.key.get_pressed()

    # Player 1 Controls
    # Up
    if keys[pygame.K_w] and player1_pos[1] > 0:
        player1_pos = (player1_pos[0], player1_pos[1] - paddle_speed)
    # Down
    elif keys[pygame.K_s] and player1_pos[1] < HEIGHT - paddle_height:
        player1_pos = (player1_pos[0], player1_pos[1] + paddle_speed)

    # Player 2 Controls
    # Up
    if keys[pygame.K_UP] and player2_pos[1] > 0:
        player2_pos = (player2_pos[0], player2_pos[1] - paddle_speed)
    # Down
    elif keys[pygame.K_DOWN] and player2_pos[1] < HEIGHT - paddle_height:
        player2_pos = (player2_pos[0], player2_pos[1] + paddle_speed)

    # Fill the background with black for background
    screen.fill(black)

    # Calls function to create ball logic in game
    update_ball()

    # Draws both player and the ball to the screen
    draw_paddle(player1_pos)
    draw_paddle(player2_pos)
    draw_ball(ball_pos)

    # Creates the players scores text using the font class
    # Turn player_score int, into string with -> str(player_score)) *To use render, it must be a string
    # antialias is True to give letters a slight bend, then color of text
    player1_text = style.render(str(player1_score), True, white)
    player2_text = style.render(str(player2_score), True, white)
    winner1_text = style.render(str(winner1_message), True, white)
    winner2_text = style.render(str(winner2_message), True, white)

    # Puts Scores on screen starting at 0
    screen.blit(player1_text, (WIDTH/4, 20))
    screen.blit(player2_text, (WIDTH * 3 /4, 20))

    # Player 1's score updating logic
    if player1_score >= 5:
        # After 5 points, the screen displays the winner
        screen.blit(winner1_text, (WIDTH / 4 + 30, HEIGHT / 4))
        # Updates constantly to show the winner before game turns off
        pygame.display.update()
        # Delays and displays the player winner screen for 3 seconds
        pygame.time.delay(3000)
        # Game window closes
        bob = False

    # Player 2's score and logic
    elif player2_score >= 5:
        screen.blit(winner2_text, (WIDTH / 4 + 30, HEIGHT / 4))
        pygame.display.update()
        pygame.time.delay(3000)
        bob = False

    # Updates game every loop
    pygame.display.update()
    # Keeps time with FPS
    clock.tick(FPS)



