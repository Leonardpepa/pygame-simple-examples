import random
import pygame
import sys
pygame.init()

WIDTH, HEIGHT = 600, 400
snakeSize = 20
ROW, COL = WIDTH // snakeSize, HEIGHT // snakeSize 
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
delay = 100
FPS = 60
    
class Snake:

    def __init__(self, startingX, startingY, size, color):
        self.size = size
        self.color = color
        self.length = 1
        self.x_vel = size
        self.y_vel = 0
        self.x = [startingX]
        self.y = [startingY]

    def eat(self, apple):
        if self.x[0] == apple.x and self.y[0] == apple.y:
            apple.randomize() 
            self.grow()
            global delay
            if delay > 60:
                delay -= 5
    
    def grow(self):
        self.x.append(self.x[-1])
        self.y.append(self.y[-1])
        self.length += 1
    
    def collide(self):
        # when snake goes out of window it returns back
        if self.x[0] > WIDTH:
            self.x[0] = 0
        if self.x[0] < 0:
            self.x[0] = WIDTH
        if self.y[0] > HEIGHT:
            self.y[0] = 0
        if self.y[0] < 0:
            self.y[0] = HEIGHT
        # collide with it self
        for i in reversed(range(3, self.length)):
            if self.x[0] == self.x[i] and self.y[0] == self.y[i]:
                sys.exit(0)

    def draw(self, win):
        # draw head
        pygame.draw.rect(win, "magenta", (self.x[0], self.y[0], self.size, self.size))
        #  draw body
        for i in range(1, self.length):
            pygame.draw.rect(win, self.color, (self.x[i], self.y[i], self.size, self.size))
    
    def move(self):
        for i in reversed(range(1, self.length)):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]
        
        self.x[0] = self.x[0] + self.x_vel
        self.y[0] = self.y[0] + self.y_vel
    

    def up(self):
        if (self.x[0] < 0 or self.x[0] >= WIDTH) or (self.y[0] < 0 or self.y[0] >= HEIGHT):
            return 
        self.y_vel = -snakeSize
        self.x_vel = 0

    def down(self):
        if (self.x[0] < 0 or self.x[0] >= WIDTH) or (self.y[0] < 0 or self.y[0] >= HEIGHT):
            return 
        self.y_vel = snakeSize
        self.x_vel = 0
    
    def left(self):
        if (self.x[0] < 0 or self.x[0] >= WIDTH) or (self.y[0] < 0 or self.y[0] >= HEIGHT):
            return 
        self.x_vel = -snakeSize
        self.y_vel = 0

    def right(self):
        if (self.x[0] < 0 or self.x[0] >= WIDTH) or (self.y[0] < 0 or self.y[0] >= HEIGHT):
            return 
        self.x_vel = snakeSize
        self.y_vel = 0

# end of snake class
        
# Food class
class Food:
    def __init__(self):
        self.x = random.randint(0, ROW-1) * snakeSize
        self.y = random.randint(0, COL-1) * snakeSize
    
    def randomize(self):
        self.x = random.randint(0, ROW-1) * snakeSize
        self.y = random.randint(0, COL-1) * snakeSize
        
    def draw(self, win):
        pygame.draw.rect(win, "red", (self.x, self.y, snakeSize, snakeSize))

# top level functions
def draw(win, snake, apple):
    # draw 2d grid
    for i in range(ROW):
        for j in range(COL):
            pygame.draw.rect(win, "black", (i * snakeSize, j * snakeSize, snakeSize, snakeSize), 1)

    snake.draw(win)
    apple.draw(win)

def update(clock):
    pygame.display.update()
    pygame.time.delay(delay)
    clock.tick(FPS)

def gameLogic(snake, apple):
    snake.move()
    snake.eat(apple)
    snake.collide()
    

def main():
    clock = pygame.time.Clock()
    snake = Snake(WIDTH // 2, HEIGHT // 2,snakeSize, "green")
    apple = Food()
    
    direction = "R"
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        win.fill("white") # clear screen

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and direction != "R":
            direction = "L"
            snake.left()
        elif keys[pygame.K_RIGHT] and direction != "L":
            direction = "R"
            snake.right()
        elif keys[pygame.K_UP] and direction != "D":
            direction = "U"
            snake.up()
        elif keys[pygame.K_DOWN] and direction != "U":
            direction = "D"
            snake.down()
    
        gameLogic(snake, apple)
        draw(win, snake, apple)
        update(clock)
    
    pygame.quit()


if __name__ == "__main__":
    main()



