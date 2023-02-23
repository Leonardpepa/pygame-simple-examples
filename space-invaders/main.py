import random
import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")
font = pygame.font.SysFont("comicsans", 32)

playerW, playerH = 50, 30
bulletW, bulletH = 5, 15
enemyW, enemyH = 30, 30
enemyGap = 5

class Player:
    VEL = 5
    def __init__(self, x, y, w, h, color, lives):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.lives = lives

    def collide(self, bullets):
        for bullet in bullets[:]:
            if bullet.y <= self.y + self.h and bullet.y >= self.y and bullet.x + bullet.w >= self.x and bullet.x <= self.x + self.w:
                bullets.remove(bullet)
                self.lives -= 1
            
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.w, self.h))
        
    def right(self):
        if self.x + self.w >= WIDTH:
            return
        self.x += self.VEL

    def left(self):
        if self.x <= 0:
            return
        self.x -= self.VEL 

class Bullet:
    VEL = 5
    color = "red"
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def move(self):
        self.y -= self.VEL

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.w, self.h))

class EnemyBullet(Bullet):
    color = (200, 105, 0)
    def move(self):
        self.y += self.VEL


class Enemy:
    color = (200, 105, 0)
    VEL = 1
    direction = "R"
    to_move = 75
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
    
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.w, self.h))
    
    def move(self):
        if self.direction == "R":
            if self.to_move > 0:
                self.x += self.VEL
                self.to_move -= self.VEL
        elif self.direction == "L":
            if self.to_move > 0:
                self.x -= self.VEL
                self.to_move -= self.VEL

        if self.to_move == 0:
            self.direction = "L" if self.direction == "R" else "R"
            self.to_move = 150

    def collide(self, bullets):
        for bullet in bullets[:]:
            if bullet.y <= self.y + self.h and bullet.y >= self.y and bullet.x + bullet.w >= self.x and bullet.x <= self.x + self.w:
                bullets.remove(bullet)
                return True
              

def generateEnemys():
    gap = 15

    enemys = []
    for x in range(200, 600, 30 + gap):
        for y in range(20, 200, 30 + gap):
            enemys.append(Enemy(x, y, enemyW, enemyH))

    return enemys

def drawText(win, text, x, y, color):
    text = font.render(text, True, color)
    text_rect = text.get_rect()
    text_rect.center = (x, y)
    win.blit(text, text_rect)


def gameLogic(player, enemys, bullets, enemyBullets):
    player.collide(enemyBullets)
    for enemy in enemys[:]:
        if random.random() <= 0.002:
            enemyBullets.append(EnemyBullet(enemy.x + enemy.w // 2, enemy.y, bulletW, bulletH))
        enemy.move()
        if enemy.collide(bullets):
            enemys.remove(enemy)
    for bullet in bullets[:]:
        if bullet.y <= 0:
            bullets.remove(bullet)
    for bullet in bullets:
        bullet.move()
    for bullet in enemyBullets[:]:
        if bullet.y + bullet.h >= HEIGHT:
            enemyBullets.remove(bullet)
    for bullet in enemyBullets:
        bullet.move()

def update(clock):
    clock.tick(60)
    pygame.display.update()

def draw(win, player,enemys, bullets, enemyBullet):
    player.draw(win)
    for enemy in enemys:
        enemy.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    for bullet in enemyBullet:
        bullet.draw(win)
    drawText(win, f"Lives: {player.lives}", 100, HEIGHT - playerW - 30, "red")

def main():
    running = True
    clock = pygame.time.Clock()
    player = Player(WIDTH // 2 - playerW // 2, HEIGHT - playerH - 10, playerW, playerH, "magenta", 3)
    enemys = generateEnemys()
    bullets = []
    previous_time = pygame.time.get_ticks()
    enemyBullets = []

    pause = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
        keys = pygame.key.get_pressed()
        
        if pause:
            drawText(win, "Press space to start the game and p to pause it", WIDTH // 2, HEIGHT // 2, "cyan")
            draw(win, player, enemys, bullets, enemyBullets)
            update(clock)
            if keys[pygame.K_SPACE]:
                pause = False
            continue

        if keys[pygame.K_p]:
                pause = True

        if keys[pygame.K_LEFT]:
            player.left()

        if keys[pygame.K_RIGHT]:
            player.right()
        
        if keys[pygame.K_SPACE] and len(bullets) < 50:
            current_time = pygame.time.get_ticks()
            if current_time - previous_time > 200:
                previous_time = current_time
                bullets.append(Bullet(player.x + player.w // 2, player.y, bulletW, bulletH))
        
        win.fill("black")

        if player.lives <= 0:
            drawText(win, "You lost", WIDTH // 2, HEIGHT // 2, "red")
            update(clock)
            pygame.time.delay(3000)
            player = Player(WIDTH // 2 - playerW // 2, HEIGHT - playerH - 10, playerW, playerH, "magenta", 3)
            enemys = generateEnemys()
            bullets = []
            enemyBullets = []
        
        if len(enemys) == 0:
            drawText(win, "You won", WIDTH // 2, HEIGHT // 2, "green")
            update(clock)
            pygame.time.delay(3000)
            player = Player(WIDTH // 2 - playerW // 2, HEIGHT - playerH - 10, playerW, playerH, "magenta", 3)
            enemys = generateEnemys()
            bullets = []
            enemyBullets = []
        
        gameLogic(player, enemys, bullets, enemyBullets)
        draw(win, player, enemys, bullets, enemyBullets)
        update(clock)

    pygame.quit()


if __name__  == "__main__":
    main()