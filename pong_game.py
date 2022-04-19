import pygame
import os

from pong_character import pong_character

# Game window constants
FPS = 60
WIDTH, HEIGHT = 1280, 720
GAME_WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
BORD_SIZE = 5
BORD_TOP = pygame.Rect(0, 0, WIDTH, BORD_SIZE)
BORD_LEFT = pygame.Rect(0, 0, BORD_SIZE, HEIGHT)
BORD_RIGHT = pygame.Rect(WIDTH - BORD_SIZE, 0, BORD_SIZE, HEIGHT)
BORD_BOT = pygame.Rect(0, HEIGHT - BORD_SIZE, WIDTH, BORD_SIZE)
pygame.display.set_caption("Hello Pong :)")


# Game assets for red character 
red_bar = pong_character(WIDTH, HEIGHT)
red_bar.image = pygame.image.load(
    os.path.join("Game_Assets", "red_pong_stick.png"))
red_bar.spawn = (WIDTH - (red_bar.width + BORD_SIZE), (HEIGHT - red_bar.height) / 2)
red_bar.move_speed = red_bar.height / 50

red_bar.resized_pong = pygame.transform.scale(red_bar.image, (red_bar.width, red_bar.height))

# Game assets for blue character
blue_bar = pong_character(WIDTH, HEIGHT)
blue_bar.image = pygame.image.load(
    os.path.join("Game_Assets", "blue_pong_stick.png"))
blue_bar.spawn = (BORD_SIZE, (HEIGHT - blue_bar.height) / 2)
blue_bar.move_speed = blue_bar.height / 50

blue_bar.resized_pong = pygame.transform.scale(blue_bar.image, (blue_bar.width, blue_bar.height))

# game assets for ball
BALL_SIDE = HEIGHT / 50
BALL_SPEED = 5 #BALL_SIDE
WHITE_BALL_IMAGE = pygame.image.load(os.path.join("Game_Assets", "white_ball.png"))
BLUE_BALL_IMAGE = pygame.image.load(os.path.join("Game_Assets", "blue_ball.png"))
RED_BALL_IMAGE = pygame.image.load(os.path.join("Game_Assets", "red_ball.png"))
ball = pygame.transform.scale(WHITE_BALL_IMAGE, (BALL_SIDE, BALL_SIDE))

# Color constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


def draw_game(red_hitbox, blue_hitbox, ball_hitbox, ball_color):
        GAME_WINDOW.fill(BLACK)
        pygame.draw.rect(GAME_WINDOW, WHITE, BORD_TOP)
        pygame.draw.rect(GAME_WINDOW, WHITE, BORD_BOT)
        pygame.draw.rect(GAME_WINDOW, WHITE, BORD_LEFT)
        pygame.draw.rect(GAME_WINDOW, WHITE, BORD_RIGHT)
        GAME_WINDOW.blit(red_bar.resized_pong, (red_hitbox.x, red_hitbox.y))
        GAME_WINDOW.blit(blue_bar.resized_pong, (blue_hitbox.x, blue_hitbox.y))

        if (ball_color == -1):
            current_ball = pygame.transform.scale(BLUE_BALL_IMAGE, (BALL_SIDE, BALL_SIDE))
        elif (ball_color == 1):
            current_ball = pygame.transform.scale(RED_BALL_IMAGE, (BALL_SIDE, BALL_SIDE))
        else:
            current_ball = pygame.transform.scale(WHITE_BALL_IMAGE, (BALL_SIDE, BALL_SIDE))

        GAME_WINDOW.blit(current_ball, (ball_hitbox.x, ball_hitbox.y))
        
        pygame.display.update()

# handles all movement for blue character
def blue_movement(keys_input, blue_character):
    # check if blue moving upwards and is within the border bounds
    if keys_input[pygame.K_w] and (blue_character.y - blue_bar.move_speed >= BORD_SIZE):
        blue_character.y -= blue_bar.move_speed
    # check if blue moving downwards and is within the border bounds
    elif keys_input[pygame.K_s] and (blue_character.y + blue_bar.move_speed < HEIGHT - BORD_SIZE - blue_bar.height):
        blue_character.y += blue_bar.move_speed

# handles all movement for red character 
def red_movement(keys_input, red_character):
    # check if red moving upwards and is within the border bounds
    if keys_input[pygame.K_UP] and (red_character.y - blue_bar.move_speed >= BORD_SIZE):
        red_character.y -= red_bar.move_speed
    # check if red moving downwards and is within the border bounds
    elif keys_input[pygame.K_DOWN] and (red_character.y + blue_bar.move_speed < HEIGHT - BORD_SIZE - red_bar.height):
        red_character.y += red_bar.move_speed

def ball_move(ball_hitbox, ball_direction, ball_col, blue_character, red_character):
    # check if the ball collided with the left or right border
    if ball_hitbox.colliderect(BORD_LEFT) or ball_hitbox.colliderect(BORD_RIGHT):
        ball_direction[0] *= -1

    # check if ball collided with the top or bottom border
    if ball_hitbox.colliderect(BORD_TOP) or ball_hitbox.colliderect(BORD_BOT):
        ball_direction[1] *= -1
    
    # check if the blue character collided with the ball
    if ball_hitbox.colliderect(blue_character):
        ball_direction[0] *= -1
        ball_col = -1
        
    # check if the red character collided with the ball
    elif ball_hitbox.colliderect(red_character):
        ball_direction[0] *= -1
        ball_col = 1

    ball_hitbox.y += ball_direction[1] * BALL_SPEED
    ball_hitbox.x += ball_direction[0] * BALL_SPEED

    return ball_col


def main():
    # initialize hitboxes for red and blue characters
    red_pong_hb = pygame.Rect(red_bar.spawn[0], red_bar.spawn[1], red_bar.width, red_bar.height)
    blue_pong_hb = pygame.Rect(blue_bar.spawn[0], blue_bar.spawn[1], blue_bar.width, blue_bar.height)
    ball_hb = pygame.Rect(WIDTH / 2 , HEIGHT / 2, BALL_SIDE, BALL_SIDE)
    ball_direc = [-1, -1] # (horizontal, vertical)
    ball_color = 0 # (ball color: -1 = blue, 0 = white, 1 = red)

    # start a clock that will help maintain the FPS
    game_clock = pygame.time.Clock()

    game_running = True

    while (game_running):
        game_clock.tick(FPS) # locks fps to 60

        # loop through all current events
        for event in pygame.event.get():
            # checks if the user quit the game already
            if (event.type == pygame.QUIT):
                game_running = False

        # get all keys being pressed
        keys_input = pygame.key.get_pressed()

        # move blue if needed
        blue_movement(keys_input, blue_pong_hb)
        # move red if needed
        red_movement(keys_input, red_pong_hb)

        # ball movement
        ball_color = ball_move(ball_hb, ball_direc, ball_color, blue_pong_hb, red_pong_hb)  
        # draw the game board each loop
        draw_game(red_pong_hb, blue_pong_hb, ball_hb, ball_color)

    
    pygame.quit()
    return None

if __name__ == "__main__":
    main()