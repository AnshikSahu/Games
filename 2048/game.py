import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Snake class
class Snake:
    def __init__(self):
        self.body = [(200, 200), (210, 200), (220, 200)]  # Initial segments
        self.direction = pygame.math.Vector2(1, 0)  # Initial direction
        self.speed = 5

    def move(self, target_pos):
        # Calculate the direction vector towards the mouse pointer
        direction_vector = pygame.math.Vector2(target_pos[0] - self.body[0][0], target_pos[1] - self.body[0][1])
        direction_vector.normalize_ip()

        # Update the snake's direction
        self.direction = direction_vector

        # Move each segment except the head
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i] = (self.body[i - 1][0], self.body[i - 1][1])

        # Move the head
        self.body[0] = (self.body[0][0] + self.direction.x * 20, self.body[0][1] + self.direction.y * 20)

    def grow(self):
        # Add a new segment to the end of the snake
        self.body.append((self.body[-1][0], self.body[-1][1]))

    def draw(self, surface):
        for pos in self.body:
            pygame.draw.rect(surface, GREEN, (pos[0], pos[1], 20, 20))

# Main function
def main():
    # Set up the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake Game")

    # Initialize snake
    snake = Snake()

    # Main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Move snake towards mouse pointer
        snake.move(mouse_pos)

        # Draw everything
        screen.fill(BLACK)
        snake.draw(screen)
        pygame.display.flip()
        pygame.time.Clock().tick(10)

if __name__ == "__main__":
    main()
