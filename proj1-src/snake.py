import pygame
import random
import numpy as np
import os

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
GREEN = (100, 200, 100)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLOCKSIZE = 40

# pygame init
pygame.init()
pygame.display.set_caption("20191667 홍예선")
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

class Snake:
    def __init__(self):
        self.position = [(2, 0),(1, 0),(0, 0)]
        self.direction = ''
 
    def draw(self):
        for pos in self.position: 
            pygame.draw.rect(screen, BLUE, 
            [pos[0]*BLOCKSIZE, pos[1]*BLOCKSIZE, BLOCKSIZE, BLOCKSIZE])
 
    def update(self):
        x = self.position[0][0]
        y = self.position[0][1]
        if self.direction == 'U':
            self.position = [(x, y - 1)] + self.position[0:-1]
        elif self.direction == 'D':
            self.position = [(x, y + 1)] + self.position[0:-1]
        elif self.direction == 'L':
            self.position = [(x - 1, y)] + self.position[0:-1]
        elif self.direction == 'R':
            self.position = [(x + 1, y)] + self.position[0:-1]
 
    def grow(self):
        x = self.position[-1][0]
        y = self.position[-1][1]
        if self.direction == 'U':
            self.position.append((x, y - 1))
        elif self.direction == 'D':
            self.position.append((x, y + 1))
        elif self.direction == 'L':
            self.position.append((x - 1, y))
        elif self.direction == 'R':
            self.position.append((x + 1, y))    

class Food:
    def __init__(self, position=(5, 5)):
        self.position = position
 
    def update(self):
        self.position = (random.randint(0, WINDOW_WIDTH/BLOCKSIZE - 1), 
                         random.randint(0, WINDOW_HEIGHT/BLOCKSIZE - 1))
    def draw(self):
        pygame.draw.rect(screen, RED, 
        [self.position[0]*BLOCKSIZE, self.position[1]*BLOCKSIZE, BLOCKSIZE, BLOCKSIZE])

def main():
    snake = Snake()
    food = Food()
    cnt = 0

    done = False
    while not done:
        # 1. event check
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                if event.key == pygame.K_UP:
                    snake.direction = 'U'
                elif event.key == pygame.K_DOWN:
                    snake.direction = 'D'
                elif event.key == pygame.K_LEFT:
                    snake.direction = 'L'
                elif event.key == pygame.K_RIGHT:
                    snake.direction = 'R'

        # 2. logic
        screen.fill(GRAY)

        if cnt >= 10:
            snake.update()
            cnt = 0
        
        if snake.position[0] == food.position:
            snake.grow()    
            food.update()
        
        if snake.position[0] in snake.position[1:]:
            done = True

        if (snake.position[0][0] < 0) or (snake.position[0][0] > WINDOW_WIDTH/BLOCKSIZE - 1):
            done = True

        if (snake.position[0][1] < 0) or (snake.position[0][1]> WINDOW_HEIGHT/BLOCKSIZE - 1):
            done = True
        
        cnt += 1

        # 3. draw
        snake.draw()
        food.draw()

        # 4.
        pygame.display.flip()
        clock.tick(30)

    pass

if __name__ == "__main__":
    main()