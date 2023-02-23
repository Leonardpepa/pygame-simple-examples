import pygame
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Brick Breaker")
font = pygame.font.SysFont("comicsans", 40)

running = True
FPS = 60
paddleW = 100
paddleH = 20
radius = 10


class Paddle(pygame.Rect):
    x_vel = 8
    
    def __init__(self, x, y, paddleW, paddleH, color):
        super().__init__((x, y, paddleH, paddleW))
        self.x = x
        self.y = y
        self.w = paddleW
        self.h = paddleH
        self.color = color
        self.lives = 3

    def draw(self, win):
        pygame.draw.rect(win, self.color, self)
    
    def left(self):
        if self.x > 0:
            self.x -= self.x_vel

    def right(self):
        if self.x + self.w < WIDTH:
            self.x += self.x_vel

class Ball:
    VEL = 8
    x_vel = 0
    y_vel = -VEL
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    
    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
    
    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel
    
    def collide(self, bricks, paddle):
        if self.x + self.radius >= WIDTH or self.x - self.radius <= 0:
            self.x_vel *= -1

        if self.y - self.radius <= 0:
            self.y_vel *= -1

        if  self.y + self.radius >= HEIGHT:
            self.y_vel *= -1
            paddle.lives -= 1
            reset_paddle_ball_pos(paddle, self)

        for brick in bricks[:]:
            if self.y - self.radius <= brick.y + brick.h and (self.x + self.radius >= brick.x and self.x <= brick.x + brick.w): 
                self.y_vel *= -1
                bricks.remove(brick)
                break

                    


class Brick:
    def __init__(self, x, y, w, h, color):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
    
    def __str__(self):
        return f'x: {self.x} y: {self.y}'
    
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.w, self.h))

# code from tech with tim youtube video
def ball_paddle_collision(ball, paddle):
    if not (ball.x <= paddle.x + paddle.w and ball.x >= paddle.x):
        return
    if not (ball.y + ball.radius >= paddle.y):
        return

    paddle_center = paddle.x + paddle.w/2
    distance_to_center = ball.x - paddle_center

    percent_width = distance_to_center / paddle.w
    angle = percent_width * 90
    angle_radians = math.radians(angle)

    x_vel = math.sin(angle_radians) * ball.VEL
    y_vel = math.cos(angle_radians) * ball.VEL * -1

    ball.x_vel = x_vel
    ball.y_vel = y_vel
    
# code from tech with tim youtube video
def generate_bricks(rows, cols, color):
    gap = 5
    brick_width = WIDTH // cols - gap
    brick_height = 20

    bricks = []
    for row in range(rows):
        for col in range(cols):
            brick = Brick(col * brick_width + gap * col, row * brick_height +
                          gap * row, brick_width, brick_height, color)
            bricks.append(brick)

    return bricks

def draw(win, paddle, ball, bricks):
    for brick in bricks:
        brick.draw(win)
    paddle.draw(win)
    ball.draw(win)
    drawText(win,f"Lives: {paddle.lives}", 100, HEIGHT - 70, "red")

def gameLogic(ball, paddle, bricks):
    ball.move()
    ball.collide(bricks, paddle)
    ball_paddle_collision(ball, paddle)

def update():
    clock.tick(FPS)
    pygame.display.update()

def drawText(win, text, x, y, color):
    text = font.render(text, True, color)
    text_rect = text.get_rect()
    text_rect.center = (x, y)
    win.blit(text, text_rect)

def reset_paddle_ball_pos(paddle, ball):
    paddle.x = WIDTH // 2
    paddle.y = HEIGHT - paddleH - 10
    ball.x = WIDTH // 2 + paddleW // 2
    ball.y = paddle.y - paddleH - radius
    ball.x_vel = 0
    ball.y_vel = ball.VEL * -1

def main():
    global running
    paddle = Paddle(WIDTH // 2, HEIGHT - paddleH - 10, paddleW, paddleH, "black")
    ball = Ball(WIDTH // 2 + paddleW // 2, paddle.y - paddleH - radius, radius, "red")
    bricks = generate_bricks(4, 10, "magenta")
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            paddle.left()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            paddle.right()

        win.fill("white")
        if paddle.lives <= 0:
            drawText(win, "You lost", WIDTH // 2, HEIGHT // 2, "red")
            update()
            pygame.time.delay(3000)
            reset_paddle_ball_pos(paddle, ball)
            paddle.lives = 3
            bricks = generate_bricks(4, 10, "magenta")

        if len(bricks) == 0:
            drawText(win, "You won", WIDTH // 2, HEIGHT // 2, "green")
            update()
            pygame.time.delay(3000)
            reset_paddle_ball_pos(paddle, ball)
            paddle.lives = 3
            bricks = generate_bricks(4, 10, "magenta")

        gameLogic(ball, paddle, bricks)
        draw(win, paddle, ball, bricks)
        update()
    
    pygame.quit()

if __name__ == "__main__":
    main()