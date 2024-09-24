from flask import Flask, render_template, request, jsonify
import random
import copy

app = Flask(__name__)

color_mapping = {
    '': (1, 1, 1),  # Grey
    2: (173, 216, 230),  # Light blue
    4: (144, 238, 144),  # Light green
    8: (255, 165, 0),    # Orange
    16: (255, 223, 0),   # Yellow
    32: (138, 43, 226),  # Purple
    64: (255, 0, 0),     # Red
    128: (0, 0, 255),    # Blue
    256: (0, 128, 0),    # Green
    512: (255, 0, 255),  # Magenta
    1024: (255, 69, 0),  # Red-Orange
    2048: (255, 215, 0),       # Gold
    4096: (183,104,83),      # Gold-Red
    8192: (255, 255, 255)       # White 
}

GRID_SIZE = 4
empty=[[''] * GRID_SIZE for _ in range(GRID_SIZE)]
empty_color=[[(1, 1, 1)] * GRID_SIZE for _ in range(GRID_SIZE)]
grid = copy.deepcopy(empty)
colors = copy.deepcopy(empty_color)
n=random.randint(0,GRID_SIZE-1)
m=random.randint(0,GRID_SIZE-1)
grid[n][m]=random.choice([2,2,2,4])
colors[n][m]=color_mapping[grid[n][m]]
score = 0
display = True

def is_game_over():
    global grid
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] == '':
                return 0
            if col < GRID_SIZE - 1 and grid[row][col] == grid[row][col + 1]:
                return 0
            if row < GRID_SIZE - 1 and grid[row][col] == grid[row + 1][col]:
                return 0
    return 1

# Function to insert a new random tile (2 or 4) into the grid
def insert_tile(grid):
    global colors
    empty_cells = [(row, col) for row in range(GRID_SIZE) for col in range(GRID_SIZE) if grid[row][col] == '']
    if empty_cells:
        row, col = random.choice(empty_cells)
        grid[row][col] = random.choice([2,2,2,4])
        colors[row][col]=color_mapping[grid[row][col]]

# Function to merge tiles in a row or column
def merge(line):
    global score
    changed = False
    merged_line = []
    previous_tile = None
    for tile in line:
        if tile != '':
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
    merged_line= merged_line + [''] * (len(line) - len(merged_line))
    if merged_line != line:
        changed = True
    return merged_line, changed

# Function to move the grid in a given direction
def move_grid(grid, direction):
    global score, colors
    changed=False
    if direction == "left":
        for row in range(GRID_SIZE):
            grid[row], change = merge(grid[row])
            if change:
                for col in range(GRID_SIZE):
                    colors[row][col]=color_mapping[grid[row][col]]
                changed=True
    elif direction == "right":
        for row in range(GRID_SIZE):
            grid[row], change = merge(grid[row][::-1])
            grid[row] = grid[row][::-1]
            if change:
                for col in range(GRID_SIZE):
                    colors[row][col]=color_mapping[grid[row][col]]
                changed=True
    elif direction == "up":
        columns = [[grid[row][col] for row in range(GRID_SIZE)] for col in range(GRID_SIZE)]
        # columns = [merge(col) for col in columns]
        # for row in range(GRID_SIZE):
        #     for col in range(GRID_SIZE):
        #         grid[row][col] = columns[col][row]
        for col in range(GRID_SIZE):
            columns[col], change = merge(columns[col])
            if change:
                changed=True
                for row in range(GRID_SIZE):
                    grid[row][col] = columns[col][row]
                    colors[row][col]=color_mapping[grid[row][col]]
    elif direction == "down":
        columns = [[grid[row][col] for row in range(GRID_SIZE)] for col in range(GRID_SIZE)]
        # columns = [merge(col[::-1])[::-1] for col in columns]
        # for row in range(GRID_SIZE):
        #     for col in range(GRID_SIZE):
        #         grid[row][col] = columns[col][row]
        for col in range(GRID_SIZE):
            columns[col], change = merge(columns[col][::-1])
            if change:
                changed=True
                for row in range(GRID_SIZE):
                    grid[row][col] = columns[col][GRID_SIZE-1-row]
                    colors[row][col]=color_mapping[grid[row][col]]
    return changed

@app.route('/')
def index():
    global grid, score, colors
    return render_template('index.html', grid=grid, score=score,colors=colors,gameOver=0)

@app.route('/reset', methods=['POST'])
def reset():
    global grid, score, empty, empty_color, colors
    grid = copy.deepcopy(empty)
    n=random.randint(0,GRID_SIZE-1)
    m=random.randint(0,GRID_SIZE-1)
    grid[n][m]=random.choice([2,2,2,4])
    score = 0
    colors=copy.deepcopy(empty_color)
    colors[n][m]=color_mapping[grid[n][m]]
    return jsonify({'grid': grid, 'score': score, 'colors':colors, 'gameOver':0})

@app.route('/move', methods=['POST'])
def handle_move():
    global grid, score

    direction = request.form.get('direction')
    if direction == 'left':
        t = move_grid(grid, "left")
    elif direction == 'right':
        t = move_grid(grid, "right")
    elif direction == 'up':
        t = move_grid(grid, "up")
    elif direction == 'down':
        t = move_grid(grid, "down")

    if t:
        insert_tile(grid)
        # Add any additional logic here
    
    gameOver=is_game_over()

    return jsonify({'grid': grid, 'score': score, 'colors':colors, 'gameOver':gameOver})


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080, debug=True)