import pygame
pygame.init()
import sys
from random import randint
import time
pygame.font.init()
# Constant variables
FPS = 60
WIDTH = 800
HEIGHT = 600

# Game Settings
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RETRO PONG 84'")
clock = pygame.time.Clock()

# Game Colors
black = (0, 0, 0)
white = (255, 255, 255)

# Game Variables
paddle_height = 100
paddle_width = 15
paddle_speed = 10

###################
player = ["PLayer 1", "Player 2"]
winner1_message = f"Player 1 is the winner!"
winner2_message = f"Player 2 is the winner!"
####################
player1_pos = [50, (HEIGHT - paddle_height)/2]
player2_pos = [WIDTH - 50 - paddle_width, (HEIGHT - paddle_height)/2]

ball_pos = [(WIDTH/2), (HEIGHT/2)]
ball_speed = [7,7]


##################################################

# Game Functions

# Make a Paddle
def draw_paddle(pos):
    pygame.draw.rect(screen, white, (pos[0], pos[1], paddle_width, paddle_height))

# Make a Ball
def draw_ball(pos):
    pygame.draw.circle(screen, white, pos, 15)

# Update the ball
# ball_pos = [(WIDTH/2), (HEIGHT/2)]
# ball_speed = [7,7]

def update_ball():
    global ball_pos, ball_speed, player1_score, player2_score

    ball_pos[0] += ball_speed[0]
    ball_pos[1] += ball_speed[1]

    # Bounce ball off top and bottom, ball logic
    if ball_pos[1] <= 10 or ball_pos[1] >= HEIGHT - 10:
        ball_speed[1] = -ball_speed[1]

    elif ball_pos[0] < player1_pos[0] + paddle_width and player1_pos[1] <= ball_pos[1] <= player1_pos[1] + paddle_height:
        ball_speed[0] = -ball_speed[0]

    elif ball_pos[0] >= player2_pos[0] and player2_pos[1] <= ball_pos[1] <= player2_pos[1] + paddle_height:
        ball_speed[0] = -ball_speed[0]

    # Player Scores
    if ball_pos[0] <= 0:
        player2_score += 1
        # Calling reset function
        reset()

    if ball_pos[0] >= WIDTH:
        player1_score += 1
        reset()

def reset():
    global ball_pos, ball_speed
    ball_pos = [(WIDTH / 2), (HEIGHT / 2)]
    num = randint(0, 1)
    if num == 0:
        ball_speed = [-7, -7]
    else:
        ball_speed = [7, 7]





# Scores and Font
player1_score = 0
player2_score = 0
style = pygame.font.Font(None, 45)

# Main Game Loop
bob = True
while bob:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    # Program the players
    keys = pygame.key.get_pressed()
    # Player 1 Controls
    if keys[pygame.K_w] and player1_pos[1] > 0:
        player1_pos = (player1_pos[0], player1_pos[1] - paddle_speed)

    elif keys[pygame.K_s] and player1_pos[1] < HEIGHT - paddle_height:
        player1_pos = (player1_pos[0], player1_pos[1] + paddle_speed)

    # Player 2 Controls
    if keys[pygame.K_UP] and player2_pos[1] > 0:
        player2_pos = (player2_pos[0], player2_pos[1] - paddle_speed)
    elif keys[pygame.K_DOWN] and player2_pos[1] < HEIGHT - paddle_height:
        player2_pos = (player2_pos[0], player2_pos[1] + paddle_speed)



    screen.fill(black)

    update_ball()

    draw_paddle(player1_pos)
    draw_paddle(player2_pos)
    draw_ball(ball_pos)



#player = ["PLayer 1", "Player 2"]
#winner1_message = f"Player 1 is the winner!"
#winner2_message = f"Player 2 is the winner!"


    # Player Scores
    player1_text = style.render(str(player1_score), True, white)
    player2_text = style.render(str(player2_score), True, white)
    winner1_text = style.render(str(winner1_message), True, white)
    winner2_text = style.render(str(winner2_message), True, white)

    # Puts Scores on screen
    screen.blit(player1_text, (WIDTH/4, 20))
    screen.blit(player2_text, (WIDTH * 3 /4, 20))

    if player1_score >= 5:
        screen.blit(winner1_text, (WIDTH / 4 + 30, HEIGHT / 4))  # Paints the text
        pygame.display.update()  # PULLS THE CURTAIN BACK
        pygame.time.delay(3000)  # Pauses for 3000 milliseconds (3 seconds)
        bob = False
    elif player2_score >= 5:
        screen.blit(winner2_text, (WIDTH / 4 + 30, HEIGHT / 4))
        pygame.display.update()
        pygame.time.delay(3000)
        bob = False



    pygame.display.update()
    clock.tick(FPS)



