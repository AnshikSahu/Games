import pygame
import random

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
GRID_SIZE = 20
GRID_WIDTH, GRID_HEIGHT = SCREEN_WIDTH // GRID_SIZE, SCREEN_HEIGHT // GRID_SIZE
UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3
FPS = 10

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()


class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT

    def move(self):
        head_x, head_y = self.body[0]
        if self.direction == UP:
            new_head = (head_x, head_y - 1)
        elif self.direction == DOWN:
            new_head = (head_x, head_y + 1)
        elif self.direction == LEFT:
            new_head = (head_x - 1, head_y)
        else:
            new_head = (head_x + 1, head_y)
        self.body = [new_head] + self.body[:-1]

    def grow(self):
        tail_x, tail_y = self.body[-1]
        if self.direction == UP:
            new_tail = (tail_x, tail_y + 1)
        elif self.direction == DOWN:
            new_tail = (tail_x, tail_y - 1)
        elif self.direction == LEFT:
            new_tail = (tail_x + 1, tail_y)
        else:
            new_tail = (tail_x - 1, tail_y)
        self.body.append(new_tail)

    def draw(self):
        pygame.draw.rect(screen, BLUE, (self.body[0][0] * GRID_SIZE, self.body[0][1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        for segment in self.body[1:]:
            pygame.draw.rect(screen, GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))


class Food:
    def __init__(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    def respawn(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    def draw(self):
        pygame.draw.rect(screen, RED, (self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))


def check_collision(snake, food):
    if snake.body[0] == food.position:
        snake.grow()
        food.respawn()


def main():
    snake = Snake()
    food = Food()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != DOWN:
                    snake.direction = UP
                elif event.key == pygame.K_DOWN and snake.direction != UP:
                    snake.direction = DOWN
                elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                    snake.direction = LEFT
                elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                    snake.direction = RIGHT

        snake.move()

        screen.fill(WHITE)
        snake.draw()
        food.draw()
        check_collision(snake, food)

        if snake.body[0] in snake.body[1:]:
            # Snake collided with itself, game over
            pygame.quit()
            quit()

        if snake.body[0][0] < 0 or snake.body[0][0] >= GRID_WIDTH or snake.body[0][1] < 0 or snake.body[0][1] >= GRID_HEIGHT:
            # Snake collided with the wall, game over
            pygame.quit()
            quit()

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
