import math
from turtle import width
import pygame

pygame.init()
WIDTH, HEIGHT = 900, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
font = pygame.font.SysFont("comicsans", 32)
radius = 10
paddleW = 15
paddleH = 100

class Paddle:
    VEL = 7
    def __init__(self, x, y, w, h, color, side):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.side = side
        self.lives = 3
    
    def up(self):
        if self.y > 0:
            self.y -= self.VEL
    def down(self):
        if self.y + self.h < HEIGHT:
            self.y += self.VEL

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.w, self.h))


class Ball:
    VEL = 7
    x_vel = VEL
    y_vel = VEL
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
    
    def collide(self, player1, player2):
        if self.x + self.radius >= WIDTH and self.x_vel > 0:
            self.x_vel *= -1
            player2.x, player2.y = WIDTH - paddleW - 50, HEIGHT // 2
            self.x, self.y = player2.x - self.radius, HEIGHT // 2,
            player2.lives -= 1

        if self.x - self.radius <= 0 and self.x_vel < 0:
            self.x_vel *= -1
            player1.x, player1.y = 50, HEIGHT // 2
            self.x, self.y = player1.x + self.radius, HEIGHT // 2,
            player1.lives -= 1

        if self.y - self.radius <= 0 and self.y_vel < 0:
            self.y_vel *= -1

        if  self.y + self.radius >= HEIGHT and self.y_vel > 0 :
            self.y_vel *= -1

                    
def calculate_vel_based_on_angle(ball, paddle):
    paddle_center = paddle.y + paddle.h/2
    distance_to_center = ball.y - paddle_center

    percent_width = distance_to_center / paddle.h
    angle = percent_width * 90
    angle_radians = math.radians(angle)

    y_vel = math.sin(angle_radians) * ball.VEL
    x_vel = math.cos(angle_radians) * ball.VEL

    return x_vel, y_vel

def ball_paddle_collision(ball, paddle, side):
    if side:
        if ball.x - ball.radius <= paddle.x + paddle.w and ball.x >= paddle.x + paddle.w and ball.y + ball.radius >= paddle.y and ball.y <= paddle.y + paddle.h: 
            x_vel, y_vel = calculate_vel_based_on_angle(ball, paddle)
            ball.x_vel = x_vel 
            ball.y_vel = y_vel
    else: 
        if ball.x + ball.radius >= paddle.x and ball.x + ball.radius <= paddle.x + paddle.w and ball.y + ball.radius >= paddle.y and ball.y <= paddle.y + paddle.h: 
            x_vel, y_vel = calculate_vel_based_on_angle(ball, paddle)
            ball.x_vel = x_vel * -1
            ball.y_vel = y_vel 
            

def drawText(win, text, x, y, color):
    text = font.render(text, True, color)
    text_rect = text.get_rect()
    text_rect.center = (x, y)
    win.blit(text, text_rect)

def gameLogic(ball, player1, player2):
    ball.move()
    ball.collide(player1, player2)
    ball_paddle_collision(ball, player1, player1.side)
    ball_paddle_collision(ball, player2, player2.side)

def draw(win, player1, player2, ball):
    player1.draw(win)
    player2.draw(win)
    ball.draw(win)
    drawText(win, f"Lives: {player1.lives}", 100, 30, "red")
    drawText(win, f"Lives: {player2.lives}", WIDTH - 100, 30, "red")



def update(clock):
    clock.tick(60)
    pygame.display.update()

def resetComponents():
    return Paddle(50, HEIGHT // 2, paddleW, paddleH, "white", True),\
           Paddle(WIDTH - paddleW - 50, HEIGHT // 2, paddleW, paddleH, "white", False),\
           Ball(WIDTH // 2, HEIGHT // 2, radius, "red")

def main():
    running = True
    clock = pygame.time.Clock()
    player1 = Paddle(50, HEIGHT // 2, paddleW, paddleH, "white", True)
    player2 = Paddle(WIDTH - paddleW - 50, HEIGHT // 2, paddleW, paddleH, "white", False)
    ball = Ball(WIDTH // 2, HEIGHT // 2, radius, "red")
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
        win.fill("black")
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player2.up()
        if keys[pygame.K_DOWN]:
            player2.down()
        if keys[pygame.K_w]:
            player1.up()
        if keys[pygame.K_s]:
            player1.down()
        
        if player1.lives <= 0:
            drawText(win, "Player 2 Won", WIDTH // 2, HEIGHT // 2, "white")
            update(clock)
            pygame.time.delay(3000)
            player1, player2, ball = resetComponents()
        if player2.lives <= 0:
            drawText(win, "Player 1 Won", WIDTH // 2, HEIGHT // 2, "white")
            update(clock)
            pygame.time.delay(3000)
            player1, player2, ball = resetComponents()

        gameLogic(ball, player1, player2)
        draw(win, player1, player2, ball)
        update(clock)
    
    pygame.quit()



if __name__ == "__main__":
    main()
