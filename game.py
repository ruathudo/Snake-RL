import pygame
import random
from enum import Enum
from collections import namedtuple, deque
from itertools import islice

# rgb colors
WHITE = (255, 255, 255)
RED = (150, 0, 0)
BLUE1 = (0, 0, 200)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)

BLOCK_SIZE = 20
SPEED = 10

BOARD_WIDTH = 30
BOARD_HEIGHT = 20


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


Point = namedtuple('Point', ['x', 'y'])


class Snake:

    def __init__(self):
        self.w = BOARD_WIDTH
        self.h = BOARD_HEIGHT
        self.running = True
        self.score = 0
        self.food = None
        self.snake = None
        self.direction = Direction.RIGHT

        pygame.init()
        pygame.display.set_caption("Snake Game")

        self.display = pygame.display.set_mode((BOARD_WIDTH * BLOCK_SIZE, BOARD_HEIGHT * BLOCK_SIZE))
        self.font = pygame.font.SysFont('Arial', 20)

        self.update_snake()
        self.update_food()

    def on_event(self):
        """
        Handle all game events
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN

    def on_loop(self):
        """
        Handle game logic
        """
        self.update_snake()
        status = self.check_collision()

        if status == 'eat':
            self.update_food()
            self.score += 1
        elif status == 'die':
            self.running = False
        else:
            self.snake.pop()

    def on_render(self):
        """
        Handle game visual
        """
        self.display.fill(BLACK)

        # draw food
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x * BLOCK_SIZE, self.food.y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        # draw snake
        for point in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(point.x * BLOCK_SIZE, point.y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(point.x * BLOCK_SIZE + 4, point.y * BLOCK_SIZE + 4, 12, 12))

        # draw score
        text = self.font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [20, 20])

        # draw game over
        if self.running is False:
            text = self.font.render("Game Over", True, WHITE)
            text_rect = text.get_rect(center=(self.w / 2 * BLOCK_SIZE, self.h / 2 * BLOCK_SIZE))
            self.display.blit(text, text_rect)

        # render everything to the display
        pygame.display.flip()

    def on_cleanup(self):
        pygame.time.wait(2000)
        pygame.quit()

    def play(self, human=True):
        clock = pygame.time.Clock()

        while self.running:
            clock.tick(SPEED)
            self.on_event()
            self.on_loop()
            self.on_render()

        self.on_cleanup()

        return self.running, self.score

    def update_snake(self):
        if self.snake is None:
            self.snake = deque([Point(1, 0), Point(0, 0)])
        else:
            head = self.snake[0]
            x = head.x
            y = head.y

            if self.direction == Direction.LEFT:
                x -= 1
            elif self.direction == Direction.RIGHT:
                x += 1
            elif self.direction == Direction.UP:
                y -= 1
            elif self.direction == Direction.DOWN:
                y += 1
            else:
                return 0

            self.snake.appendleft(Point(x, y))

    def update_food(self):
        x = random.randint(0, (self.w - 1))
        y = random.randint(0, (self.h - 1))
        self.food = Point(x, y)

        # re-generate food if it overlaped the snake
        if self.food in self.snake:
            self.update_food()

    def check_collision(self):
        head = self.snake[0]

        if head.x == self.food.x and head.y == self.food.y:
            return 'eat'
        elif head.x < 0 or head.x >= self.w or head.y < 0 or head.y >= self.h:
            return 'die'
        elif head in islice(self.snake, 1, len(self.snake)):
            return 'die'
        else:
            return 'move'


if __name__ == '__main__':
    game = Snake()
    game.play()
