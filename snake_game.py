import pygame
import time
import random

# Initialize Pygame
pygame.init()

blue = (0,0,255)
black = (0, 0, 0)
red = (255,0,0)
white = (255,255,255)
# Set the window title
pygame.display.set_caption("Snake Game")

# Set the window size
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))

# Create a game loop
running = True

snake_block_1 = 10
snake_block_2 = 20
clock = pygame.time.Clock()
snake_speed = 5

font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont("comicasansms", 35)

def score(score):
    value = score_font.render("Score of player 1: " + str(score), True, red)
    window.blit(value, [0,0])

def snake_as_player_1(snake_block_1, snake_list_1):
    for x in snake_list_1:
        pygame.draw.rect(window, black, [x[0], x[1], snake_block_1, snake_block_1])
        print("snake_list_1")
def snake_as_player_2(snake_block_2, snake_list_2):
    for x in snake_list_2:
        pygame.draw.rect(window, blue, [x[0], x[1], snake_block_2, snake_block_2])
        # print(snake_list_2)
def message(message, color):
    message = font_style.render(message, True, color)
    window.blit(message, [window_width/2, window_height/2])

def gameRunning():
    game_over = False
    game_close = False

    x1 = window_width/2
    y1 = window_height/2

    x2 = 300
    y2 = 300

    x1_change = 0
    y1_change = 0

    x2_change = 0
    y2_change = 0

    snake_list_1 = []
    snake_list_2 = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, window_width - snake_block_1) / 10.0) * 10.0
    foody = round(random.randrange(0, window_width - snake_block_1) / 10.0) * 10.0

    while not game_over:
        # Handle events
        while game_close == True:
            window.fill(white)
            message("You lost! Press Q-Quit or C-Play Again", red)
            score(Length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameRunning()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            keys = pygame.key.get_pressed()
            # if event.type == pygame.KEYDOWN:
            if keys[pygame.K_LEFT]:
                x1_change = -snake_block_1
                y1_change = 0
            if keys[pygame.K_RIGHT]:
                x1_change = snake_block_1
                y1_change = 0
            if keys[pygame.K_UP]:
                x1_change = 0
                y1_change = -snake_block_1
            if keys[pygame.K_DOWN]:
                x1_change = 0
                y1_change = snake_block_1
                # KEYS for Snake 2
            if keys[pygame.K_a]:
                x2_change = -snake_block_2
                y2_change = 0
            if keys[pygame.K_d]:
                x2_change = snake_block_2
                y2_change = 0
            if keys[pygame.K_w]:
                x2_change = 0
                y2_change = -snake_block_2
            if keys[pygame.K_s]:
                x2_change = 0
                y2_change = snake_block_2
                
        if x1 < 0 or x1 > 750 or y1 < 50 or y1 > 550:
            game_close = True
        if x2 < 0 or x2 > 750 or y2 < 50 or y2 > 550:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        x2 += x2_change
        y2 += y2_change
        window.fill(white)
        # Handle additional input
        pygame.draw.rect(window, black, [foodx, foody, snake_block_1, snake_block_1])
        snake_HEAD_1 = []
        snake_HEAD_1.append(x1)
        snake_HEAD_1.append(y1)
        snake_list_1.append(snake_HEAD_1)
        if len(snake_list_1) > Length_of_snake:
            del snake_list_1[0]

        snake_HEAD_2 = []
        snake_HEAD_2.append(x2)
        snake_HEAD_2.append(y2)
        snake_list_2.append(snake_HEAD_2)
        if len(snake_list_2) > Length_of_snake:
            del snake_list_2[0]

        for x in snake_list_1[:-1]:
            if x == snake_HEAD_1:
                game_close = True

        snake_as_player_1(snake_block_1, snake_list_1)        
        snake_as_player_2(snake_block_2, snake_list_2)

        score(Length_of_snake - 1)
        # pygame.draw.rect(window, black, [x1,y1,snake_block_1,snake_block_1])
        # pygame.draw.rect(window, blue, [x1,y1,snake_block_2,snake_block_2])
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, window_width - snake_block_1) / 10.0) * 10.0
            foody = round(random.randrange(0, window_height - snake_block_1) / 10.0) * 10.0
            Length_of_snake += 1
            print("Yummy!!")
        # else:
        #     if len(snake_list_1) > Length_of_snake:
        #         del snake_list_1[0]

        clock.tick(snake_speed)
        
    # Quit Pygame
    pygame.quit()

gameRunning()
