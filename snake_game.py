import pygame
import random

# UP = 0
# RIGHT = 1
# DOWN = 2
# LEFT = 3

# GAME_INIT = 0
# GAME_RUNNING = 1
# GAME_OVER = 2
# GAME_CLOSE = 3

GRID_WIDTH = 20
GRID_HEIGHT = 16
TILE_SIZE = 64

WINDOW_WIDTH = GRID_WIDTH * TILE_SIZE
WINDOW_HEIGHT = GRID_HEIGHT * TILE_SIZE

SNAKE_SPEED = 350
INCREASED_SNAKE_SPEED = 150
SPEED_UP_PERIOD = 3000
SPEED_UP_COOLDOWN = 10000

OBSTACLE_AMOUNT = 10

CHANGE_ANIMATION_POINT = 250

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        return False


class Playground:
    def __init__(self):
        self.grid = []
        for i in range(GRID_HEIGHT):
            self.grid.append([])
            for j in range(GRID_WIDTH):
                self.grid[i].append(False)

    def is_occupied(self, position):
        return self.grid[position.y][position.x]
    
    def set_field(self, position):
        self.grid[position.y][position.x] = True

    def reset_field(self, position):
        self.grid[position.y][position.x] = False


class Food:
    def __init__(self):
        global playground

        # randomly place the food
        random_position = Position(random.randrange(GRID_WIDTH), random.randrange(GRID_HEIGHT))
        while playground.is_occupied(random_position):
            random_position = Position(random.randrange(GRID_WIDTH), random.randrange(GRID_HEIGHT))
        playground.set_field(random_position)
        self.position = random_position

        self.surface_0 = pygame.image.load('./battery_0.png')
        self.surface_1 = pygame.image.load('./battery_1.png')
        self.surface_2 = pygame.image.load('./battery_2.png')
        self.animation_step = 0 # 0 - 3
        self.time_delta = 0


    def advance(self, time_delta):
        self.time_delta += time_delta
        if self.time_delta >= CHANGE_ANIMATION_POINT:
            if self.animation_step == 3:
                self.animation_step = 0
            else:
                self.animation_step += 1            
            self.time_delta = self.time_delta - CHANGE_ANIMATION_POINT

    def draw(self, window):
        match self.animation_step:
            case 0:
                surface_food = self.surface_0
            case 1:
                surface_food = self.surface_1
            case 2:
                surface_food = self.surface_2
            case 3:
                surface_food = self.surface_1      
        window.blit(surface_food, (self.position.x * TILE_SIZE, self.position.y * TILE_SIZE))

    
class BodyPart:
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction
        

class Snake:
    def __init__(self, alternative_color):
        global playground

        collision = True

        while collision:
            collision = False

            self.direction = random.randrange(4)
            start_x = random.randrange(3, GRID_WIDTH - 3)
            start_y = random.randrange(3, GRID_HEIGHT - 3)
            initial_position = Position(start_x, start_y)

            # set the fields of the snake with their positions
            self.fields = [BodyPart(initial_position, self.direction)]
            match self.direction:
                case 0:
                    self.fields.append(BodyPart(Position(initial_position.x, initial_position.y + 1), self.direction))
                    self.fields.append(BodyPart(Position(initial_position.x, initial_position.y + 2), self.direction))
                case 1:
                    self.fields.append(BodyPart(Position(initial_position.x - 1, initial_position.y), self.direction))
                    self.fields.append(BodyPart(Position(initial_position.x - 2, initial_position.y), self.direction))
                case 2:
                    self.fields.append(BodyPart(Position(initial_position.x, initial_position.y - 1), self.direction))
                    self.fields.append(BodyPart(Position(initial_position.x, initial_position.y - 2), self.direction))
                case 3:
                    self.fields.append(BodyPart(Position(initial_position.x + 1, initial_position.y), self.direction))
                    self.fields.append(BodyPart(Position(initial_position.x + 2, initial_position.y), self.direction))
        
        # check if snake overlaps
        for bodypart in self.fields:
            if playground.is_occupied(bodypart.position):
                self.fields.clear()
                collision = True

        # mark the location of the snake on the playground
        if collision == False:
            for bodypart in self.fields:
                playground.set_field(bodypart.position)

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
        
        # used in advance(); tracks time since the snake moved
        self.time_delta = 0

        # tracks the status of the speedup ability
        self.speed_up = 0



    def speed_up_activate(self):
        if self.speed_up <= 0 - SPEED_UP_COOLDOWN:
            self.speed_up = SPEED_UP_PERIOD
    
    def advance(self, time_delta):
        global playground
        global food

        self.time_delta += time_delta

        if self.speed_up > 0:
            # speed up active
            speed = INCREASED_SNAKE_SPEED
            self.speed_up = self.speed_up - time_delta
        elif self.speed_up < 0 - SPEED_UP_COOLDOWN:
            # speedup available but inactive
            speed = SNAKE_SPEED
        else:
            # speedup cooldown
            speed = SNAKE_SPEED
            self.speed_up = self.speed_up - time_delta

        if self.time_delta >= speed:
            self.time_delta = self.time_delta - speed

            # get direction of head and determine its next position
            self.fields[0].direction = self.direction
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

            if playground.is_occupied(next_position):
                if next_position == food.position:
                    food = Food()
                else:
                    return False
            else:
                playground.reset_field(self.fields[len(self.fields) - 1].position)
                self.fields.pop(len(self.fields) - 1)

            playground.set_field(next_position)
            self.fields.insert(0, BodyPart(next_position, head.direction))


    def draw(self, window):

        # iterate through all body parts
        for i in range(len(self.fields)):
            current_bodypart = self.fields[i]
            if i == 0:
                # draw head
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
                # draw tail
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
                # draw body (straight and curved)
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

        # prevent illegal movements
        if direction == 2 and self.fields[0].direction == 0:
            return
        elif direction == 3 and self.fields[0].direction == 1:
            return
        elif direction == 0 and self.fields[0].direction == 2:
            return
        elif direction == 1 and self.fields[0].direction == 3:
            return
        
        self.direction = direction


def draw_obstacles(obstacle_list, obstacle_surface):
    for o in obstacle_list:
        window.blit(obstacle_surface, (o.x * TILE_SIZE, o.y * TILE_SIZE))


def message(window, message, color):
    message = pygame.font.SysFont(None, 50).render(message, True, color)
    x_pos = WINDOW_WIDTH / 2 - game_over_surface.get_width() / 2 
    y_pos = WINDOW_HEIGHT / 2 - game_over_surface.get_height() / 2
    window.blit(message, (x_pos, y_pos))


def start_game():
    global game_state
    global playground
    global player_1
    global player_2
    global food
    global obstacles
    global window
    global game_winner_1

    playground = Playground()
    player_1 = Snake(True)
    player_2 = Snake(False)

    # place obstacles
    obstacles.clear()
    for i in range(OBSTACLE_AMOUNT):
        random_position = Position(random.randrange(GRID_WIDTH), random.randrange(GRID_HEIGHT))
        while playground.is_occupied(random_position):
            random_position = Position(random.randrange(GRID_WIDTH), random.randrange(GRID_HEIGHT))
        playground.set_field(random_position)
        obstacles.append(random_position)

    food = Food()
    game_state = 1


# Initialize Pygame
pygame.init()

white = 255, 255, 255, 255

# Set the window title
pygame.display.set_caption("Snake Game")

# Load images
background = pygame.image.load('./background.png')
game_over_surface = pygame.image.load('./gameover.png')
title_surface = pygame.image.load('./title.png')
obstacle_surface = pygame.image.load('./obstacle.png')

# Set the window size etc.
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
window_with_background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))

playground = Playground()

obstacles = []

player_1 = Snake(True)
player_2 = Snake(False)
food = Food()
game_winner_1 = False

# speed of the snake
clock = pygame.time.Clock()
time_delta = 0


game_state = 0
pygame.mixer.music.load('./bgmusic.mp3')
pygame.mixer.music.play()

def game_init():
    global game_state

    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                game_state = 3
            case pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    game_state = 3
                else:
                    start_game()

    window.blit(window_with_background, (0, 0))
    y_pos = WINDOW_HEIGHT / 2 - title_surface.get_height() / 2
    window.blit(title_surface, (0, y_pos))

def game_running():
    global game_state
    global player_1
    global player_2
    global food
    global window
    global game_winner_1

    # check input and change state accordingly
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                game_state = 3
            case pygame.KEYDOWN:
                match event.key:
                    case pygame.K_q:
                            game_state = 3
                    case pygame.K_UP:
                        player_1.change_direction(0)
                    case pygame.K_RIGHT:
                        player_1.change_direction(1)
                    case pygame.K_DOWN:
                        player_1.change_direction(2)
                    case pygame.K_LEFT:
                        player_1.change_direction(3)
                    case pygame.K_RSHIFT:
                        player_1.speed_up_activate()
                    case pygame.K_w:
                        player_2.change_direction(0)
                    case pygame.K_d:
                        player_2.change_direction(1)
                    case pygame.K_s:
                        player_2.change_direction(2)
                    case pygame.K_a:
                        player_2.change_direction(3)
                    case pygame.K_e:
                        player_2.speed_up_activate()

    # advance snakes
    if player_1.advance(time_delta) == False:
        game_winner_1 = False
        game_state = 2
    if player_2.advance(time_delta) == False:
        game_winner_1 = True
        game_state = 2
    food.advance(time_delta)

    # draw frame
    window.blit(window_with_background, (0, 0))
    food.draw(window)
    player_1.draw(window)
    player_2.draw(window)
    draw_obstacles(obstacles, obstacle_surface)

def game_over():
    global game_state
    global player_1
    global player_2
    global food
    
    # check input and change state accordingly
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                game_state = 3
            case pygame.KEYDOWN:
                match event.key:
                    case pygame.K_q:
                        game_state = 3
                    case pygame.K_c:
                        start_game()
    
    # draw frame
    x_pos = WINDOW_WIDTH / 2 - game_over_surface.get_width() / 2 
    y_pos = WINDOW_HEIGHT / 2 - game_over_surface.get_height() / 2 
    window.blit(game_over_surface, (x_pos, y_pos))
    if game_winner_1:
        message(window, "Player 1 won the game! Press Q-Quit or C-Play Again", white)
    else:
        message(window, "Player 2 won the game! Press Q-Quit or C-Play Again", white)


# game loop
while game_state != 3:
    match game_state:
        case 0:
            game_init()
        case 1:
            game_running()
        case 2:
            game_over()
    pygame.display.update()
    time_delta = clock.tick(143)

pygame.mixer.music.stop()
pygame.quit()

# Shutdown Raspberry Pi
# os.system("sudo shutdown -h now")