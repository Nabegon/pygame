import pygame
import random

GRID_WIDTH = 20
GRID_HEIGHT = 16
TILE_SIZE = 64

WINDOW_WIDTH = GRID_WIDTH * TILE_SIZE
WINDOW_HEIGHT = GRID_HEIGHT * TILE_SIZE

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        return False

class Food:
    def __init__(self):
        self.position = Position(random.randrange(GRID_WIDTH), random.randrange(GRID_HEIGHT))
        self.surface_food = pygame.image.load('./battery.png')
    
    def calculate_randam_position(self):
        self.position = Position(random.randrange(GRID_WIDTH), random.randrange(GRID_HEIGHT))

    def draw(self, window):
        window.blit(self.surface_food, (self.position.x * TILE_SIZE, self.position.y * TILE_SIZE))
    
class BodyPart:
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction
        

class Snake:
    def __init__(self, alternative_color):
        # self.direction = random.randrange(4) # 0 -> up, 1 -> right, 2 -> down, 3 -> left
        direction = random.randrange(4) # 0 -> up, 1 -> right, 2 -> down, 3 -> left
        start_x = random.randrange(3, GRID_WIDTH - 3)
        start_y = random.randrange(3, GRID_HEIGHT - 3)
        initial_position = Position(start_x, start_y)


        # set the fields of the snake with their positions
        self.fields = [BodyPart(initial_position, direction)]
        match direction:
            case 0:
                self.fields.append(BodyPart(Position(initial_position.x, initial_position.y + 1), direction))
                self.fields.append(BodyPart(Position(initial_position.x, initial_position.y + 2), direction))
            case 1:
                self.fields.append(BodyPart(Position(initial_position.x - 1, initial_position.y), direction))
                self.fields.append(BodyPart(Position(initial_position.x - 2, initial_position.y), direction))
            case 2:
                self.fields.append(BodyPart(Position(initial_position.x, initial_position.y - 1), direction))
                self.fields.append(BodyPart(Position(initial_position.x, initial_position.y - 2), direction))
            case 3:
                self.fields.append(BodyPart(Position(initial_position.x + 1, initial_position.y), direction))
                self.fields.append(BodyPart(Position(initial_position.x + 2, initial_position.y), direction))
        
        # load graphics
        if alternative_color:
            self.surface_head = pygame.image.load('./p1_head.png')
            self.surface_straight = pygame.image.load('./p1_straight.png')
            self.surface_curve = pygame.image.load('./p1_curve.png')
            self.surface_tail = pygame.image.load('./p1_tail.png')
        else:
            self.surface_head = pygame.image.load('./p2_head.png')
            self.surface_straight = pygame.image.load('./p2_straight.png')
            self.surface_curve = pygame.image.load('./p2_curve.png')
            self.surface_tail = pygame.image.load('./p2_tail.png')
    
    def advance(self, food, other_snake):
        head = self.fields[0]
        match head.direction:
            case 0:
                next_position = Position(head.position.x, head.position.y - 1)
            case 1:
                next_position = Position(head.position.x + 1, head.position.y)
            case 2:
                next_position = Position(head.position.x, head.position.y + 1)
            case 3:
                next_position = Position(head.position.x - 1, head.position.y)

        if next_position.x < 0 or next_position.x > GRID_WIDTH  - 1 or next_position.y < 0 or next_position.y > GRID_HEIGHT - 1:
            return False
        
        for i in other_snake.fields:
            if next_position == i.position:
                return False

        if not (next_position == food.position):
            self.fields.pop(len(self.fields) - 1)
        else:
            food.calculate_randam_position()

        self.fields.insert(0, BodyPart(next_position, head.direction))

    def draw(self, window):
        for i in range(len(self.fields)):
            current_bodypart = self.fields[i]
            if i == 0:
                match self.fields[0].direction:
                    case 0:
                        rotated_head = pygame.transform.rotate(self.surface_head, 270)
                    case 1:
                        rotated_head = pygame.transform.rotate(self.surface_head, 180)
                    case 2:
                        rotated_head = pygame.transform.rotate(self.surface_head, 90)
                    case 3:
                        rotated_head = self.surface_head
                window.blit(rotated_head, (current_bodypart.position.x * TILE_SIZE, current_bodypart.position.y * TILE_SIZE))

            elif i == len(self.fields) - 1:
                match current_bodypart.direction:
                    case 0:
                        rotated_body = pygame.transform.rotate(self.surface_tail, 270)
                    case 1:
                        rotated_body = pygame.transform.rotate(self.surface_tail, 180)
                    case 2:
                        rotated_body = pygame.transform.rotate(self.surface_tail, 90)
                    case 3:
                        rotated_body = self.surface_tail
                window.blit(rotated_body, (current_bodypart.position.x * TILE_SIZE, current_bodypart.position.y * TILE_SIZE))
                

            else:
                current_direction = current_bodypart.direction
                following_bodypart = self.fields[i + 1]
                follwoing_direction = following_bodypart.direction

                match current_direction:
                    case 0:
                        match follwoing_direction:
                            case 0:
                                rotated_body = self.surface_straight
                            case 1:
                                rotated_body = pygame.transform.rotate(self.surface_curve, 270)
                            case 3:
                                rotated_body = pygame.transform.rotate(pygame.transform.flip(self.surface_curve, True, False), 90)
                    case 1:
                        match follwoing_direction:
                            case 0:
                                rotated_body = pygame.transform.flip(self.surface_curve, True, False)
                            case 1:
                                rotated_body = pygame.transform.rotate(self.surface_straight, 270)
                            case 2:
                                rotated_body = pygame.transform.rotate(self.surface_curve, 180)

                    case 2:
                        match follwoing_direction:
                            case 1:
                                rotated_body = pygame.transform.rotate(pygame.transform.flip(self.surface_curve, False, True), 90)
                            case 2:
                                rotated_body = pygame.transform.flip(self.surface_straight, False, True)
                            case 3:
                                rotated_body = pygame.transform.rotate(self.surface_curve, 90)
                    case 3:
                        match follwoing_direction:
                            case 0:
                                rotated_body = self.surface_curve
                            case 2:
                                rotated_body = pygame.transform.flip(self.surface_curve, False, True)
                            case 3:
                                rotated_body = pygame.transform.rotate(self.surface_straight, 90)

                window.blit(rotated_body, (current_bodypart.position.x * TILE_SIZE, current_bodypart.position.y * TILE_SIZE))

    def change_direction(self, direction):
        #print(self.fields[0].direction)
        # if direction == 0
        if direction == 2 and self.fields[0].direction == 0:
            return
        elif direction == 3 and self.fields[0].direction == 1:
            return
        elif direction == 0 and self.fields[0].direction == 2:
            return
        elif direction == 1 and self.fields[0].direction == 3:
            return

        self.fields[0].direction = direction



# Initialize Pygame
pygame.init()

white = 255, 255, 255, 255

# Set the window title
pygame.display.set_caption("Snake Game")

# Set the window size etc.
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
background = pygame.image.load('./background.png')
window_with_background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))

# Create a game loop
running = True

# speed of the snake
clock = pygame.time.Clock()
snake_speed = 2

# font. after we use grafik, just delete here
font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont("comicasansms", 35)

# def score_counter(score_1, score_2):
#     value_1 = score_font.render("Score of player 1: " + str(score_1), True, red)
#     value_2 = score_font.render("Score of player 2: " + str(score_2), True, blue)
#     window.blit(value_1, [0,0])
#     window.blit(value_2, [window_width - 600, 0])

# def jedge_winner(score_1, score_2):
#     font = pygame.font.Font(None, 36)
#     text_1 = font.render("Win player 1", True, red)
#     text_2 = font.render("Win player 2", True, red)
#     text_3 = font.render("Draw", True, red)
#     if score_1 > score_2:
#         window.blit(text_1, [window_width / 2, window_height - 50])
#     elif score_2 > score_1:
#         window.blit(text_2, [window_width / 2, window_height - 50])
#     else:
#         window.blit(text_3, [window_width / 2, window_height - 50])

def message(message, color):
    message = font_style.render(message, True, color)
    window.blit(message, [WINDOW_HEIGHT / 6, WINDOW_HEIGHT / 3])

def gameRunning():
    game_over = False
    game_close = False

    player_1 = Snake(True)
    player_2 = Snake(False)
    food = Food()

    while not game_over:
        while game_close == True:
            message("You lost! Press Q-Quit or C-Play Again", white)
            # score_counter(Length_of_snake1 - 1, Length_of_snake2 - 1)
            # jedge_winner(Length_of_snake1 - 1, Length_of_snake2 - 1)
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
            if keys[pygame.K_UP]:
                player_1.change_direction(0)
            if keys[pygame.K_RIGHT]:
                player_1.change_direction(1)
            if keys[pygame.K_DOWN]:
                player_1.change_direction(2)
            if keys[pygame.K_LEFT]:
                player_1.change_direction(3)

            if keys[pygame.K_a]:
                player_2.change_direction(3)
            if keys[pygame.K_d]:
                player_2.change_direction(1)
            if keys[pygame.K_w]:
                player_2.change_direction(0)
            if keys[pygame.K_s]:
                player_2.change_direction(2)

        # score_counter(Length_of_snake1 - 1, Length_of_snake2 - 1)

        # if (foodx >= x1 and foodx < x1 + snake_block_1 and foody >= y1 and foody < y1 + snake_block_1):
        #     foodx = round(random.randrange(0, window_width - snake_block_1) / 10.0) * 10.0
        #     foody = round(random.randrange(0, window_height - snake_block_1) / 10.0) * 10.0
        #     Length_of_snake1 += 1

        # if (foodx >= x2 and foodx < x2 + snake_block_2 and foody >= y2 and foody < y2 + snake_block_2):
        #     foodx = round(random.randrange(0, window_width - snake_block_2) / 10.0) * 10.0
        #     foody = round(random.randrange(0, window_height - snake_block_2) / 10.0) * 10.0
        #     Length_of_snake2 += 1
        window.blit(window_with_background, (0, 0))
        food.draw(window)
        if player_1.advance(food, player_2) == False:
            game_close = True
        player_1.draw(window)
        if player_2.advance(food, player_1) == False:
            game_close = True
        player_2.draw(window)
        pygame.display.update()
        clock.tick(snake_speed)

    pygame.quit()

gameRunning()
