import pygame
import random
import math
import pandas as pd

try:
    df=pd.read_csv("data.csv")
except:
    df=pd.DataFrame(columns=['grid','score','move','max_score','max_tile'])

# Initialize Pygame
pygame.init()

# Constants
GRID_SIZE = 4
TILE_SIZE = 100
GRID_MARGIN = 22
MARGIN_AROUND_GRID = 50  # New margin around the entire grid
SCREEN_WIDTH = GRID_SIZE * (TILE_SIZE + GRID_MARGIN) - GRID_MARGIN + 2 * MARGIN_AROUND_GRID
SCREEN_HEIGHT = SCREEN_WIDTH + 100
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_SIZE = 36
color_mapping = {
    2: {'block': (173, 216, 230), 'text': (0, 0, 0)},  # Light blue
    4: {'block': (144, 238, 144), 'text': (0, 0, 0)},  # Light green
    8: {'block': (255, 165, 0), 'text': (0, 0, 0)},    # Orange
    16: {'block': (255, 223, 0), 'text': (0, 0, 0)},   # Yellow
    32: {'block': (138, 43, 226), 'text': (255, 255, 255)},  # Purple
    64: {'block': (255, 0, 0), 'text': (255, 255, 255)},     # Red
    128: {'block': (0, 0, 255), 'text': (255, 255, 255)},    # Blue
    256: {'block': (0, 128, 0), 'text': (255, 255, 255)},    # Green
    512: {'block': (255, 0, 255), 'text': (255, 255, 255)},  # Magenta
    1024: {'block': (255, 69, 0), 'text': (255, 255, 255)},  # Red-Orange
    2048: {'block': (255, 215, 0), 'text': (0, 0, 0)} ,       # Gold
    4096: {'block': (183,104,83), 'text': (0, 0, 0)}  ,      # Gold-Red
    8192: {'block': (255, 255, 255), 'text': (0, 0, 0)}        # White 
}

name="ANSHIK"
FONT_SIZE_NAME = 24
colour=WHITE
cursive=pygame.font.SysFont('comicsansms', FONT_SIZE_NAME)
text=cursive.render(name, True, colour)
text_rect=text.get_rect(right=SCREEN_WIDTH-10, bottom=SCREEN_HEIGHT-10)


def draw_rounded_square(surface, color, rect, radius):
    x, y, w, h = rect
    pygame.draw.rect(surface, color, rect)

    # Top-left corner
    pygame.draw.arc(surface, color, (x, y, radius * 2, radius * 2), math.pi, 3 * math.pi / 2)
    pygame.draw.line(surface, color, (x + radius, y), (x + w - radius, y))

    # Top-right corner
    pygame.draw.arc(surface, color, (x + w - 2 * radius, y, radius * 2, radius * 2), 3 * math.pi / 2, 0)
    pygame.draw.line(surface, color, (x + w, y + radius), (x + w, y + h - radius))

    # Bottom-right corner
    pygame.draw.arc(surface, color, (x + w - 2 * radius, y + h - 2 * radius, radius * 2, radius * 2), 0, math.pi / 2)
    pygame.draw.line(surface, color, (x + radius, y + h), (x + w - radius, y + h))

    # Bottom-left corner
    pygame.draw.arc(surface, color, (x, y + h - 2 * radius, radius * 2, radius * 2), math.pi / 2, math.pi)
    pygame.draw.line(surface, color, (x, y + radius), (x, y + h - radius))

# Function to draw the grid
def draw_grid(screen, grid):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] != 0:
                value=grid[row][col]
                block_color = color_mapping.get(value, {'block': (255, 255, 255)})['block']
                text_color = color_mapping.get(value, {'text': (0, 0, 0)})['text']
                pygame.draw.rect(screen, block_color, [col * (TILE_SIZE + GRID_MARGIN) + MARGIN_AROUND_GRID,
                                            row * (TILE_SIZE + GRID_MARGIN) + MARGIN_AROUND_GRID,
                                            TILE_SIZE, TILE_SIZE], border_radius=10)
                font = pygame.font.Font(None, FONT_SIZE)
                text = font.render(str(grid[row][col]), True, text_color)
                text_rect = text.get_rect(center=(col * (TILE_SIZE + GRID_MARGIN) + TILE_SIZE / 2 + MARGIN_AROUND_GRID,
                                                  row * (TILE_SIZE + GRID_MARGIN) + TILE_SIZE / 2 + MARGIN_AROUND_GRID))
                screen.blit(text, text_rect)

# Function to insert a new random tile (2 or 4) into the grid
def insert_tile(grid):
    empty_cells = [(row, col) for row in range(GRID_SIZE) for col in range(GRID_SIZE) if grid[row][col] == 0]
    if empty_cells:
        row, col = random.choice(empty_cells)
        grid[row][col] = random.choice([2,2,2,4])

# Function to merge tiles in a row or column
def merge(line):
    global score
    merged_line = []
    previous_tile = None
    for tile in line:
        if tile != 0:
            if previous_tile is None:
                previous_tile = tile
            elif previous_tile == tile:
                merged_line.append(2 * tile)
                score+=2*tile
                previous_tile = None
            else:
                merged_line.append(previous_tile)
                previous_tile = tile
    if previous_tile is not None:
        merged_line.append(previous_tile)
    return merged_line + [0] * (len(line) - len(merged_line))

# Function to move the grid in a given direction
def move_grid(grid, direction):
    grid_copy = [row[:] for row in grid]
    if direction == "left":
        grid[:] = [merge(row) for row in grid]
    elif direction == "right":
        grid[:] = [merge(row[::-1])[::-1] for row in grid]
    elif direction == "up":
        columns = [[grid[row][col] for row in range(GRID_SIZE)] for col in range(GRID_SIZE)]
        columns = [merge(col) for col in columns]
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                grid[row][col] = columns[col][row]
    elif direction == "down":
        columns = [[grid[row][col] for row in range(GRID_SIZE)] for col in range(GRID_SIZE)]
        columns = [merge(col[::-1])[::-1] for col in columns]
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                grid[row][col] = columns[col][row]
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col]!=grid_copy[row][col]:
                return True
    return False

# Function to check if the game is over
def is_game_over():
    global grid
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] == 0:
                return False
            if col < GRID_SIZE - 1 and grid[row][col] == grid[row][col + 1]:
                return False
            if row < GRID_SIZE - 1 and grid[row][col] == grid[row + 1][col]:
                return False
    return True

# Function to check if the player has won
def is_game_won(grid):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] == 8192:
                return True
    return False

# Function to display the game over message
def game_over_message(screen):
    font = pygame.font.Font(None, 2 * FONT_SIZE)
    text = font.render("Game Over!", True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_WIDTH / 2 - FONT_SIZE))
    screen.blit(text, text_rect)
    font = pygame.font.Font(None, FONT_SIZE)
    text = font.render("Press R to restart", True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_WIDTH / 2 + FONT_SIZE))
    screen.blit(text, text_rect)

# Function to display the game won message
def game_won_message(screen):
    font = pygame.font.Font(None, 2 * FONT_SIZE)
    text = font.render("You Win!", True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_WIDTH / 2 - FONT_SIZE))
    screen.blit(text, text_rect)
    font = pygame.font.Font(None, FONT_SIZE)
    text = font.render("Press R to restart", True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_WIDTH / 2 + FONT_SIZE))
    screen.blit(text, text_rect)

# Function to restart the game
def restart_game(grid):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            grid[row][col] = 0
    insert_tile(grid)
    insert_tile(grid)

#display score
def display_score(screen, score):
    font = pygame.font.Font(None, FONT_SIZE)
    text = font.render("Score: " + str(score), True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_WIDTH + 50))
    screen.blit(text, text_rect)

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2048")

# Initialize the game grid
grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
insert_tile(grid)
insert_tile(grid)

#Score
score = 0
# Game loop
running = True
display=True
data=[]
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key ==pygame.K_ESCAPE:
                running=False
            elif (event.key == pygame.K_LEFT) and display :
                dictions={'grid':grid[0]+grid[1]+grid[2]+grid[3],'score':score,'move':'left','max_score': -1,'max_tile': -1}
                t=move_grid(grid, "left")
                if(t):
                    data.append(dictions)
                    insert_tile(grid)
            elif (event.key == pygame.K_RIGHT) and display:
                dictions={'grid':grid[0]+grid[1]+grid[2]+grid[3],'score':score,'move':'right','max_score': -1,'max_tile': -1}
                t=move_grid(grid, "right")
                if(t):
                    data.append(dictions)
                    insert_tile(grid)
            elif (event.key == pygame.K_UP) and display:
                dictions={'grid':grid[0]+grid[1]+grid[2]+grid[3],'score':score,'move':'up','max_score': -1,'max_tile': -1}
                t=move_grid(grid, "up")
                if(t):
                    data.append(dictions)
                    insert_tile(grid)
            elif (event.key == pygame.K_DOWN) and display:
                diction={'grid':grid[0]+grid[1]+grid[2]+grid[3],'score':score,'move':'down','max_score': -1,'max_tile': -1}
                t=move_grid(grid, "down")
                if(t):
                    data.append(diction)
                    insert_tile(grid)
            elif event.key == pygame.K_r and not display:
                restart_game(grid)
                score=0
                display=True

        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, [MARGIN_AROUND_GRID-15, MARGIN_AROUND_GRID-15, SCREEN_WIDTH - 2 * MARGIN_AROUND_GRID+30, SCREEN_WIDTH - 2 * MARGIN_AROUND_GRID+30])
        pygame.draw.rect(screen, BLACK, [MARGIN_AROUND_GRID-10, MARGIN_AROUND_GRID-10, SCREEN_WIDTH - 2 * MARGIN_AROUND_GRID+20, SCREEN_WIDTH - 2 * MARGIN_AROUND_GRID+20])
        for row in range(1,GRID_SIZE):
            pygame.draw.line(screen, WHITE, (MARGIN_AROUND_GRID-15, row * (TILE_SIZE + GRID_MARGIN)-GRID_MARGIN//2-1 + MARGIN_AROUND_GRID), (SCREEN_WIDTH - MARGIN_AROUND_GRID+15, row * (TILE_SIZE + GRID_MARGIN)-GRID_MARGIN//2-1 + MARGIN_AROUND_GRID), 2)
        for col in range(1,GRID_SIZE):
            pygame.draw.line(screen, WHITE, (col * (TILE_SIZE + GRID_MARGIN)-GRID_MARGIN//2-1 + MARGIN_AROUND_GRID, MARGIN_AROUND_GRID-15), (col * (TILE_SIZE + GRID_MARGIN)-GRID_MARGIN//2-1 + MARGIN_AROUND_GRID, SCREEN_WIDTH - MARGIN_AROUND_GRID+15), 2)
        draw_grid(screen, grid)
        if is_game_over():
            max_tile=max(grid[0]+grid[1]+grid[2]+grid[3])
            for i in range(len(data)):
                data[i]['max_score']=score
                data[i]['max_tile']=max_tile
            df=pd.concat([df,pd.DataFrame(data)])
            df.to_csv("data.csv",index=False)
            data=[]
            game_over_message(screen)
            display=False

        #Check game won
        if is_game_won(grid):
            max_tile=max(grid[0]+grid[1]+grid[2]+grid[3])
            for i in range(len(data)):
                data[i]['max_score']=score
                data[i]['max_tile']=max_tile
            df=pd.concat([df,pd.DataFrame(data)])
            df.to_csv("data.csv",index=False)
            data=[]
            game_won_message(screen)
            display=False

        #display score
        display_score(screen, score)

        #display name
        screen.blit(text, text_rect)

    # Update the display
    pygame.display.flip()

    pygame.time.delay(50)
max_tile=max(grid[0]+grid[1]+grid[2]+grid[3])
for i in range(len(data)):
    data[i]['max_score']=score
    data[i]['max_tile']=max_tile
df=pd.concat([df,pd.DataFrame(data)])
df.to_csv("data.csv",index=False)
# Quit Pygame
pygame.quit() 