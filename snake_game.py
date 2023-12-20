import pygame
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
window_width = 1280
window_height = 1024
window = pygame.display.set_mode((window_width, window_height))
background = pygame.image.load('./background.png')
window_with_background = pygame.transform.scale(background, (window_width, window_height))

# Create a game loop
running = True

snake_block_1 = 64
snake_block_2 = 64
clock = pygame.time.Clock()
snake_speed = 5

font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont("comicasansms", 35)

def score_counter(score_1, score_2):
    value_1 = score_font.render("Score of player 1: " + str(score_1), True, red)
    value_2 = score_font.render("Score of player 2: " + str(score_2), True, blue)
    window.blit(value_1, [0,0])
    window.blit(value_2, [window_width - 600, 0])

def jedge_winner(score_1, score_2):
    font = pygame.font.Font(None, 36)
    text_1 = font.render("Win player 1", True, red)
    text_2 = font.render("Win player 2", True, red)
    text_3 = font.render("Draw", True, red)
    if score_1 > score_2:
        window.blit(text_1, [window_width / 2, window_height - 50])
    elif score_2 > score_1:
        window.blit(text_2, [window_width / 2, window_height - 50])
    else:
        window.blit(text_3, [window_width / 2, window_height - 50])

def snake_as_player_1(snake_block_1, snake_list_1):
    for x in snake_list_1:
        pygame.draw.rect(window, black, [x[0], x[1], snake_block_1, snake_block_1])

def snake_as_player_2(snake_block_2, snake_list_2):
    for x in snake_list_2:
        pygame.draw.rect(window, blue, [x[0], x[1], snake_block_2, snake_block_2])

def message(message, color):
    message = font_style.render(message, True, color)
    window.blit(message, [window_width / 6, window_height / 3])

def gameRunning():
    game_over = False
    game_close = False

    x1 = round(random.randrange(10, window_width - snake_block_1) / snake_block_1) * snake_block_1
    y1 = round(random.randrange(10, window_height - snake_block_1) / snake_block_1) * snake_block_1

    x2 = round(random.randrange(10, window_width - snake_block_2) / snake_block_2) * snake_block_2
    y2 = round(random.randrange(10, window_height - snake_block_2) / snake_block_2) * snake_block_2

    x1_change = 0
    y1_change = 0

    x2_change = 0
    y2_change = 0

    snake_list_1 = []
    snake_list_2 = []
    Length_of_snake1 = 1
    Length_of_snake2 = 1

    food_size =64
    foodx = round(random.randrange(10, window_width - food_size) / food_size) * food_size
    foody = round(random.randrange(10, window_height - food_size) / food_size) * food_size

    while not game_over:
        while game_close == True:
            message("You lost! Press Q-Quit or C-Play Again", red)
            score_counter(Length_of_snake1 - 1, Length_of_snake2 - 1)
            jedge_winner(Length_of_snake1 - 1, Length_of_snake2 - 1)
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
                pygame.quit()
            keys = pygame.key.get_pressed()
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
        if x1 < 0 or x1 >= window_width or y1 < 0 or y1 >= window_height:
            game_close = True
        if x2 < 0 or x2 >= window_width or y2 < 0 or y2 >= window_height:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        x2 += x2_change
        y2 += y2_change
        window.blit(window_with_background, (0, 0))
        pygame.draw.rect(window, red, [foodx, foody, snake_block_1, snake_block_1])
        snake_HEAD_1 = []
        snake_HEAD_1.append(x1)
        snake_HEAD_1.append(y1)
        snake_list_1.append(snake_HEAD_1)
        if len(snake_list_1) > Length_of_snake1:
            del snake_list_1[0]

        snake_HEAD_2 = []
        snake_HEAD_2.append(x2)
        snake_HEAD_2.append(y2)
        snake_list_2.append(snake_HEAD_2)
        if len(snake_list_2) > Length_of_snake2:
            del snake_list_2[0]

        for x in snake_list_1[:-1]:
            if x == snake_HEAD_1:
                game_close = True

        snake_as_player_1(snake_block_1, snake_list_1)
        snake_as_player_2(snake_block_2, snake_list_2)    

        score_counter(Length_of_snake1 - 1, Length_of_snake2 - 1)

        if (foodx >= x1 and foodx < x1 + snake_block_1 and foody >= y1 and foody < y1 + snake_block_1):
            foodx = round(random.randrange(0, window_width - snake_block_1) / 10.0) * 10.0
            foody = round(random.randrange(0, window_height - snake_block_1) / 10.0) * 10.0
            Length_of_snake1 += 1

        if (foodx >= x2 and foodx < x2 + snake_block_2 and foody >= y2 and foody < y2 + snake_block_2):
            foodx = round(random.randrange(0, window_width - snake_block_2) / 10.0) * 10.0
            foody = round(random.randrange(0, window_height - snake_block_2) / 10.0) * 10.0
            Length_of_snake2 += 1

        pygame.display.update()
        clock.tick(snake_speed)

    pygame.quit()

gameRunning()