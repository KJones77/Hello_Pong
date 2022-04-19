import pygame
import os

from pong_character import pong_character

# Color constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# General constants
pygame.init()
FPS = 60
WIDTH, HEIGHT = 1280, 720
GAME_WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
BORD_SIZE = 5
BORD_TOP = pygame.Rect(0, 0, WIDTH, BORD_SIZE)
BORD_LEFT = pygame.Rect(0, 0, BORD_SIZE, HEIGHT)
BORD_RIGHT = pygame.Rect(WIDTH - BORD_SIZE, 0, BORD_SIZE, HEIGHT)
BORD_BOT = pygame.Rect(0, HEIGHT - BORD_SIZE, WIDTH, BORD_SIZE)
pygame.display.set_caption("Hello Pong :)")
SCORE_FONT = pygame.font.Font("freesansbold.ttf", 32)
TITLE_FONT = pygame.font.Font("freesansbold.ttf", 64)


# Game assets for red character 
red_bar = pong_character(WIDTH, HEIGHT)
red_bar.image = pygame.image.load(
    os.path.join("Game_Assets", "red_pong_stick.png"))
red_bar.spawn = (WIDTH - (red_bar.width + BORD_SIZE), (HEIGHT - red_bar.height) // 2)
red_bar.move_speed = red_bar.height // 50
red_bar.resized_pong = pygame.transform.scale(red_bar.image, (red_bar.width, red_bar.height))
RED_SCORE_POS = (3 * WIDTH // 4, SCORE_FONT.get_height())

# Game assets for blue character
blue_bar = pong_character(WIDTH, HEIGHT)
blue_bar.image = pygame.image.load(
    os.path.join("Game_Assets", "blue_pong_stick.png"))
blue_bar.spawn = (BORD_SIZE, (HEIGHT - blue_bar.height) // 2)
blue_bar.move_speed = blue_bar.height // 50
blue_bar.resized_pong = pygame.transform.scale(blue_bar.image, (blue_bar.width, blue_bar.height))
BLUE_SCORE_POS = (WIDTH // 4, SCORE_FONT.get_height())


# game assets for ball
BALL_SIDE = HEIGHT // 50
BALL_SPEED = 5 #BALL_SIDE // 2
WHITE_BALL_IMAGE = pygame.image.load(os.path.join("Game_Assets", "white_ball.png"))
BLUE_BALL_IMAGE = pygame.image.load(os.path.join("Game_Assets", "blue_ball.png"))
RED_BALL_IMAGE = pygame.image.load(os.path.join("Game_Assets", "red_ball.png"))
ball = pygame.transform.scale(WHITE_BALL_IMAGE, (BALL_SIDE, BALL_SIDE))



# User events
BALL_HIT_RED = pygame.USEREVENT + 1
BALL_HIT_BLUE = pygame.USEREVENT + 2
BALL_RESET = pygame.USEREVENT + 3
RED_SCORED = pygame.USEREVENT + 4
BLUE_SCORED = pygame.USEREVENT + 5

"""
Helper function that draws all the objects we need on screen each loop

Input: red_hitbox = pygame rectangle representing red character's hitbox
       blue_hitbox = pygame rectangle representing blue character's hitbox
       ball_hitbox = pygame rectangle representing the ball's hitbox
       current_ball = a pygame image object representing the current state of the ball

Output: None
"""
def draw_game(red_hitbox, blue_hitbox, ball_hitbox, current_ball, red_score, blue_score):
        GAME_WINDOW.fill(BLACK)
        pygame.draw.rect(GAME_WINDOW, WHITE, BORD_TOP)
        pygame.draw.rect(GAME_WINDOW, WHITE, BORD_BOT)
        pygame.draw.rect(GAME_WINDOW, WHITE, BORD_LEFT)
        pygame.draw.rect(GAME_WINDOW, WHITE, BORD_RIGHT)
        

        red_score.get_rect().center = (RED_SCORE_POS)
        blue_score.get_rect().center = (BLUE_SCORE_POS)
        GAME_WINDOW.blit(red_score, RED_SCORE_POS)
        GAME_WINDOW.blit(blue_score, BLUE_SCORE_POS)

        GAME_WINDOW.blit(red_bar.resized_pong, (red_hitbox.x, red_hitbox.y))
        GAME_WINDOW.blit(blue_bar.resized_pong, (blue_hitbox.x, blue_hitbox.y))

        

        GAME_WINDOW.blit(current_ball, (ball_hitbox.x, ball_hitbox.y))
        
        pygame.display.update()


"""
Helper function that handles all blue character movement

Input: keys_input = all the keyboard inputs that are currently being pressed
       blue_character = the blue_character's hitbox rectangle object

Output: None
""" 
def blue_movement(keys_input, blue_character):
    # check if blue moving upwards and is within the border bounds
    if keys_input[pygame.K_w] and (blue_character.y - blue_bar.move_speed >= BORD_SIZE):
        blue_character.y -= blue_bar.move_speed
    # check if blue moving downwards and is within the border bounds
    elif keys_input[pygame.K_s] and (blue_character.y + blue_bar.move_speed < HEIGHT - BORD_SIZE - blue_bar.height):
        blue_character.y += blue_bar.move_speed

    return None

"""
Helper function that handles all red character movement
Input: keys_input = all the keyboard inputs that are currently being pressed
       red_character = the red_character's hitbox rectangle object
Output: None
""" 
def red_movement(keys_input, red_character):
    # check if red moving upwards and is within the border bounds
    if keys_input[pygame.K_UP] and (red_character.y - blue_bar.move_speed >= BORD_SIZE):
        red_character.y -= red_bar.move_speed
    # check if red moving downwards and is within the border bounds
    elif keys_input[pygame.K_DOWN] and (red_character.y + blue_bar.move_speed < HEIGHT - BORD_SIZE - red_bar.height):
        red_character.y += red_bar.move_speed

    return None

"""
A function that calculates the amount the ball will move and which directions the ball will move

Input: ball_hitbox = a pygame rectangle representing the ball's hitbox
       ball_direction = a 2 index list that will keep track of the current direction the ball 
                            is moving and switch it if the ball collides with an object
       blue_character = a pygame rectangle representing the blue character's hitbox 
       red_character = a pygame rectangle representing the red character's hitbox

Output: None
"""
def ball_move(ball_hitbox, ball_direction, blue_character, red_character):
    # check if the ball collided with the left or right border
    if ball_hitbox.colliderect(BORD_LEFT):
        ball_direction[0] *= -1
        pygame.event.post(pygame.event.Event(RED_SCORED))
    elif ball_hitbox.colliderect(BORD_RIGHT):
        ball_direction[0] *= -1
        pygame.event.post(pygame.event.Event(BLUE_SCORED))
        
        
    # check if ball collided with the top or bottom border
    if ball_hitbox.colliderect(BORD_TOP) or ball_hitbox.colliderect(BORD_BOT):
        ball_direction[1] *= -1
    
    # check if the blue character collided with the ball
    if ball_hitbox.colliderect(blue_character):
        ball_direction[0] *= -1
        pygame.event.post(pygame.event.Event(BALL_HIT_BLUE))
        
    # check if the red character collided with the ball
    elif ball_hitbox.colliderect(red_character):
        ball_direction[0] *= -1
        pygame.event.post(pygame.event.Event(BALL_HIT_RED))

    ball_hitbox.y += ball_direction[1] * BALL_SPEED
    ball_hitbox.x += ball_direction[0] * BALL_SPEED

    return None

"""
A helper function that draws the red wins screen when red wins
Input: red_score =  pygame font object that represents the red player's score
       blue_score = pygame font object that represents the blue player's score
"""
def draw_red_wins(red_score, blue_score):
    # draw background
    GAME_WINDOW.fill(BLACK)

    # draw red has won text
    red_win_msg = TITLE_FONT.render("RED HAS WON!", True, RED, BLACK)
    GAME_WINDOW.blit(red_win_msg, ((WIDTH // 2) - (red_win_msg.get_width() // 2), HEIGHT // 3))
    # draw blue and red scores
    GAME_WINDOW.blit(red_score, (3 * WIDTH // 4, 3 * HEIGHT // 4))
    GAME_WINDOW.blit(blue_score, (WIDTH // 4, 3 * HEIGHT // 4))
    pygame.display.update()



"""
A helper function that draws the red wins screen when red wins
Input: red_score =  pygame font object that represents the red player's score
       blue_score = pygame font object that represents the blue player's score
"""
def draw_blue_wins(red_score, blue_score):
    # draw background
    GAME_WINDOW.fill(BLACK)

    # draw blue has won text
    blue_win_msg = TITLE_FONT.render("BLUE HAS WON!", True, BLUE, BLACK)
    GAME_WINDOW.blit(blue_win_msg, ((WIDTH // 2) - (blue_win_msg.get_width() // 2), HEIGHT // 3))
    # draw blue and red scores
    GAME_WINDOW.blit(red_score, (3 * WIDTH // 4, 3 * HEIGHT // 4))
    GAME_WINDOW.blit(blue_score, (WIDTH // 4, 3 * HEIGHT // 4))
    pygame.display.update()


def main():
    # initialize hitboxes for red and blue characters
    red_pong_hb = pygame.Rect(red_bar.spawn[0], red_bar.spawn[1], red_bar.width, red_bar.height)
    blue_pong_hb = pygame.Rect(blue_bar.spawn[0], blue_bar.spawn[1], blue_bar.width, blue_bar.height)
    ball_hb = pygame.Rect(WIDTH // 2 , HEIGHT // 2, BALL_SIDE, BALL_SIDE)
    curr_ball = pygame.transform.scale(WHITE_BALL_IMAGE, (BALL_SIDE, BALL_SIDE))
    ball_direc = [-1, -1] # (horizontal, vertical)
    red_score_text = SCORE_FONT.render("0", True, RED, BLACK)
    blue_score_text = SCORE_FONT.render("0", True, BLUE, BLACK)
    is_winner = False


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
            
            if is_winner is False:
                if event.type == BALL_HIT_BLUE:
                    curr_ball = pygame.transform.scale(BLUE_BALL_IMAGE, (BALL_SIDE, BALL_SIDE))
                elif event.type == BALL_HIT_RED:
                    curr_ball = pygame.transform.scale(RED_BALL_IMAGE, (BALL_SIDE, BALL_SIDE))
                elif event.type == BALL_RESET:
                    curr_ball = pygame.transform.scale(WHITE_BALL_IMAGE, (BALL_SIDE, BALL_SIDE))
                
                # check if red or blue just scored
                if event.type == RED_SCORED:
                    red_bar.score += 1
                    red_score_text = SCORE_FONT.render(str(red_bar.score), True, RED, BLACK)
                elif event.type == BLUE_SCORED:
                    blue_bar.score += 1
                    blue_score_text = SCORE_FONT.render(str(blue_bar.score), True, BLUE, BLACK)


        # get all keys being pressed
        keys_input = pygame.key.get_pressed()
        if is_winner is False:
            # move blue if needed
            blue_movement(keys_input, blue_pong_hb)
            # move red if needed
            red_movement(keys_input, red_pong_hb)

            # ball movement
            ball_move(ball_hb, ball_direc, blue_pong_hb, red_pong_hb)  

        score_gap_red = red_bar.score - blue_bar.score
        score_gap_blue = blue_bar.score - red_bar.score
        if (score_gap_red > 1):
            draw_red_wins(red_score_text, blue_score_text)
            is_winner = True
        elif (score_gap_blue > 1):
            draw_blue_wins(red_score_text, blue_score_text)
            is_winner = True
        else:
            # draw the game board each loop
            draw_game(red_pong_hb, blue_pong_hb, ball_hb, curr_ball, red_score_text, blue_score_text)


    pygame.quit()
    return None

if __name__ == "__main__":
    main()